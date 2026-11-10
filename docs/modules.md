# Vockpit 0.1 Module Specifications

## 1. `vockpit.findings`
Defines finding models and output formatting.

### Classes
- `Finding(rule: str, severity: str, location: str, message: str)`:
  Represents a diagnostic issue (`ERROR` or `WARN`). Implements `__str__` formatted as:
  `{rule} {severity} {location}: {message}`
  Implements `__lt__` sorting by `(rule, location, message, severity)`.

### Functions
- `format_findings(findings: Sequence[Finding]) -> str`:
  Sorts findings and joins them with newlines.

---

## 2. `vockpit.registry`
Parses and loads declarative YAML model files.

### Classes
- `System(id: str, title: str, summary: str)`: The root system definition.
- `Actor(id: str, title: str, kind: str, summary: str = "")`: An external user or external system.
- `Box(id: str, title: str, summary: str, inputs: list[str], outputs: list[str], parent: str, level: int, children: list[str], source: str)`: An L1 or L2 system box.
- `Edge(from_id: str, to_id: str, data: str, source: str)`: Directed connection. Provides `.to` and `.from_` properties.
- `Model(system: System, actors: list[Actor], boxes: list[Box], edges: list[Edge])`: Full in-memory model graph with `.get_box()` and `.get_actor()` helpers.

### Functions
- `validate_c01(root: Path) -> list[Finding]`: Validates YAML schema, permitted keys, required fields, and naming patterns.
- `load(root: Path | str) -> tuple[Model | None, list[Finding]]`: Loads project model files from `root`. Returns `(None, findings)` if C01 schema validation fails.

---

## 3. `vockpit.checks`
Enforces the Vockpit verification rules.

### Functions
- `check_c01(root: Path | str) -> list[Finding]`: Runs C01 schema checks.
- `check_c02(root: Path | str, model: Model) -> list[Finding]`: Enforces ID uniqueness across the global project namespace and verifies parent L1 box IDs.
- `check_c03(model: Model) -> list[Finding]`: Validates edge endpoints, forbids system ID, detects self-loops, and forbids actor-to-actor edges.
- `check_c10(root: Path | str, model: Model, diag_list: list[Diagram]) -> list[Finding]`: Verifies `.d2` and `model.js` freshness against in-memory generated state; warns on missing `.svg` or `diagrams.js`.
- `check_c26(diag_list: list[Diagram]) -> list[Finding]`: Warns if any diagram contains more than 12 nodes.
- `run_model_checks(root: Path | str) -> list[Finding]`: Runs staged validation pipeline (C01 -> C02/C03 -> C10/C26).

---

## 4. `vockpit.diagrams`
Projects the model into diagram structures.

### Classes
- `DiagramNode(id: str, title: str, summary: str, role: str, link: str)`: Node in a diagram (`system`, `inner`, `person`, `external`, `neighbour`).
- `DiagramEdge(from_id: str, to_id: str, label: str)`: Directed edge between diagram nodes with merged data labels.
- `Diagram(name: str, title: str, nodes: list[DiagramNode], edges: list[DiagramEdge])`: Diagram container.

### Functions
- `build(model: Model) -> list[Diagram]`: Builds `L0_context`, `L1_system`, and all `L2_<id>` diagrams.

---

## 5. `vockpit.d2`
Renders D2 syntax and invokes the D2 CLI.

### Functions
- `escape_d2(s: str) -> str`: Escapes backslashes, quotes, and collapses newlines to single spaces.
- `node_key(node_id: str) -> str`: Generates D2 key (`n_<id>` with hyphens replaced by underscores).
- `render(diagram: Diagram) -> str`: Deterministically renders a `Diagram` object as D2 text.
- `find_d2_executable() -> str | None`: Locates `d2` on `PATH` or in `~/bin`.
- `to_svg(d2_path: Path | str, svg_path: Path | str, d2_bin: str | None = None) -> None`: Converts a `.d2` file to `.svg`.

---

## 6. `vockpit.viewerdata`
Prepares payload files for the browser viewer.

### Functions
- `build_model_js(model: Model, diagrams_list: list[Diagram]) -> str`: Produces `window.VOCKPIT_MODEL = { ... };`.
- `build_diagrams_js(svg_map: dict[str, str] | None = None) -> str`: Produces `window.VOCKPIT_SVG = { ... };`.
- `write_viewer_data(viewer_dir: Path, model: Model, diagrams_list: list[Diagram], svg_map: dict[str, str] | None = None) -> None`: Writes `model.js` and `diagrams.js` into `docs/viewer/`.

---

## 7. `vockpit.scaffold`
Bootstraps starter projects.

### Functions
- `init_project(target: Path) -> int`: Copies starter assets (`system.yaml`, `brief.md`, `.gitkeep`, `SKILL.md`), triggers initial `generate`, and skips existing files.

---

## 8. `vockpit.cli`
Command-line interface entry point.

### Functions
- `main(argv: list[str] | None = None) -> int`: Parses flags, routes commands (`init`, `generate`, `check`, `view`), and returns standard exit codes (`0`, `1`, `2`).
- `cmd_generate(root: Path, no_svg: bool = False) -> int`: Implements `vockpit generate`.
- `cmd_check(root: Path) -> int`: Implements `vockpit check`.
- `cmd_view(root: Path, focus_id: str | None = None, no_open: bool = False) -> int`: Implements `vockpit view`.
