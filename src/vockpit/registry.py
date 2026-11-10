from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Any
import yaml

from vockpit.findings import Finding

ID_PATTERN = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")


@dataclass
class System:
    id: str
    title: str
    summary: str


@dataclass
class Actor:
    id: str
    title: str
    kind: str
    summary: str = ""


@dataclass
class Box:
    id: str
    title: str
    summary: str
    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    parent: str = ""
    level: int = 1
    children: list[str] = field(default_factory=list)
    source: str = ""


@dataclass
class Edge:
    from_id: str
    to_id: str
    data: str
    source: str = ""

    @property
    def to(self) -> str:
        return self.to_id

    @property
    def from_(self) -> str:
        return self.from_id


@dataclass
class Model:
    system: System
    actors: list[Actor] = field(default_factory=list)
    boxes: list[Box] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)

    def get_box(self, box_id: str) -> Box | None:
        for b in self.boxes:
            if b.id == box_id:
                return b
        return None

    def get_actor(self, actor_id: str) -> Actor | None:
        for a in self.actors:
            if a.id == actor_id:
                return a
        return None


def validate_c01(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    root = Path(root)
    sys_file = root / "model" / "system.yaml"
    rel_sys_file = "model/system.yaml"

    if not sys_file.is_file():
        findings.append(
            Finding("C01", "ERROR", rel_sys_file, "file does not exist")
        )
        return findings

    try:
        with open(sys_file, "r", encoding="utf-8") as f:
            sys_data = yaml.safe_load(f)
    except Exception as e:
        findings.append(Finding("C01", "ERROR", rel_sys_file, f"invalid YAML: {e}"))
        return findings

    if not isinstance(sys_data, dict):
        findings.append(Finding("C01", "ERROR", rel_sys_file, "root must be a mapping"))
        return findings

    allowed_sys_keys = {"system", "actors", "boxes", "edges"}
    extra_keys = set(sys_data.keys()) - allowed_sys_keys
    for k in sorted(extra_keys):
        findings.append(Finding("C01", "ERROR", rel_sys_file, f"unexpected key '{k}'"))

    # system key
    if "system" not in sys_data:
        findings.append(Finding("C01", "ERROR", rel_sys_file, "missing required key 'system'"))
    elif not isinstance(sys_data["system"], dict):
        findings.append(Finding("C01", "ERROR", rel_sys_file, "key 'system' must be a mapping"))
    else:
        s_data = sys_data["system"]
        allowed_s_keys = {"id", "title", "summary"}
        for k in sorted(set(s_data.keys()) - allowed_s_keys):
            findings.append(Finding("C01", "ERROR", rel_sys_file, f"unexpected key in 'system': '{k}'"))
        for req in ["id", "title", "summary"]:
            if req not in s_data:
                findings.append(Finding("C01", "ERROR", rel_sys_file, f"system missing required key '{req}'"))
            elif not isinstance(s_data[req], str):
                findings.append(Finding("C01", "ERROR", rel_sys_file, f"system '{req}' must be a string"))
            elif req == "id" and not ID_PATTERN.match(s_data[req]):
                findings.append(Finding("C01", "ERROR", rel_sys_file, f"invalid system id '{s_data[req]}'"))

    # actors key (optional list)
    if "actors" in sys_data:
        actors_data = sys_data["actors"]
        if not isinstance(actors_data, list):
            findings.append(Finding("C01", "ERROR", rel_sys_file, "'actors' must be a list"))
        else:
            allowed_actor_keys = {"id", "title", "kind", "summary"}
            for idx, actor in enumerate(actors_data):
                if not isinstance(actor, dict):
                    findings.append(Finding("C01", "ERROR", rel_sys_file, f"actors[{idx}] must be a mapping"))
                    continue
                for k in sorted(set(actor.keys()) - allowed_actor_keys):
                    findings.append(Finding("C01", "ERROR", rel_sys_file, f"unexpected key in actor: '{k}'"))
                for req in ["id", "title", "kind"]:
                    if req not in actor:
                        findings.append(Finding("C01", "ERROR", rel_sys_file, f"actor missing required key '{req}'"))
                    elif not isinstance(actor[req], str):
                        findings.append(Finding("C01", "ERROR", rel_sys_file, f"actor '{req}' must be a string"))
                    elif req == "id" and not ID_PATTERN.match(actor[req]):
                        findings.append(Finding("C01", "ERROR", rel_sys_file, f"invalid actor id '{actor[req]}'"))
                    elif req == "kind" and actor[req] not in ("person", "external"):
                        findings.append(Finding("C01", "ERROR", rel_sys_file, f"actor kind must be 'person' or 'external', got '{actor[req]}'"))
                if "summary" in actor and not isinstance(actor["summary"], str):
                    findings.append(Finding("C01", "ERROR", rel_sys_file, "actor 'summary' must be a string"))

    # boxes key (required, at least one)
    if "boxes" not in sys_data:
        findings.append(Finding("C01", "ERROR", rel_sys_file, "missing required key 'boxes'"))
    elif not isinstance(sys_data["boxes"], list):
        findings.append(Finding("C01", "ERROR", rel_sys_file, "'boxes' must be a list"))
    elif len(sys_data["boxes"]) == 0:
        findings.append(Finding("C01", "ERROR", rel_sys_file, "'boxes' list must have at least one entry"))
    else:
        _validate_boxes(sys_data["boxes"], rel_sys_file, findings)

    # edges key (optional list)
    if "edges" in sys_data:
        edges_data = sys_data["edges"]
        if not isinstance(edges_data, list):
            findings.append(Finding("C01", "ERROR", rel_sys_file, "'edges' must be a list"))
        else:
            _validate_edges(edges_data, rel_sys_file, findings)

    # Validate box files in model/boxes/
    boxes_dir = root / "model" / "boxes"
    if boxes_dir.is_dir():
        box_files = sorted(boxes_dir.glob("*.yaml"), key=lambda p: p.name)
        for bf in box_files:
            rel_bf = f"model/boxes/{bf.name}"
            try:
                with open(bf, "r", encoding="utf-8") as f:
                    b_data = yaml.safe_load(f)
            except Exception as e:
                findings.append(Finding("C01", "ERROR", rel_bf, f"invalid YAML: {e}"))
                continue

            if not isinstance(b_data, dict):
                findings.append(Finding("C01", "ERROR", rel_bf, "root must be a mapping"))
                continue

            allowed_b_file_keys = {"parent", "boxes", "edges"}
            for k in sorted(set(b_data.keys()) - allowed_b_file_keys):
                findings.append(Finding("C01", "ERROR", rel_bf, f"unexpected key '{k}'"))

            expected_parent = bf.stem
            if "parent" not in b_data:
                findings.append(Finding("C01", "ERROR", rel_bf, "missing required key 'parent'"))
            elif not isinstance(b_data["parent"], str):
                findings.append(Finding("C01", "ERROR", rel_bf, "'parent' must be a string"))
            elif b_data["parent"] != expected_parent:
                findings.append(Finding("C01", "ERROR", rel_bf, f"parent '{b_data['parent']}' differs from file name '{expected_parent}'"))

            if "boxes" not in b_data:
                findings.append(Finding("C01", "ERROR", rel_bf, "missing required key 'boxes'"))
            elif not isinstance(b_data["boxes"], list):
                findings.append(Finding("C01", "ERROR", rel_bf, "'boxes' must be a list"))
            elif len(b_data["boxes"]) == 0:
                findings.append(Finding("C01", "ERROR", rel_bf, "'boxes' list must have at least one entry"))
            else:
                _validate_boxes(b_data["boxes"], rel_bf, findings)

            if "edges" in b_data:
                if not isinstance(b_data["edges"], list):
                    findings.append(Finding("C01", "ERROR", rel_bf, "'edges' must be a list"))
                else:
                    _validate_edges(b_data["edges"], rel_bf, findings)

    return findings


def _validate_boxes(boxes: list[Any], loc: str, findings: list[Finding]) -> None:
    allowed_keys = {"id", "title", "summary", "inputs", "outputs"}
    for idx, b in enumerate(boxes):
        if not isinstance(b, dict):
            findings.append(Finding("C01", "ERROR", loc, f"boxes[{idx}] must be a mapping"))
            continue
        for k in sorted(set(b.keys()) - allowed_keys):
            findings.append(Finding("C01", "ERROR", loc, f"unexpected key in box: '{k}'"))
        for req in ["id", "title", "summary"]:
            if req not in b:
                findings.append(Finding("C01", "ERROR", loc, f"box missing required key '{req}'"))
            elif not isinstance(b[req], str):
                findings.append(Finding("C01", "ERROR", loc, f"box '{req}' must be a string"))
            elif req == "id" and not ID_PATTERN.match(b[req]):
                findings.append(Finding("C01", "ERROR", loc, f"invalid box id '{b[req]}'"))

        for list_key in ["inputs", "outputs"]:
            if list_key in b:
                val = b[list_key]
                if not isinstance(val, list) or not all(isinstance(x, str) for x in val):
                    findings.append(Finding("C01", "ERROR", loc, f"box '{list_key}' must be a list of strings"))


def _validate_edges(edges: list[Any], loc: str, findings: list[Finding]) -> None:
    allowed_keys = {"from", "to", "data"}
    for idx, e in enumerate(edges):
        if not isinstance(e, dict):
            findings.append(Finding("C01", "ERROR", loc, f"edges[{idx}] must be a mapping"))
            continue
        for k in sorted(set(e.keys()) - allowed_keys):
            findings.append(Finding("C01", "ERROR", loc, f"unexpected key in edge: '{k}'"))
        for req in ["from", "to", "data"]:
            if req not in e:
                findings.append(Finding("C01", "ERROR", loc, f"edge missing required key '{req}'"))
            elif not isinstance(e[req], str) or not e[req].strip():
                findings.append(Finding("C01", "ERROR", loc, f"edge '{req}' must be a non-empty string"))


def load(root: Path | str) -> tuple[Model | None, list[Finding]]:
    root = Path(root).resolve()
    c01_findings = validate_c01(root)
    if any(f.severity == "ERROR" for f in c01_findings):
        return None, c01_findings

    sys_file = root / "model" / "system.yaml"
    with open(sys_file, "r", encoding="utf-8") as f:
        sys_data = yaml.safe_load(f)

    sys_obj = System(
        id=sys_data["system"]["id"],
        title=sys_data["system"]["title"],
        summary=sys_data["system"]["summary"],
    )

    actors: list[Actor] = []
    if "actors" in sys_data and isinstance(sys_data["actors"], list):
        for a in sys_data["actors"]:
            actors.append(
                Actor(
                    id=a["id"],
                    title=a["title"],
                    kind=a["kind"],
                    summary=a.get("summary", ""),
                )
            )

    boxes: list[Box] = []
    l1_boxes: list[Box] = []
    for b in sys_data.get("boxes", []):
        box = Box(
            id=b["id"],
            title=b["title"],
            summary=b["summary"],
            inputs=list(b.get("inputs") or []),
            outputs=list(b.get("outputs") or []),
            parent=sys_obj.id,
            level=1,
            children=[],
            source="model/system.yaml",
        )
        boxes.append(box)
        l1_boxes.append(box)

    edges: list[Edge] = []
    for e in sys_data.get("edges", []):
        edges.append(
            Edge(
                from_id=e["from"],
                to_id=e["to"],
                data=e["data"],
                source="model/system.yaml",
            )
        )

    # Box files in model/boxes/
    boxes_dir = root / "model" / "boxes"
    if boxes_dir.is_dir():
        box_files = sorted(boxes_dir.glob("*.yaml"), key=lambda p: p.name)
        for bf in box_files:
            rel_path = f"model/boxes/{bf.name}"
            with open(bf, "r", encoding="utf-8") as f:
                b_data = yaml.safe_load(f)
            parent_id = b_data.get("parent")
            for b in b_data.get("boxes", []):
                child_box = Box(
                    id=b["id"],
                    title=b["title"],
                    summary=b["summary"],
                    inputs=list(b.get("inputs") or []),
                    outputs=list(b.get("outputs") or []),
                    parent=parent_id,
                    level=2,
                    children=[],
                    source=rel_path,
                )
                boxes.append(child_box)
                # Register as child of parent L1 box if found
                for l1 in l1_boxes:
                    if l1.id == parent_id:
                        l1.children.append(child_box.id)

            for e in b_data.get("edges", []):
                edges.append(
                    Edge(
                        from_id=e["from"],
                        to_id=e["to"],
                        data=e["data"],
                        source=rel_path,
                    )
                )

    model = Model(
        system=sys_obj,
        actors=actors,
        boxes=boxes,
        edges=edges,
    )
    return model, c01_findings
