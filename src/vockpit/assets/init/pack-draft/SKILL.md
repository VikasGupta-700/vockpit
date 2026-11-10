---
name: pack-draft
description: Turn brief.md into a Vockpit model (model/system.yaml and model/boxes/*.yaml) and generate the drill-down diagrams. Use when the user asks to draft, model or diagram a system from a brief.
---

# Draft the model from the brief

1. Read `brief.md`. If it is empty, ask the user to describe the system and stop.
2. Write `model/system.yaml`:
   - `system`: one id, title and one-sentence summary.
   - `actors`: each kind of user (`kind: person`) and each outside system (`kind: external`).
   - `boxes`: three to seven subsystems (L1). Each needs an id, title and one-sentence summary.
   - `edges`: what passes between actors and boxes, and between boxes. `data` names the thing passed.
3. For each L1 box with real internal structure, write `model/boxes/<l1-id>.yaml` with `parent`, two to seven
   L2 boxes, and the edges between them. An edge may also connect to a box in another file.
4. IDs are lowercase words joined by hyphens, unique across all files.
5. Run `vockpit check`. Fix every ERROR and run it again until it prints OK.
6. Run `vockpit generate`.
7. Write no code and no other files.
8. Tell the user:
   - the boxes you created, level by level;
   - every assumption you made that the brief did not state;
   - every question the brief left open;
   - that they can run `vockpit view` to review the result.
