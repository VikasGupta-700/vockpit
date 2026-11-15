from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from vockpit.registry import Actor, Box, Model, System


@dataclass
class DiagramNode:
    id: str
    title: str
    summary: str
    role: str  # system | inner | person | external | neighbour
    link: str  # #/<id> or ""


@dataclass
class DiagramEdge:
    from_id: str
    to_id: str
    label: str


@dataclass
class Diagram:
    name: str
    title: str
    nodes: list[DiagramNode]
    edges: list[DiagramEdge]


def _merge_edges(raw_edges: list[tuple[str, str, str]]) -> list[DiagramEdge]:
    grouped: dict[tuple[str, str], set[str]] = defaultdict(set)
    for f, t, data in raw_edges:
        grouped[(f, t)].add(data)

    merged: list[DiagramEdge] = []
    for f, t in sorted(grouped.keys()):
        distinct_data = sorted(grouped[(f, t)])
        label = "; ".join(distinct_data)
        merged.append(DiagramEdge(from_id=f, to_id=t, label=label))
    return merged


def build(model: Model) -> list[Diagram]:
    diagrams: list[Diagram] = []

    actor_map: dict[str, Actor] = {a.id: a for a in model.actors}
    box_map: dict[str, Box] = {b.id: b for b in model.boxes}
    actor_ids = set(actor_map.keys())
    box_ids = set(box_map.keys())

    # 1. L0_context
    l0_nodes: list[DiagramNode] = [
        DiagramNode(
            id=model.system.id,
            title=model.system.title,
            summary=model.system.summary,
            role="system",
            link=f"#/{model.system.id}",
        )
    ]
    for a in model.actors:
        l0_nodes.append(
            DiagramNode(
                id=a.id,
                title=a.title,
                summary=a.summary,
                role=a.kind,
                link="",
            )
        )

    l0_raw_edges: list[tuple[str, str, str]] = []
    for e in model.edges:
        if e.from_id in actor_ids and e.to_id in box_ids:
            l0_raw_edges.append((e.from_id, model.system.id, e.data))
        elif e.from_id in box_ids and e.to_id in actor_ids:
            l0_raw_edges.append((model.system.id, e.to_id, e.data))

    diagrams.append(
        Diagram(
            name="L0_context",
            title=f"L0: {model.system.title}",
            nodes=l0_nodes,
            edges=_merge_edges(l0_raw_edges),
        )
    )

    # Helper for L1 and L2 representative resolution
    def get_rep(x_id: str, focus: System | Box) -> tuple[Any, str] | None:
        # returns (item, role)
        if x_id in actor_map:
            act = actor_map[x_id]
            return act, act.kind

        if isinstance(focus, System):
            # Focus is the system. Children of F are L1 boxes.
            if x_id in box_map:
                box = box_map[x_id]
                if box.level == 1:
                    return box, "inner"
                elif box.level == 2:
                    # grandchild -> L1 parent is inner
                    l1_parent = box_map[box.parent]
                    return l1_parent, "inner"
            return None

        # Focus is an L1 box
        if x_id in box_map:
            box = box_map[x_id]
            if box.parent == focus.id:
                # child of F
                return box, "inner"
            if box.id == focus.id:
                # F itself: not an inner node, not outside F
                return focus, "focus"
            # outside F: the L1 box that is x or contains x
            l1_box = box if box.level == 1 else box_map[box.parent]
            return l1_box, "neighbour"

        return None

    # 2. L1_system
    l1_focus = model.system
    l1_inner_boxes = [b for b in model.boxes if b.level == 1]
    l1_nodes: list[DiagramNode] = [
        DiagramNode(
            id=b.id,
            title=b.title,
            summary=b.summary,
            role="inner",
            link=f"#/{b.id}",
        )
        for b in l1_inner_boxes
    ]

    l1_raw_edges: list[tuple[str, str, str]] = []
    l1_non_inner: dict[str, tuple[Any, str]] = {}

    for e in model.edges:
        rep_from_info = get_rep(e.from_id, l1_focus)
        rep_to_info = get_rep(e.to_id, l1_focus)
        if not rep_from_info or not rep_to_info:
            continue
        rep_from, role_from = rep_from_info
        rep_to, role_to = rep_to_info

        if (role_from == "inner" or role_to == "inner") and rep_from.id != rep_to.id:
            l1_raw_edges.append((rep_from.id, rep_to.id, e.data))
            if role_from != "inner":
                l1_non_inner[rep_from.id] = (rep_from, role_from)
            if role_to != "inner":
                l1_non_inner[rep_to.id] = (rep_to, role_to)

    for nid in sorted(l1_non_inner.keys()):
        item, role = l1_non_inner[nid]
        link = f"#/{item.id}" if role == "neighbour" else ""
        l1_nodes.append(
            DiagramNode(
                id=item.id,
                title=item.title,
                summary=item.summary,
                role=role,
                link=link,
            )
        )

    diagrams.append(
        Diagram(
            name="L1_system",
            title=f"L1: {model.system.title}",
            nodes=l1_nodes,
            edges=_merge_edges(l1_raw_edges),
        )
    )

    # 3. L2_<id> for each L1 box with children
    for l1_box in l1_inner_boxes:
        if not l1_box.children:
            continue

        l2_focus = l1_box
        l2_inner_boxes = [box_map[cid] for cid in l1_box.children]
        l2_nodes: list[DiagramNode] = [
            DiagramNode(
                id=b.id,
                title=b.title,
                summary=b.summary,
                role="inner",
                link=f"#/{b.id}",
            )
            for b in l2_inner_boxes
        ]

        l2_raw_edges: list[tuple[str, str, str]] = []
        l2_non_inner: dict[str, tuple[Any, str]] = {}

        for e in model.edges:
            rep_from_info = get_rep(e.from_id, l2_focus)
            rep_to_info = get_rep(e.to_id, l2_focus)
            if not rep_from_info or not rep_to_info:
                continue
            rep_from, role_from = rep_from_info
            rep_to, role_to = rep_to_info

            if (role_from == "inner" or role_to == "inner") and rep_from.id != rep_to.id:
                l2_raw_edges.append((rep_from.id, rep_to.id, e.data))
                if role_from != "inner":
                    l2_non_inner[rep_from.id] = (rep_from, role_from)
                if role_to != "inner":
                    l2_non_inner[rep_to.id] = (rep_to, role_to)

        for nid in sorted(l2_non_inner.keys()):
            item, role = l2_non_inner[nid]
            link = f"#/{item.id}" if role == "neighbour" else ""
            l2_nodes.append(
                DiagramNode(
                    id=item.id,
                    title=item.title,
                    summary=item.summary,
                    role=role,
                    link=link,
                )
            )

        diagrams.append(
            Diagram(
                name=f"L2_{l1_box.id}",
                title=f"L2: {l1_box.title}",
                nodes=l2_nodes,
                edges=_merge_edges(l2_raw_edges),
            )
        )

    return diagrams
