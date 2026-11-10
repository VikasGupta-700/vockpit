# The Vockpit Method: Boxes, Levels, and Drill-Down

## 1. The Core Idea

Software architecture documentation usually suffers from two failure modes: either it consists of hand-drawn diagrams that rapidly drift out of sync with reality, or it dissolves into raw source code where the forest is lost for the trees.

Vockpit treats system design as a **declarative data model**. You describe the functional components of a system ("boxes"), who talks to them ("actors"), and the data that flows between them ("edges") in minimal, version-controlled YAML files. Vockpit validates the model against rigorous structural rules and automatically builds interactive drill-down diagrams.

---

## 2. Boxes and the Three Levels

Vockpit enforces a strict hierarchy of exactly three abstraction levels:

1. **Level 0 (L0: Context)**:
   - Represents the entire system as a single black box.
   - Shows all external users and partner systems ("actors") and their connections to the system.
   - Answers: *What is the boundary of the system, and who interacts with it?*

2. **Level 1 (L1: System)**:
   - Decomposes the system into its primary subsystems (L1 boxes).
   - Shows data flows between subsystems, as well as the external actors that interact with them.
   - Answers: *What are the major parts of the system, and how do they coordinate?*

3. **Level 2 (L2: Subsystem Components)**:
   - Zooms into a specific L1 subsystem to show its internal components (L2 boxes).
   - Shows internal communication, plus external L1 subsystems that act as "neighbours" communicating with these components.
   - Answers: *How does this specific subsystem achieve its responsibilities?*

An L2 box cannot have child boxes. This boundary guarantees that diagrams remain concise, readable, and focused without infinite recursion.

---

## 3. Directed Edges

Edges represent the flow of named data, events, or requests between entities:
- Every edge has a sender (`from`), a recipient (`to`), and a payload description (`data`).
- Edges connect actors to boxes, or boxes to other boxes.
- Direct edges between two outside actors are prohibited, as are circular self-referencing loops and edges using the system ID.
- When multiple data payloads travel between the same two entities, Vockpit automatically merges them into a clean, semicolon-separated edge label.

---

## 4. Interactive Drill-Down

Rather than forcing the viewer to navigate dozens of disconnected pages, Vockpit renders an interactive single-page application:
- **Clicking an L1 box** zooms directly into its L2 internal diagram.
- **Clicking a leaf component** highlights it in context and displays its inspector details (inputs, outputs, who sends to it, and who it sends to).
- **Breadcrumbs and Zoom Out** (via UI button or the `Escape` key) allow instant, effortless traversal back up the abstraction stack.

---

## 5. Why Diagrams Are Generated, Never Hand-Edited

In Vockpit, diagrams are strictly downstream build artifacts:
- **Single Source of Truth**: The declarative YAML files in `model/` define the architecture. There are no canvas coordinates, visual layout tweaks, or diagram drift.
- **Continuous Validation**: Rules C01 (schema), C02 (identity), C03 (edges), C10 (freshness), and C26 (size) ensure that every model is mathematically consistent and that generated diagrams are up to date.
- **AI Agent Friendly**: AI agents excel at reading and writing concise YAML data models from design briefs. Hand-editing graphic diagrams is brittle for humans and nearly impossible for agents.
- **Version Controlled**: Architecture diffs are visible directly in Git commits as readable text changes.
