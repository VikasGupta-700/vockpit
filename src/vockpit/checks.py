from __future__ import annotations

from pathlib import Path
from typing import Sequence
import yaml

from vockpit.findings import Finding
from vockpit import registry
from vockpit.registry import Model


def check_c01(root: Path | str) -> list[Finding]:
    return registry.validate_c01(Path(root))


def check_c02(root: Path | str, model: Model) -> list[Finding]:
    findings: list[Finding] = []
    root = Path(root).resolve()
    id_sources: dict[str, str] = {}

    # System ID
    sys_source = "model/system.yaml"
    id_sources[model.system.id] = sys_source

    # Actors
    for a in model.actors:
        if a.id in id_sources:
            findings.append(
                Finding("C02", "ERROR", sys_source, f"duplicate id '{a.id}' (also in {id_sources[a.id]})")
            )
        else:
            id_sources[a.id] = sys_source

    # L1 boxes
    l1_ids: set[str] = set()
    for b in model.boxes:
        if b.level == 1:
            if b.id in id_sources:
                findings.append(
                    Finding("C02", "ERROR", sys_source, f"duplicate id '{b.id}' (also in {id_sources[b.id]})")
                )
            else:
                id_sources[b.id] = sys_source
                l1_ids.add(b.id)

    # Box files in model/boxes/
    boxes_dir = root / "model" / "boxes"
    if boxes_dir.is_dir():
        box_files = sorted(boxes_dir.glob("*.yaml"), key=lambda p: p.name)
        for bf in box_files:
            rel_source = f"model/boxes/{bf.name}"
            try:
                with open(bf, "r", encoding="utf-8") as f:
                    b_data = yaml.safe_load(f)
            except Exception:
                continue

            if not isinstance(b_data, dict):
                continue

            parent_id = b_data.get("parent")
            if isinstance(parent_id, str):
                if parent_id not in l1_ids:
                    findings.append(
                        Finding("C02", "ERROR", rel_source, f"parent '{parent_id}' is not an L1 box")
                    )

            # L2 boxes
            l2_boxes = b_data.get("boxes", [])
            if isinstance(l2_boxes, list):
                for b in l2_boxes:
                    if isinstance(b, dict) and "id" in b and isinstance(b["id"], str):
                        b_id = b["id"]
                        if b_id in id_sources:
                            findings.append(
                                Finding("C02", "ERROR", rel_source, f"duplicate id '{b_id}' (also in {id_sources[b_id]})")
                            )
                        else:
                            id_sources[b_id] = rel_source

    return findings


def check_c03(model: Model) -> list[Finding]:
    findings: list[Finding] = []
    actor_ids = {a.id for a in model.actors}
    box_ids = {b.id for b in model.boxes}
    valid_endpoints = actor_ids | box_ids
    sys_id = model.system.id

    for edge in model.edges:
        from_id = edge.from_id
        to_id = edge.to_id
        src = edge.source

        from_valid = True
        to_valid = True

        if from_id == sys_id:
            findings.append(Finding("C03", "ERROR", src, f"edge from '{from_id}' uses system id"))
            from_valid = False
        elif from_id not in valid_endpoints:
            findings.append(Finding("C03", "ERROR", src, f"unknown edge from '{from_id}'"))
            from_valid = False

        if to_id == sys_id:
            findings.append(Finding("C03", "ERROR", src, f"edge to '{to_id}' uses system id"))
            to_valid = False
        elif to_id not in valid_endpoints:
            findings.append(Finding("C03", "ERROR", src, f"unknown edge to '{to_id}'"))
            to_valid = False

        if from_valid and to_valid:
            if from_id == to_id:
                findings.append(Finding("C03", "ERROR", src, f"self-referencing edge '{from_id}' -> '{to_id}'"))
            elif from_id in actor_ids and to_id in actor_ids:
                findings.append(Finding("C03", "ERROR", src, f"edge between two actors '{from_id}' and '{to_id}'"))

    return findings


def run_model_checks(root: Path | str) -> list[Finding]:
    root = Path(root).resolve()
    # Step 1: C01
    c01_findings = check_c01(root)
    if any(f.severity == "ERROR" for f in c01_findings):
        return c01_findings

    model, _ = registry.load(root)
    if model is None:
        return c01_findings

    # Step 2: C02 & C03
    c02_findings = check_c02(root, model)
    c03_findings = check_c03(model)
    return c02_findings + c03_findings
