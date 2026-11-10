from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys
import webbrowser

from vockpit import __version__, checks, d2, diagrams, registry, viewerdata
from vockpit.findings import format_findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="vockpit",
        description="Vockpit: the Vibe Coding Cockpit. You steer. AI builds.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"vockpit {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command")

    # init
    p_init = subparsers.add_parser("init", help="Create a starter project")
    p_init.add_argument("path", nargs="?", default=".", help="Target folder")

    # generate
    p_gen = subparsers.add_parser("generate", help="Generate diagrams and viewer files")
    p_gen.add_argument("--root", default=".", help="Project root folder")
    p_gen.add_argument("--no-svg", action="store_true", help="Do not render SVGs with d2")

    # check
    p_check = subparsers.add_parser("check", help="Check model and freshness")
    p_check.add_argument("--root", default=".", help="Project root folder")

    # view
    p_view = subparsers.add_parser("view", help="View diagrams in a browser")
    p_view.add_argument("id", nargs="?", default=None, help="Item id to focus on")
    p_view.add_argument("--root", default=".", help="Project root folder")
    p_view.add_argument("--no-open", action="store_true", help="Print address without opening browser")

    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help(sys.stderr)
        return 2

    if args.command == "init":
        from vockpit import scaffold
        return scaffold.init_project(Path(args.path))

    elif args.command == "generate":
        return cmd_generate(Path(args.root), no_svg=args.no_svg)

    elif args.command == "check":
        return cmd_check(Path(args.root))

    elif args.command == "view":
        return cmd_view(Path(args.root), focus_id=args.id, no_open=args.no_open)

    return 2


def cmd_generate(root: Path, no_svg: bool = False) -> int:
    root = root.resolve()
    sys_yaml = root / "model" / "system.yaml"
    if not sys_yaml.is_file():
        print(f"No project found in '{root}'.", file=sys.stderr)
        return 2

    # Step 1: load and check C01, C02, C03
    c01_findings = checks.check_c01(root)
    if any(f.severity == "ERROR" for f in c01_findings):
        print(format_findings(c01_findings))
        return 1

    model, _ = registry.load(root)
    if model is None:
        print(format_findings(c01_findings))
        return 1

    c02_c03_findings = checks.check_c02(root, model) + checks.check_c03(model)
    early_errors = [f for f in c02_c03_findings if f.severity == "ERROR"]
    if early_errors:
        print(format_findings(early_errors))
        return 1

    # Step 2: delete old .d2 and .svg, build and write new .d2
    diag_dir = root / "docs" / "diagrams"
    diag_dir.mkdir(parents=True, exist_ok=True)
    for old_file in list(diag_dir.glob("*.d2")) + list(diag_dir.glob("*.svg")):
        old_file.unlink()

    diag_list = diagrams.build(model)
    for d in diag_list:
        d2_file = diag_dir / f"{d.name}.d2"
        d2_file.write_text(d2.render(d), encoding="utf-8")

    # Step 3: Unless --no-svg: render each .d2 to .svg
    svg_map: dict[str, str] | None = None
    if not no_svg:
        d2_bin = d2.find_d2_executable()
        if not d2_bin:
            print("d2 not found on PATH. Install from https://d2lang.com or use --no-svg.")
            return 2

        svg_map = {}
        for d in diag_list:
            d2_file = diag_dir / f"{d.name}.d2"
            svg_file = diag_dir / f"{d.name}.svg"
            d2.to_svg(d2_file, svg_file, d2_bin=d2_bin)
            svg_map[d.name] = svg_file.read_text(encoding="utf-8")

    # Step 4: Write docs/viewer/model.js, diagrams.js, and index.html
    viewer_dir = root / "docs" / "viewer"
    viewer_dir.mkdir(parents=True, exist_ok=True)
    viewerdata.write_viewer_data(viewer_dir, model, diag_list, svg_map)

    index_asset = Path(__file__).parent / "assets" / "viewer" / "index.html"
    if index_asset.is_file():
        shutil.copyfile(index_asset, viewer_dir / "index.html")

    # Step 5: Print one line per diagram, then Generated N diagrams. Print C26 warnings.
    for d in diag_list:
        print(d.name)
    print(f"Generated {len(diag_list)} diagrams.")

    c26_warnings = checks.check_c26(diag_list)
    if c26_warnings:
        print(format_findings(c26_warnings))

    return 0


def cmd_check(root: Path) -> int:
    root = root.resolve()
    if not root.exists():
        print(f"Path does not exist: '{root}'", file=sys.stderr)
        return 2

    findings = checks.run_model_checks(root)
    if findings:
        print(format_findings(findings))

    num_errors = sum(1 for f in findings if f.severity == "ERROR")
    num_warns = sum(1 for f in findings if f.severity == "WARN")

    if num_errors == 0 and num_warns == 0:
        print("OK")
        return 0
    elif num_errors == 0:
        print(f"OK with {num_warns} warning(s)")
        return 0
    else:
        print(f"FAILED: {num_errors} error(s), {num_warns} warning(s)")
        return 1


def cmd_view(root: Path, focus_id: str | None = None, no_open: bool = False) -> int:
    root = root.resolve()
    viewer_html = root / "docs" / "viewer" / "index.html"
    if not viewer_html.is_file():
        print('Run "vockpit generate" first.')
        return 2

    if focus_id is not None:
        model, _ = registry.load(root)
        if model is None:
            print(f"No item with id '{focus_id}'.")
            return 2
        valid_ids = {model.system.id} | {a.id for a in model.actors} | {b.id for b in model.boxes}
        if focus_id not in valid_ids:
            print(f"No item with id '{focus_id}'.")
            return 2

    url = viewer_html.as_uri()
    if focus_id:
        url += f"#/{focus_id}"

    print(url)
    if not no_open:
        webbrowser.open(url)

    return 0


if __name__ == "__main__":
    sys.exit(main())
