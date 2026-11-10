from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from vockpit import __version__
from vockpit.diagrams import Diagram
from vockpit.registry import Model


def build_model_js(model: Model, diagrams_list: list[Diagram]) -> str:
    nodes: dict[str, Any] = {}

    # System node
    l1_child_ids = [b.id for b in model.boxes if b.level == 1]
    nodes[model.system.id] = {
        "id": model.system.id,
        "kind": "system",
        "title": model.system.title,
        "summary": model.system.summary,
        "level": 0,
        "parent": None,
        "children": l1_child_ids,
        "inputs": [],
        "outputs": [],
        "diagram": "L1_system",
    }

    # Actor nodes
    for a in model.actors:
        nodes[a.id] = {
            "id": a.id,
            "kind": a.kind,
            "title": a.title,
            "summary": a.summary,
            "level": None,
            "parent": None,
            "children": [],
            "inputs": [],
            "outputs": [],
            "diagram": "L0_context",
        }

    # Box nodes
    for b in model.boxes:
        if b.children:
            diagram_name = f"L2_{b.id}"
        else:
            if b.level == 1:
                diagram_name = "L1_system"
            else:
                diagram_name = f"L2_{b.parent}"

        nodes[b.id] = {
            "id": b.id,
            "kind": "box",
            "title": b.title,
            "summary": b.summary,
            "level": b.level,
            "parent": b.parent,
            "children": list(b.children),
            "inputs": list(b.inputs),
            "outputs": list(b.outputs),
            "diagram": diagram_name,
        }

    edges: list[dict[str, str]] = [
        {"from": e.from_id, "to": e.to_id, "data": e.data}
        for e in model.edges
    ]

    diagrams_meta: dict[str, dict[str, str]] = {
        d.name: {"title": d.title} for d in diagrams_list
    }

    data = {
        "version": 1,
        "generator": f"vockpit {__version__}",
        "system": model.system.id,
        "nodes": nodes,
        "edges": edges,
        "diagrams": diagrams_meta,
    }

    json_str = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)
    return f"window.VOCKPIT_MODEL = {json_str};\n"


def build_diagrams_js(svg_map: dict[str, str] | None = None) -> str:
    if not svg_map:
        return "window.VOCKPIT_SVG = {};\n"
    json_str = json.dumps(svg_map, indent=2, sort_keys=True, ensure_ascii=False)
    return f"window.VOCKPIT_SVG = {json_str};\n"


def write_viewer_data(
    viewer_dir: Path,
    model: Model,
    diagrams_list: list[Diagram],
    svg_map: dict[str, str] | None = None,
) -> None:
    viewer_dir.mkdir(parents=True, exist_ok=True)
    model_js_path = viewer_dir / "model.js"
    diagrams_js_path = viewer_dir / "diagrams.js"

    model_js_path.write_text(build_model_js(model, diagrams_list), encoding="utf-8")
    diagrams_js_path.write_text(build_diagrams_js(svg_map), encoding="utf-8")
