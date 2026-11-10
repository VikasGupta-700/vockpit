# Changelog

All notable changes to Vockpit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-11-10

### Added
- **Core Registry**: Loads system, actors, L1 boxes, and L2 boxes from `model/system.yaml` and `model/boxes/*.yaml`.
- **Validation Engine**:
  - `C01`: Schema and structural validation.
  - `C02`: Identity uniqueness and parent relationship validation.
  - `C03`: Directed edge endpoint and relationship validation.
  - `C10`: Diagram and viewer freshness verification.
  - `C26`: Diagram size sanity checks (>12 nodes warning).
- **Diagram Generation**: Builds `L0_context`, `L1_system`, and `L2_<id>` diagrams with automatic edge mapping and merging.
- **D2 & SVG Integration**: Deterministic D2 syntax generation with SVG conversion via CLI tool `d2`.
- **Interactive Drill-Down Viewer**: Standalone HTML/CSS/JS viewer supporting click-to-zoom, pan and zoom, inspector sidebar, deep hash routing, keyboard navigation (`Escape`), and dark mode.
- **CLI Suite**: `vockpit init`, `vockpit generate`, `vockpit check`, and `vockpit view`.
- **Pack-Draft Skill**: AI agent skill for scaffolding models from `brief.md`.
- **Reference Example**: Full online shop demo in `examples/shop/`.

---

## Known Limits in 0.1.0

1. **L1 Edges in L2 Diagrams**:
   An edge declared between subsystems at L1 (e.g. in `system.yaml`) does not appear inside an L2 diagram unless it explicitly names an L2 box as an endpoint. In L2 diagrams, connections are resolved between internal L2 components and external neighbour subsystems.
2. **Fixed 3-Level Depth**:
   Hierarchies are strictly bounded to L0 (context), L1 (subsystems), and L2 (components). Arbitrary nesting depths are not supported.
3. **Static Model**:
   Model editing directly within the web viewer is not supported; all updates must be made in the YAML files and regenerated.
