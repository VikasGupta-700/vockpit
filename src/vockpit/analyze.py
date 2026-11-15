from __future__ import annotations

import ast
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from vockpit import registry
from vockpit.findings import format_findings

SKIP_DIRS = {
    "__pycache__",
    "build",
    "dist",
    "env",
    "node_modules",
    "site-packages",
    "venv",
}
TEST_DIRS = {"test", "tests"}
# Packaging/test plumbing, not part of the system's structure.
SKIP_FILES = {"setup.py", "conftest.py"}
MAX_EDGE_NAMES = 3
TOP_N = 5


@dataclass
class ImportRef:
    level: int
    module: str
    names: list[str]


@dataclass
class ModuleInfo:
    path: str
    dotted: str
    is_init: bool
    doc: str
    classes: int
    functions: int
    loc: int
    imports: list[ImportRef]


@dataclass
class Unit:
    id: str
    key: str
    summary: str
    modules: list[ModuleInfo]
    children: dict[str, ModuleInfo] = field(default_factory=dict)


@dataclass
class Analysis:
    name: str
    system_id: str
    source_root: str
    units_root: str
    modules: list[ModuleInfo]
    units: list[Unit]
    l1_edges: dict[tuple[str, str], set[str]]
    l2_edges: dict[tuple[str, str], set[str]]
    external: Counter[str]
    warnings: list[str]
    test_files: int


def _make_id(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "unit"
    return s if s[0].isalpha() else f"m-{s}"


def _unique(base: str, used: set[str]) -> str:
    candidate = base
    n = 2
    while candidate in used:
        candidate = f"{base}-{n}"
        n += 1
    used.add(candidate)
    return candidate


def _first_line(doc: str | None) -> str:
    if not doc or not doc.strip():
        return ""
    return doc.strip().splitlines()[0].strip()


def _is_test_file(name: str) -> bool:
    return name.startswith("test_") or name.endswith("_test.py")


def _scan_file(path: Path, root: Path, source_root: Path, warnings: list[str]) -> ModuleInfo | None:
    try:
        rel = path.resolve().relative_to(root)
    except ValueError:
        warnings.append(f"{path.name}: resolves outside the project root, skipped")
        return None
    rel_posix = rel.as_posix()
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=rel_posix, type_comments=True)
    except (OSError, UnicodeDecodeError) as e:
        warnings.append(f"{rel_posix}: could not be read ({e.__class__.__name__}), skipped")
        return None
    except (SyntaxError, ValueError) as e:
        warnings.append(f"{rel_posix}: syntax error ({e}), skipped")
        return None

    imports: list[ImportRef] = []
    classes = functions = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(ImportRef(0, alias.name, []) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(ImportRef(node.level, node.module or "", [a.name for a in node.names]))
        elif isinstance(node, ast.ClassDef):
            classes += 1
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions += 1

    parts = list(path.resolve().relative_to(source_root.resolve()).with_suffix("").parts)
    is_init = parts[-1] == "__init__"
    if is_init:
        parts = parts[:-1]
    return ModuleInfo(
        path=rel_posix,
        dotted=".".join(parts),
        is_init=is_init,
        doc=_first_line(ast.get_docstring(tree)),
        classes=classes,
        functions=functions,
        loc=sum(1 for line in text.splitlines() if line.strip()),
        imports=imports,
    )


def _pick_source_root(root: Path) -> Path:
    src = root / "src"
    if src.is_dir() and any(src.rglob("*.py")):
        return src
    return root


def _skip_dir(name: str) -> bool:
    return name in SKIP_DIRS or name.startswith(".") or name.endswith(".egg-info")


def _walk(source_root: Path, root: Path, warnings: list[str]) -> list[ModuleInfo]:
    modules: list[ModuleInfo] = []
    for dirpath, dirnames, filenames in os.walk(source_root, followlinks=False):
        dirnames[:] = sorted(d for d in dirnames if not _skip_dir(d) and d not in TEST_DIRS)
        for name in sorted(filenames):
            if not name.endswith(".py") or name in SKIP_FILES or _is_test_file(name):
                continue
            info = _scan_file(Path(dirpath) / name, root, source_root, warnings)
            if info is not None:
                modules.append(info)
    return modules


def _count_test_files(root: Path) -> int:
    count = 0
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = [d for d in dirnames if not _skip_dir(d)]
        in_tests = any(part in TEST_DIRS for part in Path(dirpath).relative_to(root).parts)
        count += sum(1 for n in filenames if n.endswith(".py") and (in_tests or _is_test_file(n)))
    return count


def _pick_units_root(source_root: Path, root: Path, modules: list[ModuleInfo]) -> str:
    """Descend into the lone package of a single-package project."""
    prefix = source_root.relative_to(root).as_posix()
    prefix = "" if prefix == "." else prefix + "/"
    top_dirs: set[str] = set()
    loose = False
    for m in modules:
        parts = m.path[len(prefix) :].split("/")
        if len(parts) == 1:
            loose = loose or parts[0] != "__init__.py"
        else:
            top_dirs.add(parts[0])
    if len(top_dirs) == 1 and not loose:
        return f"{prefix}{next(iter(top_dirs))}/"
    return prefix


def _unit_key(m: ModuleInfo, units_prefix: str) -> str | None:
    if not m.path.startswith(units_prefix):
        return None
    parts = m.path[len(units_prefix) :].split("/")
    if len(parts) == 1:
        return None if parts[0] == "__init__.py" else parts[0][:-3]
    return parts[0]


def _build_units(modules: list[ModuleInfo], units_prefix: str) -> list[Unit]:
    groups: dict[str, list[ModuleInfo]] = {}
    for m in modules:
        key = _unit_key(m, units_prefix)
        if key is not None:
            groups.setdefault(key, []).append(m)

    used: set[str] = set()
    units: list[Unit] = []
    for key in sorted(groups):
        unit = Unit(
            id=_unique(_make_id(key), used),
            key=key,
            summary="",
            modules=sorted(groups[key], key=lambda m: m.path),
        )
        units.append(unit)

    for unit in units:
        is_package = any(m.path[len(units_prefix) :].count("/") >= 1 for m in unit.modules)
        if is_package:
            init = next(
                (m for m in unit.modules if m.path == f"{units_prefix}{unit.key}/__init__.py"),
                None,
            )
            for m in unit.modules:
                if m.is_init:
                    continue
                rel = m.path[len(units_prefix) + len(unit.key) + 1 : -3].replace("/", "-")
                child_id = _unique(_make_id(f"{unit.id}-{rel}"), used)
                unit.children[child_id] = m
            n = len(unit.children)
            unit.summary = (init.doc if init else "") or f"Package with {n} module(s)."
        else:
            unit.summary = unit.modules[0].doc or "No docstring."
    return units


def _resolve_import(mod: ModuleInfo, ref: ImportRef, index: dict[str, ModuleInfo]) -> set[str]:
    if ref.level:
        pkg = mod.dotted.split(".") if mod.dotted else []
        if not mod.is_init:
            pkg = pkg[:-1]
        up = ref.level - 1
        if up > len(pkg):
            return set()
        base_parts = pkg[: len(pkg) - up]
        if ref.module:
            base_parts = [*base_parts, ref.module]
        base = ".".join(base_parts)
    else:
        base = ref.module

    found: set[str] = set()
    if ref.names:
        for n in ref.names:
            cand = f"{base}.{n}" if base else n
            if cand in index:
                found.add(cand)
            elif base in index:
                found.add(base)
        return found
    parts = base.split(".")
    for i in range(len(parts), 0, -1):
        cand = ".".join(parts[:i])
        if cand in index:
            return {cand}
    return found


def _edge_data(names: set[str]) -> str:
    ordered = sorted(names)
    shown = ", ".join(ordered[:MAX_EDGE_NAMES])
    extra = len(ordered) - MAX_EDGE_NAMES
    return f"imports {shown}" + (f" (+{extra} more)" if extra > 0 else "")


def analyze(root: Path) -> Analysis:
    root = Path(root).resolve()
    warnings: list[str] = []
    source_root = _pick_source_root(root)
    modules = _walk(source_root, root, warnings)
    test_files = _count_test_files(root)
    units_prefix = _pick_units_root(source_root, root, modules)
    units = _build_units(modules, units_prefix)

    index = {m.dotted: m for m in modules if m.dotted}
    where: dict[str, tuple[str, str | None]] = {}
    for unit in units:
        child_of = {id(m): cid for cid, m in unit.children.items()}
        for m in unit.modules:
            if m.dotted:
                where[m.dotted] = (unit.id, child_of.get(id(m)))

    l1_edges: dict[tuple[str, str], set[str]] = {}
    l2_edges: dict[tuple[str, str], set[str]] = {}
    internal_tops = {d.split(".")[0] for d in index}
    external: Counter[str] = Counter()
    stdlib = set(sys.stdlib_module_names) | {"__future__"}

    for m in modules:
        seen_ext: set[str] = set()
        for ref in m.imports:
            if ref.level == 0 and ref.module:
                top = ref.module.split(".")[0]
                if top not in stdlib and top not in internal_tops:
                    seen_ext.add(top)
            src = where.get(m.dotted) if m.dotted else None
            if src is None:
                continue
            for target in _resolve_import(m, ref, index):
                dst = where.get(target)
                if dst is None or target == m.dotted:
                    continue
                if src[0] != dst[0]:
                    l1_edges.setdefault((src[0], dst[0]), set()).add(target)
                elif src[1] and dst[1] and src[1] != dst[1]:
                    l2_edges.setdefault((src[1], dst[1]), set()).add(target)
        external.update(seen_ext)

    name = root.name or "project"
    return Analysis(
        name=name,
        system_id=_make_id(name),
        source_root=source_root.relative_to(root).as_posix(),
        units_root=units_prefix.rstrip("/") or ".",
        modules=modules,
        units=units,
        l1_edges=l1_edges,
        l2_edges=l2_edges,
        external=external,
        warnings=warnings,
        test_files=test_files,
    )


def _dump(data: dict[str, object]) -> str:
    text: str = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100)
    return text


def _edges_list(edges: dict[tuple[str, str], set[str]]) -> list[dict[str, str]]:
    return [
        {"from": a, "to": b, "data": _edge_data(names)} for (a, b), names in sorted(edges.items())
    ]


def build_model_files(a: Analysis) -> dict[str, str]:
    boxes: list[dict[str, object]] = [
        {
            "id": u.id,
            "title": u.key,
            "summary": u.summary,
            "code": [m.path for m in u.modules],
        }
        for u in a.units
    ]
    system: dict[str, object] = {
        "system": {
            "id": a.system_id,
            "title": a.name,
            "summary": f"Structure of {a.name}, generated from its Python imports.",
        },
        "boxes": boxes,
    }
    l1 = _edges_list(a.l1_edges)
    if l1:
        system["edges"] = l1
    files = {"model/system.yaml": _dump(system)}

    for u in a.units:
        if not u.children:
            continue
        child_boxes: list[dict[str, object]] = [
            {
                "id": cid,
                "title": m.path.rsplit("/", 1)[-1][:-3],
                "summary": m.doc or "No docstring.",
                "code": [m.path],
            }
            for cid, m in sorted(u.children.items())
        ]
        box_file: dict[str, object] = {"parent": u.id, "boxes": child_boxes}
        own = {k: v for k, v in a.l2_edges.items() if k[0] in u.children and k[1] in u.children}
        if own:
            box_file["edges"] = _edges_list(own)
        files[f"model/boxes/{u.id}.yaml"] = _dump(box_file)
    return files


def _cell(text: str) -> str:
    return text.replace("|", "\\|")


def render_report(a: Analysis) -> str:
    lines = [f"# Structure report: {a.name}", ""]
    total_loc = sum(m.loc for m in a.modules)
    lines += [
        "## Overview",
        "",
        f"- Source root: `{a.source_root}`",
        f"- Modules analysed: {len(a.modules)} ({total_loc} non-blank lines)",
        f"- Classes: {sum(m.classes for m in a.modules)}, "
        f"functions: {sum(m.functions for m in a.modules)}",
        f"- Top-level units (diagram boxes): {len(a.units)}",
        f"- Test files (not modelled): {a.test_files}",
        "",
        "## Structure",
        "",
    ]
    for u in a.units:
        lines.append(f"### {u.id}")
        lines += ["", u.summary, ""]
        if u.children:
            lines += [
                "| Module | File | Lines | Classes | Functions | Summary |",
                "|---|---|---|---|---|---|",
            ]
            for cid, m in sorted(u.children.items()):
                lines.append(
                    f"| {cid} | `{m.path}` | {m.loc} | {m.classes} | {m.functions} "
                    f"| {_cell(m.doc or 'No docstring.')} |"
                )
        else:
            m = u.modules[0]
            lines.append(f"`{m.path}`: {m.loc} lines, {m.classes} classes, {m.functions} functions")
        lines.append("")

    lines += ["## Dependencies", ""]
    if a.l1_edges:
        lines.append("Unit-to-unit imports:")
        lines.append("")
        for (src, dst), names in sorted(a.l1_edges.items()):
            lines.append(f"- {src} -> {dst}: {_edge_data(names)}")
    else:
        lines.append("No imports between top-level units.")
    cycles = sorted({tuple(sorted(k)) for k in a.l1_edges if (k[1], k[0]) in a.l1_edges})
    if cycles:
        lines += ["", "Circular dependencies between units:", ""]
        lines += [f"- {x} <-> {y}" for x, y in cycles]

    fan_in: Counter[str] = Counter()
    for names in [*a.l1_edges.values(), *a.l2_edges.values()]:
        fan_in.update(names)
    if fan_in:
        lines += ["", f"Most imported modules (top {TOP_N}):", ""]
        lines += [
            f"- `{name}`: imported from {n} place(s)" for name, n in fan_in.most_common(TOP_N)
        ]

    lines += ["", "External packages imported:", ""]
    if a.external:
        lines += [f"- {name}: {n} module(s)" for name, n in sorted(a.external.items())]
    else:
        lines.append("None (standard library only).")

    lines += ["", "## Warnings", ""]
    lines += [f"- {w}" for w in a.warnings] if a.warnings else ["None."]
    lines.append("")
    return "\n".join(lines)


def _write(root: Path, rel: str, text: str) -> None:
    target = root / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")


def run(path: Path, force: bool = False) -> int:
    root = Path(path).resolve()
    if not root.is_dir():
        print(f"Path is not a folder: '{root}'", file=sys.stderr)
        return 2
    if (root / "model" / "system.yaml").exists() and not force:
        print("model/system.yaml already exists. Use --force to overwrite the model.")
        return 1

    a = analyze(root)
    if not a.units:
        print(f"No Python modules found in '{root}'.")
        return 1

    files = build_model_files(a)
    files["docs/analysis.md"] = render_report(a)
    if force:
        for old in (root / "model" / "boxes").glob("*.yaml"):
            old.unlink()
    for rel, text in files.items():
        _write(root, rel, text)

    errors = [f for f in registry.validate_c01(root) if f.severity == "ERROR"]
    if errors:
        print(format_findings(errors))
        return 1

    for rel in files:
        print(f"wrote {rel}")
    print(f"Analyzed {len(a.modules)} modules into {len(a.units)} boxes.")
    for w in a.warnings:
        print(f"warning: {w}")
    print('Next: "vockpit generate" then "vockpit view".')
    return 0
