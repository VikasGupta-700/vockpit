# Vockpit — Fable Plan (Draft 2)

**Vockpit: the Vibe Coding Cockpit.** *You steer. AI builds.*

Vockpit lets a person do effective vibe coding by steering only what matters for a good system (its structure, flows, data, screens and decisions) while AI agents handle the detail.

| | |
|---|---|
| **Date** | 2026-11-10 |
| **Status** | Draft 2, awaiting review. Nothing in this plan has been built yet. |
| **Supersedes** | `plan.md` (kept unchanged for reference). Draft 1 is kept as `fable-plan.draft1.md`. |
| **Workspace** | `C:\dev\2026-Nov-10-Vibe-Coding-Cockpit` |

### What changed in Draft 2

Draft 1 described one hierarchy: boxes of functionality. Draft 2 adds the other things a person needs to see in order to understand a system, and the order in which they are produced.

| Addition | Where |
|---|---|
| Views beside the box hierarchy: process flow, data (tables), UI (screens and navigation), technology (database, cache, queues, streams), layers (model, view, controller), AI handoff, agent harness | Section 24 |
| Contextual drill-down: at any point only the diagrams linked to the current focus are shown | Section 24 |
| Stages: brief, diagram pack, vetting, "now build this", specifications, build | Section 25 |
| Technology components and layer wiring | Section 26 |
| AI handoff diagram | Section 27 |
| Rules, skills, hooks and context files created at project start and shown in a diagram | Section 28 |
| Reuse and upgrade of `C:\dev\tools\template-harness` | Section 29 |
| Use of Google's Elephant-Goldfish Model (EGM) plugin for the design stages | Section 30 |
| Delivery in small public releases, each followed by use and feedback. **Section 31 sets the order of work and takes precedence over section 19.** | Section 31 |
| Name: Vockpit, with the tagline "You steer. AI builds." | Title |
| Build specification for release 0.1, for the building agent | Section 32 and `docs/designs/0.1-build-spec.md` |
| Smaller edits to match | Sections 1, 3, 4, 6, 8, 9, 11, 12, 15, 17, 19, 22, 23 |

---

## 1. Goal

Build a development system in which software is designed, built, tested and debugged **one diagram box at a time**, and in which any problem can be traced to the exact box, at the exact diagram level, where it lives.

Vockpit is a method plus a small toolset. It is meant to be dropped into any project and used by any developer or AI coding agent.

### What it must do

1. Describe a system as a hierarchy of boxes: a high-level scaffold, broken down level by level.
2. Tie every box to a specification, the code that implements it, and the tests that prove it.
3. Let a developer build one box, test that box alone, then integrate it with its neighbours.
4. Given a failing test, a stack trace, or a file and line, say which box is at fault and show its path through the levels.
5. Refuse to pass when a diagram, a spec, the code and the tests disagree.
6. Show the system from every angle a reader needs: logic, process flow, data tables, screens and navigation, technology components, layers, and who (human or AI agent) does what.
7. Show only what matters at the current point. Drilling into a box brings up the flows, tables, screens and components linked to that box, and nothing else.
8. Produce the full set of diagrams from the initial brief, before any detailed specification or code is written, so the design can be vetted as pictures.
9. Turn a vetted part of the diagrams into detailed specifications when the human says "now build this".
10. Set up every new project with the rules, skills, hooks and context files the method needs, and show them in a diagram.

### What it is not

The earlier `plan.md` described a runtime control panel for AI workloads (model routing, quota throttling, content safety, immutable audit storage). Those are features of an AI application, not of a development method. They are out of scope. See section 20.

---

## 2. The problem this plan is built around

The earlier projects already have diagrams, code links and "verified" reports. A check on 2026-11-10 showed the links are not enforced:

| Finding | Location |
|---|---|
| 0 of 71 catalogued line anchors point at their marker. 45 are off by up to 3 lines, 24 are off by 8 to 116 lines, 2 have no marker. | `2026-Oct-11-AI-103/labs/video_command_catalog.json` |
| The verifier prints a hardcoded `PASSED & VERIFIED` and never checks an anchor. | `2026-Oct-11-AI-103/labs/verify_video_traceability.py` line 68 |
| Rendered SVG diagrams have no `.d2` source, so they cannot be regenerated. | `2026-Oct-11-AI-103/docs/diagrams/` |
| The interactive studio holds hand-typed node data that points to `src/service.py`, while the D2 diagram points to `src/greeting_service.py`. Node IDs differ between the two. | `HelloWorld-SDD/docs/diagrams/` |
| The compliance audit only checks that files exist. | `HelloWorld-SDD/tests/test_harness_audit.py` |
| The secret-safety hook is a no-op. The rules require a `design.md` that does not exist. The folder is not under version control. | `HelloWorld-SDD/.agent/` |

Links that are typed by hand and never checked go stale without anyone noticing. Every design choice below follows from fixing that.

---

## 3. Principles

1. **One identity per box.** Each box has a stable ID. That ID appears in the registry, the diagram, the spec, the code and the tests.
2. **One source of truth.** Boxes are declared once, in the registry. Diagrams and viewer data are generated from it and never edited by hand.
3. **Symbols, not line numbers.** Code is referenced by module and function or class name, resolved by parsing the code. Line numbers are computed when needed, never stored.
4. **A check that can fail.** Every rule in this plan has an automated check. A report may only say "verified" when a check actually ran and passed.
5. **Small boxes.** A leaf box is one unit of behaviour that can be specified on one page and tested alone.
6. **Spec before code.** No box is implemented without a written spec and an open change.
7. **Reuse before rebuild.** Existing viewer, templates, rules and spec layout are carried over (section 5).
8. **Small releases, used and published.** Vockpit is built as a series of small releases. Each one is used on a real project, published on GitHub, and announced, and the feedback decides what the next release contains (section 31). This replaces Draft 1's "prove before packaging".
9. **Diagrams before specs, specs before code.** The diagram pack is drafted and vetted first. Detailed specs are written only for the part the human has asked to build.
10. **Show only what the focus needs.** A diagram is always drawn for one focus (a box, a table, a screen, a flow). Unrelated items are left out, not greyed out.
11. **One box, many views.** Flows, tables, screens and technology components are not separate documents. Each one is linked to the boxes that use it, and the links are checked.

---

## 4. Concepts

| Term | Meaning |
|---|---|
| **Box** | A unit of the system with a stable ID, a level and a parent. |
| **Level** | L0 Context (the system and what surrounds it). L1 Subsystem. L2 Component (a function, class or small module). A box with no children is a **leaf**. |
| **Edge** | A directed connection between two boxes carrying named data. Every edge between leaf boxes needs an integration test. |
| **Registry** | The YAML files in `model/` that declare all boxes and edges. |
| **Spec** | The behaviour a box must have: requirements in RFC 2119 wording, scenarios in Given/When/Then form. |
| **Change** | A numbered workspace holding the proposal, design, spec changes and task list for one piece of work. |
| **ADR** | Architecture Decision Record: one file per significant decision. |
| **Status** | Where a box is in its lifecycle (section 9). Computed by the tools, not typed by hand. |
| **View** | One way of looking at the system: structure, flow, data, UI, technology, layer, handoff, harness (section 24). |
| **Focus** | The single item the viewer is currently centred on. It decides which diagrams are shown. |
| **Entity** | A stored table: columns, keys and relations. Entities are grouped into **data domains**. |
| **Screen** | One UI screen: its elements, the actions a user can take, and where each action leads. Screens are grouped into **areas**. |
| **Flow** | An ordered list of steps across boxes for one use case. Drawn as a sequence or process diagram. |
| **Technology component** | A runtime part that is not application code: a database, cache, message queue, event stream, object store or external service. |
| **Layer** | The role a box plays: view, controller, model, repository or integration (section 26). |
| **Brief** | The initial free-text specification the human gives at the start (`brief.md`). |
| **Diagram pack** | The complete set of generated diagrams for every view, produced from the brief. |
| **Vetted** | A box, entity, screen or flow that the human has approved in its current form. |
| **Harness** | The rules, skills, hooks and context files that steer AI agents in a project. |

---

## 5. What is reused

| Existing asset | Source | Action |
|---|---|---|
| Pan/zoom viewer with inspector drawer and inline SVG | `2026-Oct-11-AI-103/docs/templates/interactive_architecture_viewer_template.html` | Copy. Change it to load generated JSON instead of hand-typed node data. |
| Level 0/1/2 diagram convention and D2 styling | `HelloWorld-SDD/docs/diagrams/*.d2` | Keep the convention. Use the files as the visual target for the generator. |
| Spec layout: `openspec/specs/`, `openspec/changes/NNN-name/` | `HelloWorld-SDD/openspec/` | Copy the layout and `config.yaml`. |
| Agent rules: spec lifecycle, diagram standards, logging | `HelloWorld-SDD/.agent/rules/` | Copy and revise to match this plan. |
| `@dfd-change` prompt card (click a node, get a prompt for the agent) | `HelloWorld-SDD` studio and rules | Keep. Rename to `@box-change` and generate the card from registry data. |
| Decision gate spec template | `2026-Oct-11-AI-103/docs/templates/decision_gate_specification_template.md` | Copy as an optional spec section for boxes that are decision points. |
| Task board protocol (`goals/tasks.md`, `[x]` `[/]` `[ ]`) | `2026-Oct-11-AI-103/AGENTS.md` section 6 | Keep. |
| D2 command-line tool | Already installed at `C:\Users\vikas\bin\d2` | Use as is. |
| Elephant-Goldfish Model (EGM) plugin: brainstorm, draft, review and drift-report skills | `github.com/google/elephant-goldfish-model` (Apache 2.0) | Install as a plugin. Use for the design stages; do not rebuild what it does (section 30). |

---

## 6. Folder structure

```text
C:\dev\2026-Nov-10-Vibe-Coding-Cockpit\
├── README.md                     # What this is, quick start, link to the viewer
├── AGENTS.md                     # Project constitution for all AI agents (canonical)
├── CLAUDE.md                     # One line importing AGENTS.md, plus Claude-specific notes
├── CHANGELOG.md                  # Human-readable history, one entry per merged change
├── fable-plan.md                 # This plan
├── plan.md                       # Earlier plan, superseded
├── pyproject.toml                # Package metadata, dependencies, tool settings
├── .gitignore
├── .gitattributes                # Line endings; mark generated files
│
├── model/                        # THE REGISTRY (single source of truth)
│   ├── system.yaml               # L0 box, external actors, L1 boxes, L1 edges
│   ├── boxes/
│   │   └── <l1-box-id>.yaml      # One file per subsystem: its L2 boxes and edges
│   ├── data/
│   │   └── <domain>.yaml         # Tables of one data domain: columns, keys, relations
│   ├── ui/
│   │   └── <area>.yaml           # Screens of one area: elements, actions, navigation
│   ├── flows/
│   │   └── <flow-id>.yaml        # One use case as ordered steps across boxes
│   ├── tech.yaml                 # Databases, caches, queues, streams, external services
│   ├── handoff.yaml              # Stages, who acts in each, what is handed over
│   ├── harness.yaml              # Rules, skills, hooks, context files and their stage
│   └── review.yaml               # Vetting record, written by `vockpit approve`
│
├── openspec/                     # SPECIFICATIONS
│   ├── config.yaml               # Spec standards and validation switches
│   ├── specs/
│   │   └── <box-id>/
│   │       ├── spec.md           # Requirements and scenarios for the box
│   │       └── behaviour.d2      # Optional sequence or state diagram
│   └── changes/
│       ├── NNN-<slug>/           # Active change
│       │   ├── proposal.md       # Why, and what changes
│       │   ├── design.md         # How; links to ADRs
│       │   ├── tasks.md          # Ordered task list, one box per task
│       │   └── specs/<box-id>/spec.md   # Spec changes proposed by this change
│       └── archive/              # Completed changes
│
├── src/vockpit/                  # THE TOOL (built with its own method)
│   ├── __init__.py
│   ├── cli.py                    # Command entry point
│   ├── registry/                 # Load and validate model/*.yaml
│   ├── resolve/                  # Find code symbols and tests for a box
│   ├── check/                    # Consistency rules (section 12)
│   ├── generate/                 # Registry -> D2, SVG, viewer JSON, modules.md
│   ├── locate/                   # File, test or stack trace -> box path
│   ├── status/                   # Compute box lifecycle status
│   ├── scaffold/                 # init, new box, new change, new ADR
│   └── logging/                  # Structured logging helper
│
├── tests/
│   ├── unit/test_<box_id>.py     # One file per leaf box
│   ├── integration/test_<from>__<to>.py   # One file per edge
│   ├── e2e/                      # Whole-tool runs against fixtures
│   └── fixtures/
│       ├── good_project/         # A small project that must pass every check
│       └── broken_*/             # One project per rule, each must fail that rule
│
├── docs/
│   ├── architecture.md           # Narrative; diagram sections generated
│   ├── modules.md                # Generated from the registry
│   ├── user-guide.md             # How to use Vockpit on a project
│   ├── method.md                 # The box-by-box method, tool-independent
│   ├── diagrams/                 # GENERATED. Do not edit.
│   │   ├── L0_context.d2 / .svg
│   │   ├── L1_system.d2 / .svg
│   │   ├── L2_<l1-box-id>.d2 / .svg
│   │   ├── flow/<flow-id>.d2 / .svg         # Sequence diagram per flow
│   │   ├── data/<domain>.d2 / .svg          # ERD per data domain
│   │   ├── ui/navigation.d2 / .svg          # Screen-to-screen navigation map
│   │   ├── ui/<area>.d2 / .svg              # Navigation within one area
│   │   ├── tech/components.d2 / .svg        # Technology components and what uses them
│   │   ├── layer/<l1-box-id>.d2 / .svg      # View, controller, model, store wiring
│   │   ├── handoff.d2 / .svg                # Who does what, stage by stage
│   │   └── harness.d2 / .svg                # Rules, skills, hooks, context by stage
│   ├── viewer/
│   │   ├── index.html            # Interactive viewer
│   │   └── model.json            # GENERATED viewer data
│   └── decisions/
│       ├── README.md             # Index of decisions; when an ADR is required
│       ├── NNNN-<slug>.md        # One ADR per significant decision
│       └── log.md                # One-line entries for small decisions
│
├── templates/                    # Copied into other projects by `vockpit init`.
│   │                             # Seeded from C:\dev\tools\template-harness (section 29)
│   ├── brief.md.tmpl
│   ├── entity.yaml.tmpl
│   ├── screen.yaml.tmpl
│   ├── flow.yaml.tmpl
│   ├── tech.yaml.tmpl
│   ├── handoff.yaml.tmpl
│   ├── harness.yaml.tmpl
│   ├── AGENTS.md.tmpl
│   ├── spec.md.tmpl
│   ├── proposal.md.tmpl
│   ├── design.md.tmpl
│   ├── tasks.md.tmpl
│   ├── adr.md.tmpl
│   ├── decision_gate.md.tmpl
│   ├── box.yaml.tmpl
│   └── viewer.html.tmpl
│
├── goals/
│   └── tasks.md                  # Project-level task board
│
├── .agent/                       # Antigravity agent configuration
│   ├── rules/
│   │   ├── 01_spec_lifecycle.md
│   │   ├── 02_box_method.md
│   │   ├── 03_diagram_standards.md
│   │   ├── 04_logging.md
│   │   ├── 05_version_control.md
│   │   └── 06_decision_logging.md
│   └── hooks.json
│
├── .claude/                      # Claude Code configuration
│   ├── settings.json             # Hooks and permissions
│   └── skills/                   # Project skills (section 15)
│
├── .github/
│   ├── workflows/ci.yml          # Check, test, regenerate-and-compare
│   ├── pull_request_template.md
│   └── ISSUE_TEMPLATE/bug.md     # Requires a box ID or `vockpit locate` output
│
└── .vockpit/                     # Local working files, not committed
    ├── logs/                     # Structured run logs
    └── cache/
```

Folder rules:

- `model/` is the only place boxes are declared.
- `docs/diagrams/` and `docs/viewer/model.json` are generated. A check fails if they differ from a fresh generation.
- The rule text lives once, in `.agent/rules/`. `AGENTS.md` summarises and links to it. `CLAUDE.md` imports `AGENTS.md`.

---

## 7. The registry

### Box IDs

- Lowercase, hyphen-separated, unique across the project, for example `check-symbols`.
- Never changed once code refers to them. Renaming a box means changing its `title`, not its `id`.
- The parent is a field, so a box can move without changing its ID.

### Example

```yaml
# model/boxes/check.yaml
parent: check                     # the L1 box these belong to
boxes:
  - id: check-symbols
    title: Symbol existence check
    level: 2
    summary: Confirms every code symbol named in the registry exists.
    code:
      - vockpit.check.symbols:check_symbols     # module:function
    inputs:  [Registry, source tree]
    outputs: [list of Finding]
    decision_gate: false
edges:
  - from: registry-load
    to: check-symbols
    data: Registry
```

What is **not** in the registry, because it is derived by convention and checked:

| Item | Convention |
|---|---|
| Spec | `openspec/specs/<box-id>/spec.md` |
| Unit test | `tests/unit/test_<box_id>.py` |
| Integration test for an edge | `tests/integration/test_<from>__<to>.py` |
| Status | Computed (section 9) |
| Line numbers | Computed by parsing the code |

### Code marker

Each implementing function or class carries a decorator or comment naming its box:

```python
@box("check-symbols")
def check_symbols(registry, root): ...
```

The marker lets `vockpit locate` work from a line of code, and lets the logging helper tag log records. A check confirms the marker and the registry agree in both directions.

---

## 8. Diagram policy

| Diagram | When required | How produced | Where |
|---|---|---|---|
| L0 Context | Always | Generated | `docs/diagrams/L0_context.d2` |
| L1 System | Always | Generated | `docs/diagrams/L1_system.d2` |
| L2 Component, one per L1 box | Always | Generated | `docs/diagrams/L2_<id>.d2` |
| Process flow (sequence), one per flow | Every use case named in the brief | Generated from `model/flows/` | `docs/diagrams/flow/` |
| Data model (ERD), one per data domain | The system stores data | Generated from `model/data/` | `docs/diagrams/data/` |
| Table card, one per entity | Same | Rendered by the viewer from the registry | Viewer |
| UI navigation map | The system has screens | Generated from `model/ui/` | `docs/diagrams/ui/` |
| Screen wireframe, one per screen | Same | Rendered by the viewer from the screen's element list | Viewer |
| Technology component diagram | Always | Generated from `model/tech.yaml` | `docs/diagrams/tech/` |
| Layer diagram, one per L1 box | The box has more than one layer | Generated from box `layer` fields | `docs/diagrams/layer/` |
| AI handoff diagram | Always | Generated from `model/handoff.yaml` | `docs/diagrams/handoff.d2` |
| Harness diagram | Always | Generated from `model/harness.yaml` | `docs/diagrams/harness.d2` |
| State diagram (UML) | A box or entity has named states and transitions | Hand-written D2 | `openspec/specs/<box-id>/behaviour.d2` |
| Class or other UML diagram | Only when a reviewer asks for one and the views above do not answer the question | Hand-written D2 | Same |
| Decision gate table | `decision_gate: true` | Section in `spec.md` from template | Spec |

Rules:

- Draft 1 had sequence diagrams and ERDs written by hand. They are now generated, because they are required for every project and hand-written copies drift.
- D2 is used for all generated diagrams. It has built-in table shapes for ERDs and a sequence diagram shape, so one tool covers every view.
- Structure diagrams are never hand-edited. To change one, change the registry and regenerate.
- Hand-written behaviour diagrams must only name boxes that exist in the registry. This is checked.
- Every `.d2` source is committed. SVGs are committed too, so diagrams display on GitHub without tooling.
- In generated diagrams, each node links to the next level down, and its colour shows box status.
- Diagrams are not required for every process. A diagram nobody maintains is worse than none.

---

## 9. Box lifecycle

Status is computed from what exists and what passes. Nobody types it.

| Status | Condition | Colour |
|---|---|---|
| `proposed` | In the registry only | Grey |
| `vetted` | Approved by the human, and unchanged since approval (section 25) | White with solid border |
| `specified` | Spec exists with at least one requirement and one scenario | Blue |
| `stubbed` | Code symbol exists with the marker; unit test file exists | Purple |
| `red` | Unit tests exist and at least one fails | Red |
| `green` | All unit tests pass | Light green |
| `integrated` | Green, and every edge touching the box has a passing integration test | Dark green |
| `drifted` | Any consistency check fails for this box | Orange |

A parent's status is the lowest status among its children.

---

## 10. Spec-driven constraints

1. **No code without a change.** Work starts by creating `openspec/changes/NNN-<slug>/` with `proposal.md`, `design.md`, `tasks.md` and the proposed spec changes.
2. **Requirement IDs.** Each requirement is numbered `REQ-<box-id>-NN` and uses MUST, SHOULD or MAY.
3. **Scenarios.** Each requirement has at least one Given/When/Then scenario.
4. **Tests cite requirements.** Each unit test names the requirement it covers in its docstring or name. A check lists requirements with no test.
5. **One task, one box.** Each entry in `tasks.md` names the box it works on. A task that needs two boxes is split.
6. **Archive on completion.** When a change is done, its spec changes are merged into `openspec/specs/`, and the change folder moves to `archive/`.
7. **Design links to decisions.** `design.md` lists the ADRs it relies on or creates.

Phase 0 includes evaluating the installed `engineering-spec:init-spec` skill and the OpenSpec command-line tool against this layout, and recording the choice as an ADR.

---

## 11. The working method

### Building

Steps 1 to 3 below are the structure part of the diagram pack. The flows, tables, screens and technology components are drafted alongside them, and all of it is vetted before step 4 begins. Section 25 gives the full stage order.

1. **Scaffold L0.** Name the system, its users and external systems. Generate. Review the diagram.
2. **Break down to L1.** Declare subsystems and the edges between them. Generate. Review.
3. **Break down to L2.** For one subsystem at a time, declare components and edges.
4. **For each leaf box, in dependency order:**
   1. Write the spec. Status becomes `specified`.
   2. Create the stub and a failing test. Status becomes `red`.
   3. Implement until tests pass. Status becomes `green`.
   4. Commit.
5. **Integrate.** For each edge whose two ends are green, write and pass the integration test. Status becomes `integrated`.
6. **Close the change.** Run all checks, archive the change, update `CHANGELOG.md`.

### Finding a fault

1. Run `vockpit locate` with the failing test name, the stack trace, or `file:line`.
2. The tool prints the box and its path, for example `vockpit > check > check-symbols`, with links to the spec, code and tests.
3. Run `vockpit test <box-id>` to test that box alone.
4. If the box passes alone, run the integration tests on its edges. The fault is on an edge or in a neighbour.
5. If nothing at that level fails, move up one level and repeat.
6. Every bug report records the box ID. A fix starts by adding a failing test to that box.

---

## 12. Commands and checks

### Commands

| Command | Purpose |
|---|---|
| `vockpit init` | Add the folder structure, templates and agent rules to a project |
| `vockpit new box <id> --parent <id>` | Add a box to the registry and create its spec from the template |
| `vockpit new change <slug>` | Create the next numbered change workspace |
| `vockpit new adr <title>` | Create the next numbered ADR |
| `vockpit generate` | Produce diagrams, viewer data and `modules.md` from the registry |
| `vockpit check` | Run every consistency rule; non-zero exit on any failure |
| `vockpit status [box-id]` | Show lifecycle status for all boxes or one |
| `vockpit test <box-id>` | Run the unit tests of one box; `--edges` adds its integration tests |
| `vockpit locate <target>` | Map a file and line, test name or stack trace to a box path |
| `vockpit prompt <box-id>` | Print a `@box-change` card with spec, code and test locations for an AI agent, plus the tables, screens, flow steps and technology components linked to that box |
| `vockpit new entity <id> --domain <id>` | Add a table to the registry |
| `vockpit new screen <id> --area <id>` | Add a screen to the registry |
| `vockpit new flow <id>` | Add a flow to the registry |
| `vockpit approve <id> [--tree]` | Record that the human has vetted an item, or an item and everything under it |
| `vockpit new change <slug> --scope <id>` | Create a change for a vetted box, subtree or flow, with spec skeletons filled in from the diagrams (section 25) |
| `vockpit view [id]` | Open the viewer, centred on the given item |

### Check rules

| ID | Rule |
|---|---|
| C01 | Registry files parse and match the schema |
| C02 | Box IDs are unique; every parent exists; there are no cycles |
| C03 | Every edge names two existing boxes |
| C04 | Every leaf box has a spec with at least one requirement and one scenario |
| C05 | Every code symbol in the registry exists in the source |
| C06 | Every code marker names a box in the registry, and every leaf box at `stubbed` or later has a marker |
| C07 | Every leaf box at `stubbed` or later has a unit test file |
| C08 | Every requirement is cited by at least one test |
| C09 | Every edge between two green boxes has an integration test |
| C10 | Generated diagrams and viewer data match a fresh generation |
| C11 | Hand-written behaviour diagrams name only existing boxes |
| C12 | Every active change has proposal, design, tasks and at least one spec change |
| C13 | Every task in an active change names an existing box |
| C14 | Every ADR has a status and is listed in the decisions index |
| C15 | No source file under `src/` is outside every box (no unowned code) |
| C16 | Every entity belongs to a data domain; every foreign key names an existing entity and column |
| C17 | Every `reads` and `writes` on a box names an existing entity; every entity is read or written by at least one box |
| C18 | Every navigation target is an existing screen; every screen can be reached from an entry screen |
| C19 | Every screen action names an existing box, or is marked as navigation only |
| C20 | Every flow step names existing boxes; each step follows an existing edge; a step's `via` names an existing technology component |
| C21 | Every `uses` on a box names an existing technology component; every technology component is used by at least one box |
| C22 | Layer rules hold (section 26), for example a view box does not read or write an entity directly |
| C23 | Every handoff stage names a defined actor, an input artefact and an output artefact |
| C24 | Every rule, skill, hook and context file listed in `harness.yaml` exists, every such file on disk is listed, and every hook runs a real command |
| C25 | No box in an active change is unvetted, or changed since it was vetted |
| C26 | Warning, not failure: a generated diagram has more than 12 nodes and should be split |
| C27 | Every spec in an active change has the sections its box's links call for (data, UI, flow), with no generated placeholder left unfilled |

Each rule has a fixture project in `tests/fixtures/broken_*` that must fail that rule and no other. This is how the checker itself is proven to work.

---

## 13. Logging

Two kinds of logging are covered.

### Logging by Vockpit tool

- Structured JSON, one record per line, written to `.vockpit/logs/<date>.jsonl`. Human-readable summary on the console.
- Fields: `ts` (UTC), `level`, `run_id`, `command`, `box_id` when applicable, `event`, `detail`.
- Every check finding is logged with its rule ID and box ID.
- Log files are not committed.

### Logging in projects that use Vockpit

- `vockpit.logging` provides a logger that adds `box_id` (from the `@box` marker) and a correlation ID to every record.
- Required events for a leaf box: entry with input summary, each decision taken with its reason, exit with outcome, and any error with the exception.
- Levels: DEBUG for internals, INFO for decisions and outcomes, WARNING for recoverable problems, ERROR for failures.
- Secrets, tokens and personal data are never logged. A check in the pre-commit hook scans for common secret patterns.
- Because every record carries `box_id`, a log line from a failure can be passed to `vockpit locate` directly.

---

## 14. Version control

| Topic | Rule |
|---|---|
| Repository | `git init` in Phase 0. Default branch `main`. |
| Branches | One branch per change: `change/NNN-<slug>`. No direct commits to `main` after Phase 0. |
| Commits | Conventional Commits. The scope is the box ID: `feat(check-symbols): resolve dotted class paths`. |
| Trailers | `Change: NNN` on every commit. `ADR: NNNN` when a commit implements a decision. |
| Granularity | One commit per box status transition where practical. |
| Pre-commit hook | Runs `vockpit check`, the unit tests for boxes whose files changed, and the secret scan. |
| Merge | Only when `vockpit check` and the full test suite pass. The PR template asks for the change number, boxes touched and ADRs. |
| Tags | `v0.N.0` at the end of each phase. |
| CI | GitHub Actions on every push: install, check, test, regenerate and compare. |
| Ignore | `.venv/`, `.vockpit/`, `__pycache__/`, `.env`, editor folders. |
| Generated files | Committed, and marked in `.gitattributes` so reviews can collapse them. |
| Secrets | Never committed. `.env.example` documents required variables. |

---

## 15. Agent configuration and skills

### Files

| File | Role |
|---|---|
| `AGENTS.md` | Canonical constitution: project purpose, folder map, the method in brief, commands, hard rules, links to `.agent/rules/`. |
| `CLAUDE.md` | Imports `AGENTS.md`. Adds Claude-specific notes only. |
| `.agent/rules/*.md` | Full rule text, always on (section 6 lists the six files). |
| `.agent/hooks.json` | Antigravity hooks: after an edit, run `vockpit check` and the touched box's tests. |
| `.claude/settings.json` | Claude Code hooks doing the same, plus a pre-write secret scan that really scans. |

### Hard rules for agents

1. Do not write code under `src/` without an active change.
2. Do not edit files under `docs/diagrams/` or `docs/viewer/model.json`.
3. Work on one box per task. Finish its tests before starting another.
4. Do not store line numbers anywhere.
5. Do not report "verified" unless `vockpit check` and the relevant tests ran in this session and passed. Quote the output.
6. Record a decision (section 17) whenever a choice between alternatives is made.
7. After each task, report: what was built, inputs and outputs, where a human can steer, and the test output.

### Project skills (`.claude/skills/`)

| Skill | Does |
|---|---|
| `box-scaffold` | Break a box into children: update the registry, create specs, regenerate, show the diagram for review |
| `box-spec` | Write or revise a box's spec with requirement IDs and scenarios |
| `box-build` | Take one box from `specified` to `green`: stub, failing tests, implementation, commit |
| `box-integrate` | Write and pass integration tests for the edges of a box |
| `box-locate` | Given a failure, run `vockpit locate`, isolate the box, propose a failing test |
| `change-open` | Create a change workspace and its branch |
| `change-close` | Run checks, merge spec changes, archive, update the changelog |
| `adr-new` | Record a decision using the template and update the index |
| `diagram-sync` | Regenerate diagrams and report what changed |
| `pack-draft` | Read `brief.md` and draft the registry for every view: boxes to L2, flows, tables, screens, technology components. Generate the diagram pack. Write no specs and no code. |
| `pack-review` | Walk the human through unvetted items one view at a time, apply their corrections to the registry, and record approvals |
| `data-model` | Add or change tables in a data domain and regenerate the ERD |
| `ui-flow` | Add or change screens and navigation and regenerate the navigation map |
| `spec-from-diagrams` | For a vetted scope, open a change and write the detailed specs from the spec skeletons |

Each skill is a short instruction file that calls the `vockpit` commands. The skills hold no logic of their own, so the same method works in any agent that can run a command.

---

## 16. Documentation

| Document | Content | Maintained by |
|---|---|---|
| `README.md` | Purpose, install, five-minute quick start, link to viewer | Hand |
| `docs/method.md` | The box-by-box method, independent of the tool | Hand |
| `docs/user-guide.md` | Each command with an example; how to adopt on an existing project | Hand |
| `docs/architecture.md` | Narrative with the generated L0 and L1 diagrams embedded | Hand, diagrams generated |
| `docs/modules.md` | Every box: summary, inputs, outputs, code, spec, tests, status | Generated |
| `docs/decisions/` | ADRs and the decision log | Hand, index checked |
| `CHANGELOG.md` | One entry per closed change, grouped by version | Hand at change close |
| `goals/tasks.md` | Project task board | Hand |
| Docstrings | Every public function: purpose, arguments, return, box ID | Hand |

A change is not complete until the documents it affects are updated. `change-close` lists which ones to review.

---

## 17. Decision logging

### Two levels

| Level | Use for | Where |
|---|---|---|
| **ADR** | Choices that are costly to reverse, affect more than one box, add a dependency, or change the method | `docs/decisions/NNNN-<slug>.md` |
| **Log entry** | Small choices inside one box | One line in `docs/decisions/log.md`: date, box, decision, reason |

### ADR format

Title, date, status (`proposed`, `accepted`, `superseded by NNNN`), context, options considered, decision, consequences, boxes affected.

ADRs are never deleted or rewritten. A changed decision gets a new ADR that supersedes the old one.

### ADRs to write in Phase 0

| No. | Decision |
|---|---|
| 0001 | Record decisions as ADRs |
| 0002 | The registry is the single source of truth; diagrams are generated |
| 0003 | Reference code by symbol, never by line number |
| 0004 | Three structural levels (L0, L1, L2), with behaviour diagrams only where needed |
| 0005 | D2 as the diagram language |
| 0006 | Spec layout and tooling (OpenSpec layout; result of the Phase 0 evaluation) |
| 0007 | Python 3.10+ with PyYAML and pytest as the only runtime dependencies |
| 0008 | Python projects supported first; other languages through a resolver interface later |
| 0009 | Conventions for spec and test file locations instead of registry fields |
| 0010 | Runtime AI-gateway features from `plan.md` are out of scope |
| 0011 | Flows, tables, screens and technology components live in the registry and are linked to boxes |
| 0012 | Diagrams are vetted before specs are written; approval is tied to a content hash |
| 0013 | Layer names and the layer rules that are enforced |
| 0014 | Screen wireframes are low-fidelity and rendered from the registry; detailed visual design stays outside Vockpit |
| 0015 | The project template is seeded from `C:\dev\tools\template-harness` and maintained in this repository |
| 0016 | The harness (rules, skills, hooks, context files) is declared in the registry and checked |
| 0017 | EGM is used for brainstorming, design drafting and fresh-context review; Vockpit adds the registry, diagrams, checks and box-by-box build |

---

## 18. Testing

| Kind | Scope | Location |
|---|---|---|
| Unit | One leaf box, neighbours replaced by simple stand-ins | `tests/unit/test_<box_id>.py` |
| Integration | One edge, both real boxes | `tests/integration/test_<from>__<to>.py` |
| End-to-end | A full command run against a fixture project | `tests/e2e/` |
| Checker proof | Each rule fails on its broken fixture and passes on the good one | `tests/e2e/` using `tests/fixtures/` |

- Tests are written before the implementation of each box.
- A fixed bug always adds a test to the box where it was found.
- Target: every requirement cited by a test (rule C08). Line coverage is reported but is not the goal.

---

## 19. Phases

Each phase is one or more numbered changes and ends with a tag. A phase is done only when its exit test passes.

The phases below describe the work by subject. They are no longer the order of delivery. Section 31 regroups them into releases, starting with a much smaller first release, and takes precedence where the two differ.

### Phase 0 — Foundation

- `git init`, `.gitignore`, `.gitattributes`, `pyproject.toml`, virtual environment.
- Create the folder structure in section 6 (empty where content comes later).
- Write `AGENTS.md`, `CLAUDE.md`, the six rule files, `README.md` skeleton.
- Seed `templates/` from `C:\dev\tools\template-harness` and apply the fixes in section 29. Copy and adapt the other sources in section 5.
- Write ADRs 0001 to 0017.
- Evaluate `engineering-spec:init-spec` and the OpenSpec tool; record in ADR 0006.
- Install the EGM plugin, read its README, and run its three commands once on this plan. Correct section 30 where the plugin differs from what is written there. Confirm which of Claude Code, Antigravity CLI and the Antigravity IDE can run the review stage.
- Declare Vockpit's own L0 and L1 boxes in `model/system.yaml` by hand (section 21), together with `handoff.yaml` and `harness.yaml`.
- **Exit test:** repository exists with one commit; folder tree matches section 6; seventeen ADRs present; an EGM review of this plan has run and its findings are recorded.
- **Tag:** `v0.0.0`

### Phase 1 — Registry and checks

- Boxes: `registry-load`, `registry-validate`, `resolve-symbols`, `resolve-tests`, `check-*` for rules C01 to C09 and C12 to C15, `cli`.
- The registry schema covers every kind of item: boxes, entities, screens, flows, technology components, handoff stages and harness items. Rules C16 to C24 and C26 are added one view at a time, in this order: data, flow, UI, technology and layer, handoff and harness. Each view is its own change.
- Good and broken fixture projects. The good fixture is a small web application with a database, a cache and a queue, so every view has something to show.
- **Exit test:** `vockpit check` passes on the good fixture, and each broken fixture fails exactly its own rule. `vockpit check` passes on Vockpit itself.
- **Tag:** `v0.1.0`

### Phase 2 — Generation and viewer

- Boxes: `generate-d2`, `generate-svg`, `generate-viewer-data`, `generate-modules-doc`, rules C10 and C11.
- Adapt the viewer to load `model.json`; add level drill-down and the inspector showing spec, code and test links.
- Generators for the flow, data, UI, technology, layer, handoff and harness diagrams. Viewer lenses, table cards and screen wireframes (section 24).
- **Exit test:** Vockpit's own L0, L1 and L2 diagrams are generated and open in the viewer; editing a generated file makes `vockpit check` fail. On the good fixture, drilling from L0 to one L2 box shows that box's flow steps, tables, screen and technology components and no others.
- **Tag:** `v0.2.0`

### Phase 3 — Status, per-box testing and fault location

- Boxes: `status-compute`, `test-run`, `locate-file`, `locate-test`, `locate-trace`, `prompt-card`, `logging-helper`.
- Status colours in generated diagrams.
- **Exit test:** a fault deliberately placed in one box is traced to that box by `vockpit locate` from the stack trace alone; `vockpit test <box>` runs only that box's tests.
- **Tag:** `v0.3.0`

### Phase 4 — Agent workflow

- Boxes: `scaffold-init`, `scaffold-box`, `scaffold-change`, `scaffold-adr`.
- The fourteen skills, working hooks in `.claude/settings.json` and `.agent/hooks.json`, pre-commit hook, CI workflow, issue and PR templates.
- Vetting and spec generation: `vockpit approve`, `vockpit new change --scope`, rules C25 and C27.
- `sdd.ps1` changed to call `vockpit init`, so a new project starts from the upgraded template.
- **Exit test:** an agent, given only "add box X", completes the full loop from change to archive with all checks passing and no manual correction. Starting from an empty folder and a one-page brief, `sdd <name>` followed by `pack-draft` produces a diagram pack that passes `vockpit check`, and `vockpit new change --scope` is refused until the scope is vetted.
- **Tag:** `v0.4.0`

### Phase 5 — Pilot on HelloWorld-SDD

- Run `vockpit init` there. Put it under version control. Remove the duplicate `service.py`. Move its boxes into a registry. Replace the hand-typed studio data with generated data.
- Complete its open task (time-of-day greeting) using the method.
- **Exit test:** `vockpit check` passes there; the mismatches listed in section 2 are gone.

### Phase 6 — Pilot on one real project

- Apply to `2026-May-20-Angel1-Trading-Signal-Dashboard` (smallest existing documentation, real code).
- Record every point where the method was awkward. Fix the tool or the method, with ADRs.
- **Exit test:** one real bug or feature in that project handled end to end with the method.
- **Tag:** `v0.5.0`

### Phase 7 — Packaging for others

- Installable package, complete user guide, worked example, `vockpit init` tested on an empty folder and on an existing project.
- Publication to GitHub is a separate decision, to be confirmed at that time.
- **Tag:** `v1.0.0`

---

## 20. Dropped or deferred from `plan.md`

| Item | Decision | Reason |
|---|---|---|
| Six "flight levers" (model routing, quota, grounding, prompt shield, HITL, provenance seal) | Dropped | Features of an AI application, not of a development method |
| OpenTelemetry tracing, cost calculator, live latency colours | Dropped | Replaced by box status colours |
| D2 parser and code generator from diagrams | Dropped | Diagrams are generated from the registry; the AI agent writes code from specs |
| `swarms/` agent hierarchy | Deferred | Skills and rules cover agent behaviour; revisit after Phase 6 |
| Three showcase demos | Reduced | Two pilots (Phases 5 and 6) serve as proof |
| GitHub Pages, slides, video kit | Brought forward | GitHub publication and a live demo page are part of every release from 0.1 (section 31). Slides and video are optional per release. |
| Aviation naming | Optional | May be used for viewer styling only |

---

## 21. Starting scaffold: Vockpit's own boxes

**L0:** `vockpit` — used by a Developer and an AI Agent; reads a Project Repository; calls the D2 tool, Git and pytest.

**L1:**

| Box | Purpose | Receives from | Sends to |
|---|---|---|---|
| `cli` | Parse commands, dispatch, set exit code | Developer, Agent | all others |
| `registry` | Load and validate the model | `cli` | `resolve`, `check`, `generate`, `status`, `locate` |
| `resolve` | Find code symbols, markers and tests | `registry` | `check`, `status`, `locate` |
| `check` | Apply rules C01 to C15 | `registry`, `resolve` | `cli`, `status` |
| `status` | Compute lifecycle status | `resolve`, `check`, test results | `generate`, `cli` |
| `generate` | Produce diagrams, viewer data, docs | `registry`, `status` | Project Repository |
| `locate` | Map a failure to a box path | `registry`, `resolve` | `cli` |
| `scaffold` | Create boxes, changes, ADRs, project setup | `cli` | Project Repository |
| `logging` | Structured logs with box ID | all | `.vockpit/logs/` |

L2 boxes are declared at the start of each phase, in that phase's change.

---

## 22. Risks

| Risk | Response |
|---|---|
| Registry upkeep feels like extra work and gets skipped | Scaffold commands write the registry; hooks block commits when it is out of step |
| Box granularity drifts too fine or too coarse | Guideline: a leaf fits a one-page spec. Review at each phase end. |
| Method only fits Python | Resolver sits behind an interface (ADR 0008). Second language considered after Phase 6. |
| Tool grows before the method is proven | Phases 5 and 6 are pilots, placed before packaging |
| Agents bypass the rules | Hard rules are enforced by hooks and CI, not by instruction alone |
| Generated SVGs differ between D2 versions and cause false failures | Pin the D2 version; compare `.d2` text for freshness, not SVG bytes |
| Draft 2 makes the registry several times larger than Draft 1, and the tool could stall before anything is usable | Structure view first, then one view per change in a fixed order. Each view is usable when its change closes. |
| The agent-drafted diagram pack looks complete but is wrong, and the human approves it without reading | `pack-review` presents one view and one level at a time. Approval is per item, not one button for everything. |
| Screens and tables in the registry drift from the real UI code and database schema | Phase 6 decides, with an ADR, whether to add resolvers that read migrations and route definitions, as the symbol resolver does for code |
| EGM is at an early version and not an officially supported Google product; its commands or file names may change | Vockpit calls EGM only through the three commands and reads only its output documents. Version pinned in `harness.yaml`. ADR 0017 records what to do if it is withdrawn: the `pack-draft` and `pack-review` skills still work alone. |
| EGM review needs fresh sub-sessions, and stops where the host cannot provide them. One write-up reports the standalone Antigravity IDE cannot. | Phase 0 tests each host. Until then, plan to run the review stage from Claude Code or the Antigravity CLI. |
| Two design documents (EGM's Markdown and the registry) drift apart | The registry holds every structured fact. `design_draft.md` holds reasoning and links to generated diagrams; it does not restate tables, screens or boxes. |
| Wireframes are mistaken for visual design | They show regions, controls and actions only (ADR 0014). A screen may link to an external mock-up. |

---

## 23. Points to confirm

1. **File name.** This plan is saved as `fable-plan.md`, and `plan.md` is left untouched. Say if `plan.md` should be replaced instead.
2. **EGM.** Settled on 2026-11-10: EGM is Google's Elephant-Goldfish Model plugin. Section 30 describes how it is used. Its details come from Google's announcement and third-party write-ups, not yet from the plugin itself; Phase 0 verifies them.
3. **Diagram set.** Structure (L0, L1, L2), process flow, ERD, UI navigation and wireframes, technology components, layers, AI handoff and harness are always produced. State diagrams are added where a box has states. Other UML (class, activity) is written only on request. Confirm or extend.
4. **Agents to support.** Both Antigravity (`.agent/`) and Claude Code (`.claude/`) are covered. Say if only one is needed.
5. **First language.** Python only at first.
6. **Second pilot.** Angel1 Trading Signal Dashboard is proposed for Phase 6.
7. **Duplicate folder.** `C:\dev\2026-NOV-10-VIBE-cooling-cockpit` holds a copy of `plan.md`. It has not been touched.
8. **Template location.** Confirmed 2026-11-10. The template is copied into this repository's `templates/` folder and upgraded there, and `sdd.ps1` is pointed at it. `C:\dev\tools\template-harness` is left as it is until Phase 4 passes, then replaced.
9. **Layer names.** Confirmed 2026-11-10. Five layers: view, controller, model, repository, integration.
10. **Wireframes.** Confirmed 2026-11-10. Low-fidelity wireframes drawn from a list of elements, not finished visual design.
11. **Size.** Settled 2026-11-10: build step by step. A first basic release is implemented, used, put on GitHub, publicised, and feedback gathered before the next (section 31).
12. **Before the first publication.** Needed from you: the GitHub account and repository name, the licence (Apache 2.0 is proposed, matching EGM), and where it will be announced.

---

## 24. Views and contextual drill-down

### The views

The box hierarchy of Draft 1 stays as the spine. Seven more views hang from it. Every view is declared in the registry and its diagrams are generated.

| View | Question it answers | Its own hierarchy | Diagram |
|---|---|---|---|
| **Structure** | What parts exist, and what passes between them? | System, subsystem, component (L0, L1, L2) | Box diagram per level |
| **Process flow** | In what order do things happen for one use case? | Use case, flow, step | Sequence diagram per flow |
| **Data** | What is stored, in which tables and columns, and how are tables related? | Data model, domain, table, column | ERD per domain; table card per table |
| **UI** | What screens exist, what is on each, and how does a user move between them? | Application, area, screen, element | Navigation map; wireframe per screen |
| **Technology** | Which database, cache, queue, stream or external service is involved? | Environment, component, resource (topic, queue, key space, schema) | Component diagram |
| **Layer** | Which box is view, which is controller, which is model, and which talks to the store? | Layers within one L1 box | Layer diagram per L1 box |
| **AI handoff** | Which stage is done by a human and which by an AI agent, and what is passed on? | Stage, actor, artefact | Swimlane diagram |
| **Harness** | Which rules, skills, hooks and context files are in force, and at which stage? | Stage, harness item | Checklist diagram |

### How the views are linked

Links are fields in the registry. Each link is checked (rules C16 to C24).

| From | Field | To | Meaning |
|---|---|---|---|
| Box | `reads`, `writes` | Entity | The box queries or changes that table |
| Box | `uses` | Technology component | The box connects to that database, cache, queue or stream |
| Box | `layer` | Layer name | The role the box plays |
| Screen action | `calls` | Box | Pressing this control runs that box |
| Screen action | `goes_to` | Screen | Pressing this control opens that screen |
| Flow step | `from`, `to` | Box | One message between two boxes |
| Flow step | `via` | Technology component | The message travels over that queue or stream |
| Entity column | `references` | Entity column | Foreign key |
| Entity | `stored_in` | Technology component | Which database holds the table |

### Example registry entries

```yaml
# model/data/orders.yaml
domain: orders
stored_in: main-db
entities:
  - id: order
    table: orders
    summary: One customer order.
    columns:
      - { name: id,          type: uuid,      key: primary }
      - { name: customer_id, type: uuid,      references: customer.id }
      - { name: status,      type: text,      values: [new, paid, shipped, cancelled] }
      - { name: total_cents, type: integer }
      - { name: created_at,  type: timestamp }
```

```yaml
# model/ui/checkout.yaml
area: checkout
screens:
  - id: cart-screen
    title: Cart
    entry: true
    elements:
      - { id: item-list,  kind: list,   shows: order-item }
      - { id: pay-button, kind: button, label: Pay, calls: create-order, goes_to: payment-screen }
```

```yaml
# model/flows/place-order.yaml
id: place-order
title: Customer places an order
steps:
  - { from: cart-view,     to: order-controller, data: Cart }
  - { from: order-controller, to: create-order,  data: OrderRequest }
  - { from: create-order,  to: order-repository, data: Order }
  - { from: create-order,  to: notify-warehouse, data: OrderCreated, via: order-events }
```

### What the viewer shows

The viewer always has one **focus**. The focus decides everything on screen.

```text
+-------------------------------------------------------------------------+
| Shop  >  Orders  >  create-order                          [ zoom out ]  |
| Lens: [Structure] [Flow 1] [Data 2] [UI 1] [Technology 2] [Layer]       |
+-----------------------------------------------+-------------------------+
|                                               | create-order            |
|   Diagram for the focus in the chosen lens.   | Status: vetted          |
|   Only items linked to the focus are drawn.   | Layer: model            |
|                                               | Spec / Code / Tests     |
|                                               | Handoff card  [ copy ]  |
+-----------------------------------------------+-------------------------+
```

Rules for the viewer:

1. **Zoom in** by clicking a node or scrolling in on it. The node becomes the focus and its children are drawn. **Zoom out** with the breadcrumb or by scrolling out.
2. **Lenses appear only when they have content.** A lens tab is shown only if the focus has linked items in that view, with a count. A box that touches no table has no Data tab.
3. **A lens shows linked items only.** With `create-order` in focus, the Data lens draws the `orders` and `order_items` tables and the relation between them, not the whole ERD. The Flow lens draws the flows that pass through the box, with its steps highlighted. The Technology lens draws the database and the event stream it uses.
4. **The level sets the amount of detail.** At L0 the Data lens shows data domains as single nodes. At L1 it shows the tables of the domains that subsystem touches. At L2 it shows those tables with their columns.
5. **Any item can be the focus.** Clicking a table makes the table the focus: the viewer shows its table card (columns, keys, indexes), the tables it relates to, and the boxes that read and write it. Clicking a screen shows its wireframe, the screens it leads to, and the boxes its actions call. This is how a reader goes through tables or screens one by one.
6. **The address holds the focus.** The focus and lens are in the page address, so a link to "the Data lens of `create-order`" can be put in a spec, a commit message or a bug report.
7. **One screenful.** A diagram with more than 12 nodes draws a warning (rule C26). The answer is another level, not a larger picture.

### Walk-through

A reader new to the system would move like this:

1. Opens the viewer. Focus is the system (L0). Sees users, external systems, and the system as one box. The Technology lens shows the database, cache and event stream as single nodes.
2. Clicks into the system. Sees the L1 subsystems. Clicks **Orders**.
3. Sees the L2 components of Orders. The Layer lens shows which are view, controller, model and repository, and which one talks to the database.
4. Clicks `create-order`. Opens the Flow lens: the "Customer places an order" sequence, with this box's steps highlighted.
5. Opens the Data lens: `orders` and `order_items`. Clicks `orders`: the table card, column by column.
6. Opens the UI lens: the Cart screen, with the Pay button that calls this box, and the screen it leads to.
7. Zooms out twice. Back at L1, with the whole path still in the breadcrumb.

---

## 25. Stages: from brief to build

The system is designed and approved as diagrams first. Detailed specifications are written only for the part the human asks to build.

| Stage | Who | What happens | Result | Gate to pass |
|---|---|---|---|---|
| **0. Start** | Human runs `sdd <name>` | Project created from the template: folders, registry seeds, rules, skills, hooks, context files, git | Empty project that passes `vockpit check` | Harness check C24 passes |
| **1. Brief** | Human, with the Elephant session (`/egm:egm-brainstorm`) | The human writes the initial specification in plain words in `brief.md`: purpose, users, main use cases, known data, known screens, technology constraints. The Elephant questions it, explores alternatives and records the agreed direction. No code. | `brief.md`, `concepts_brief.md` | Human says the direction is agreed |
| **2. Diagram pack** | Elephant session (`pack-draft` with `/egm:egm-draft`) | Drafts the registry for every view and generates all diagrams. Writes `design_draft.md`, the narrative that explains them. Lists the assumptions it made and the questions it could not answer. Writes no specs and no code. | L0, L1, L2 logic diagrams; process flows; ERDs; UI navigation and wireframes; technology and layer diagrams; AI handoff and harness diagrams; `design_draft.md` | `vockpit check` passes on the registry |
| **3. Vetting** | Goldfish sessions (`/egm:egm-review`), then the human, helped by `pack-review` | Fresh sessions with no memory of the drafting review the design document and diagrams first. The human chooses which findings to fix, then reviews in the viewer, one view and one level at a time. Corrects by commenting on a node; the agent updates the registry and regenerates. Approves item by item. | Every approved item has status `vetted` | Human approval recorded in `model/review.yaml` |
| **4. "Now build this"** | Human names a scope: a box, a subtree or a flow | `vockpit new change <slug> --scope <id>` creates the change with spec skeletons drawn from the diagrams. The agent (`spec-from-diagrams`) writes the detailed specs. A Goldfish session checks them for implementation readiness before the human approves. | `proposal.md`, `design.md`, `tasks.md`, one spec per leaf box in scope | Scope is fully vetted (C25); human approves the specs |
| **5. Build** | AI agent, one box at a time | Section 11: stub, failing test, implementation, commit | Boxes at `green` | Unit tests pass |
| **6. Integrate and close** | AI agent, human reviews | Integration tests on edges; checks; archive the change | Boxes at `integrated` | `vockpit check` and all tests pass |

### How vetting is recorded

`vockpit approve <id>` stores, in `model/review.yaml`, the item's ID, the date, and a hash of the item's registry entry. Status `vetted` is computed: the stored hash must equal the current hash. If anyone changes the item afterwards, the hashes differ and the item drops back to `proposed` until it is approved again. Approval therefore cannot go stale without the tool noticing.

### How diagrams become specifications

`vockpit new change --scope` fills each spec skeleton from what the diagrams already say. The agent then writes the detail; it does not start from a blank page.

| In the diagrams | Becomes in the spec |
|---|---|
| Box inputs and outputs | Interface section: what the box accepts and returns |
| Each flow step that enters or leaves the box | One Given/When/Then scenario stub per step |
| Each entity the box writes | A data requirement, the columns involved, and a migration task in `tasks.md` |
| Each entity the box reads | A data requirement naming the query and what happens when nothing is found |
| Each screen action that calls the box | A UI requirement and an acceptance scenario in the user's terms |
| Each technology component the box uses | A requirement naming the resource (topic, queue, key pattern) and its limits (expiry time, retry, ordering) |
| `decision_gate: true` | A decision gate table from the template |
| Edges of the box | One integration test task per edge |

`design.md` in the change embeds the diagrams for the scope, so the reader of the change sees the same pictures that were vetted.

### Changing the design later

A change to behaviour starts in the registry, not in the code. The diagram is updated and regenerated, the changed items are vetted again, the spec change is written, and then the code is changed. Rule C25 blocks a change whose boxes were altered after vetting.

### Added hard rules for agents

These extend the list in section 15.

8. Do not write a spec for a box that is not `vetted`.
9. During the diagram pack stage, write only to `model/`, `brief.md` and the EGM design documents. Do not create specs, code or tests.
10. When drafting the diagram pack, list every assumption made beyond the brief. Do not present a guess as a requirement.

---

## 26. Technology components and layers

### Technology components

`model/tech.yaml` declares every runtime part that is not application code.

```yaml
components:
  - id: main-db
    kind: database          # database | cache | queue | stream | object-store | external-api | llm | scheduler
    product: PostgreSQL
    summary: System of record for orders and customers.
  - id: session-cache
    kind: cache
    product: Redis
    resources:
      - { id: cart, pattern: "cart:{customer_id}", expiry: 30m }
  - id: order-events
    kind: stream
    product: Kafka
    resources:
      - { id: order-created, topic: order.created }
```

A box declares what it connects to:

```yaml
  - id: create-order
    layer: model
    writes: [order, order-item]
    uses:   [main-db, order-events]
```

In diagrams, each kind has a fixed shape: cylinder for a database, a stacked cylinder for a cache, a queue shape for queues and streams, a cloud for external services. The same component looks the same in every diagram it appears in.

Where technology appears:

| Level | What is shown |
|---|---|
| L0 | Each component as one node beside the system |
| L1 | Which subsystem connects to which component |
| L2 | Which box connects, and to which resource (topic, key pattern, table) |
| Flow | A step sent over a queue or stream is drawn through that component |

### Layers

Each L2 box carries one `layer` value.

| Layer | Role | May connect to |
|---|---|---|
| `view` | Screens and what the user sees | `controller` |
| `controller` | Receives a user action or request and decides what to call (the presenter, in model-view-presenter terms) | `model`, `view` |
| `model` | Business rules and decisions | `repository`, `integration`, other `model` |
| `repository` | Reads and writes tables and caches | Technology components of kind database or cache |
| `integration` | Talks to queues, streams and external services | Technology components of the other kinds |

The layer diagram for an L1 box draws its L2 boxes in these five bands, top to bottom, with the technology components underneath. It answers directly: what connects to the view, what connects to the model, what connects to the database.

Rule C22 enforces the "may connect to" column. The default rules are: a `view` box has no `reads`, `writes` or `uses`; only `repository` boxes have `reads` and `writes`; only `repository` and `integration` boxes have `uses`. A project can relax a rule, with an ADR.

---

## 27. AI handoff view

`model/handoff.yaml` declares the stages of section 25 as a chain: who acts, what they receive, what they produce, and which gate closes the stage.

```yaml
actors:
  - { id: pilot,     kind: human, title: Developer }
  - { id: elephant,  kind: agent, title: Elephant (long session, holds project context, writes no code), skills: [egm-brainstorm, egm-draft, pack-draft, box-scaffold] }
  - { id: goldfish,  kind: agent, title: Goldfish (fresh session, no memory), skills: [egm-review, pack-review] }
  - { id: spec,      kind: agent, title: Spec agent,      skills: [spec-from-diagrams, box-spec] }
  - { id: builder,   kind: agent, title: Builder agent,   skills: [box-build] }
  - { id: reviewer,  kind: agent, title: Reviewer agent,  skills: [box-integrate, change-close] }
stages:
  - { id: brief,   actor: pilot,     produces: brief.md }
  - { id: brief,   actor: elephant,  receives: brief.md,        produces: concepts_brief.md,          gate: human agreement }
  - { id: pack,    actor: elephant,  receives: concepts_brief.md, produces: "model/**, design_draft.md", gate: vockpit check }
  - { id: review,  actor: goldfish,  receives: design_draft.md and diagram pack, produces: review findings, gate: human chooses findings to fix }
  - { id: vetting, actor: pilot,     receives: diagram pack,    produces: model/review.yaml,          gate: human approval }
  - { id: specs,   actor: spec,      receives: vetted scope,    produces: "openspec/changes/NNN/**",  gate: human approval }
  - { id: build,   actor: builder,   receives: handoff card,    produces: code and unit tests,        gate: unit tests pass }
  - { id: close,   actor: reviewer,  receives: green boxes,     produces: integration tests, archive, gate: vockpit check and all tests }
```

The generated diagram has one lane per actor and one column per stage, with the artefact named on each arrow and the gate drawn at each stage boundary. Human lanes and agent lanes are coloured differently, so it is plain where a person must act.

### The handoff card

What passes between agents is a **handoff card**, printed by `vockpit prompt <box-id>`. It replaces the `@dfd-change` card of the template. It contains only what the receiving agent needs for that one box:

- box ID, path, layer and status
- spec location and the requirement IDs
- code symbol and test file
- the tables it reads and writes, with columns
- the screens and actions that call it
- its steps in each flow
- the technology components and resources it uses
- its edges and the status of the box at the other end

An agent given a card does not need to read the whole repository. This keeps each agent's context small and specific, which is the point of building one box at a time.

### How the actors run

An actor is a role: a set of rules and skills. The same registry and commands serve any of these arrangements, and the plan does not depend on which is chosen:

| Arrangement | How |
|---|---|
| One agent, in turn | A single agent takes each role in order. The handoff card is its working context for the next box. |
| Separate agents in Antigravity | One conversation per role or per box, each started with a handoff card |
| Subagents in Claude Code | The main agent hands each box to a subagent with the card as its prompt |

Running several builder agents at once is allowed only on boxes with no edge between them. `vockpit status` lists which boxes are free to build in parallel.

---

## 28. Harness: rules, skills, hooks and context from the first day

Every project started with `sdd <name>` receives the full harness, and the harness is itself declared in the registry so it can be drawn and checked.

### `model/harness.yaml`

```yaml
items:
  - { id: rule-spec-lifecycle, kind: rule,    path: .agent/rules/01_spec_lifecycle.md, stages: [specs, build, close] }
  - { id: skill-pack-draft,    kind: skill,   path: .claude/skills/pack-draft/SKILL.md, stages: [pack] }
  - { id: hook-check-on-edit,  kind: hook,    path: .claude/settings.json, event: PostToolUse, runs: vockpit check, stages: [build] }
  - { id: ctx-agents,          kind: context, path: AGENTS.md, stages: [all] }
```

### Checklist created at project start

| Kind | Items |
|---|---|
| **Context** | `AGENTS.md` (constitution), `CLAUDE.md` (imports it), `brief.md`, `docs/glossary.md` (project terms), `goals/tasks.md`, `.env.example` |
| **Rules** | Spec lifecycle; box method; diagram standards; logging; version control; decision logging; staged design (section 25); layers (section 26) |
| **Skills** | The fourteen skills of section 15, installed for both Antigravity (`.agent/skills/`) and Claude Code (`.claude/skills/`) |
| **Hooks** | After an edit: `vockpit check` and the tests of the touched box. Before a write: a secret scan that scans. Before a commit: check, tests, secret scan. Before a write under `src/` or `openspec/`: refuse if the box is not vetted or no change is open. |
| **Plugin** | EGM, installed whole (skills, personas and document standards), listed in `harness.yaml` |
| **Registry seeds** | `system.yaml` with the L0 box; empty `data/`, `ui/`, `flows/`; `tech.yaml`; `handoff.yaml` with the default actors and stages; `harness.yaml` listing everything above |
| **Repository** | `git init`, `.gitignore`, `.gitattributes`, first commit, CI workflow, PR and issue templates |

### The harness diagram

Generated from `harness.yaml`: one column per stage, and under each stage the rules that apply, the skills that are used, and the hooks that fire. It is the checklist in picture form. A reader can see at once that, for example, nothing guards the vetting stage, or that a hook is listed with no command.

Rule C24 makes the checklist real: every listed file must exist, every rule, skill and hook file on disk must be listed, and every hook must run a real command. A hook whose command does nothing fails the check.

---

## 29. The existing template: reuse and upgrade

`C:\dev\tools\template-harness`, with `sdd.ps1`, is the starting point. It already has the right shape: `AGENTS.md`, `.agent/` rules, skills and hooks, the OpenSpec layout, L0/L1/L2 diagrams, an ERD, sequence flows and an interactive studio. It is copied into `templates/` in Phase 0 and upgraded there.

### What is kept

| Item | Use |
|---|---|
| Folder layout and `openspec/config.yaml` | Kept. `diagram_formats` changed to D2 for all generated diagrams. |
| The four-phase lifecycle in `sdd_lifecycle.md` | Kept and extended with the brief, diagram pack and vetting stages in front |
| The "HOW & IPO" card after each task | Kept as the task report (hard rule 7 in section 15) |
| `@dfd-change` visual prompting | Kept as the handoff card (section 27) |
| L0, L1, L2 naming and D2 styling, including click-through links between levels | Kept as the look the generator must reproduce |
| `logging_and_observability.md`, `security_and_resilience.md`, `coding_standards.md` | Kept, revised to name box IDs |
| `sdd <name>` as the one command to start a project | Kept. It calls `vockpit init`. |

### What is fixed

Each of these was found by reading the template on 2026-11-10.

| Finding | Location | Fix |
|---|---|---|
| The secret-safety hook runs `sys.exit(0)` and checks nothing | `.agent/hooks.json` | Replace with a real secret scan |
| The compliance audit only checks that files exist, then prints "100% Project Compliance Verified" | `tests/test_harness_audit.py` | Replace with `vockpit check` |
| L0, L1 and L2 diagrams are hand-written and carry the content of one sample project (a WhatsApp message pipeline) into every new project | `docs/diagrams/*.d2` | Generate from the registry. Move the sample to an `examples/` folder outside the template. |
| ERD, DFD and sequence diagrams are hand-written Mermaid with sample content, separate from the D2 diagrams | `docs/erd.md`, `docs/dfd.md`, `docs/sequence_flows.md`, `openspec/specs/guest-ops/*.mermaid` | Generate from `model/data/` and `model/flows/` |
| The interactive studio holds hand-typed node data | `docs/diagrams/interactive_dfd_studio.html` | Replace with the viewer that loads generated `model.json` |
| Two sample changes carry the same number, 001 | `openspec/changes/001-initial-feature`, `001-whatsapp-concierge` | Ship no sample change. The first change is created by the user. |
| The compliance skill refers to `specs/active/`, which does not exist; there is a second, unused spec folder | `.agent/skills/harness-compliance/SKILL.md`, `specs/template.md` | Remove both. One spec location: `openspec/`. |
| The diagram skill refers to files that do not exist (`docs/data_model_erd.d2`, `docs/system_architecture.svg`) | `.agent/skills/diagram-compiler/SKILL.md` | Replace with `diagram-sync` |
| `AGENTS.md` announces a four-phase lifecycle and lists three | `AGENTS.md` section 2 | Rewrite from section 25 |
| The scaffold script is copied into every new project, and exists in two near-identical versions | `scaffold_new_project.ps1`, `sdd.ps1` | One script, `sdd.ps1`, kept in `C:\dev\tools` only |
| No Claude Code configuration | missing `.claude/` | Add settings, hooks and skills |
| No UI view, no technology view, no layer view, no handoff or harness declaration | whole template | Add registry seeds and generators (sections 24 to 28) |
| The template is not under version control | `C:\dev\tools` | It lives in this repository from Phase 0 |

### Order of work on the template

1. Phase 0: copy into `templates/`, remove the sample content and the dead references, fix the hooks. The template is smaller and honest, though not yet generated.
2. Phases 1 and 2: replace hand-written diagrams and the studio with registry seeds, generators and the viewer.
3. Phase 4: add the staged workflow, the full harness and `harness.yaml`; point `sdd.ps1` at `vockpit init`.
4. Phase 5: apply the upgraded template to `HelloWorld-SDD`, which was created from the old one, as the first test of upgrading an existing project.

---

## 30. Working with the Elephant-Goldfish Model (EGM)

### What EGM is

EGM is an open-source plugin from Google (`github.com/google/elephant-goldfish-model`, Apache 2.0, announced 2026-10-22). It is a set of agent skills, personas and document standards, not an AI model. It runs in Claude Code and the Antigravity CLI. Google states it is not an officially supported product.

Its idea is that memory is assigned by role:

| Role | Memory | Job |
|---|---|---|
| **Elephant** | A long session that holds the project's context | Brainstorms and drafts the design with the human. Writes no code. |
| **Goldfish** | A fresh session that knows nothing of the drafting | Reviews the design document. What it cannot understand from the document alone is a gap in the document. |
| **Human** | | Makes the design decisions and approves |

| Command | Does | Produces |
|---|---|---|
| `/egm:egm-brainstorm` | Explores requirements and alternatives under a no-code rule | `concepts_brief.md` |
| `/egm:egm-draft` | Builds the design document section by section: problem, existing system, proposed changes, implementation plan | `design_draft.md` |
| `/egm:egm-review` | Review in stages by fresh sessions, including a comprehension check (can a fresh reader explain the proposal back?), a hostile critic, and an implementation readiness check. The human then chooses which findings to resolve. | Findings; approved design kept under `docs/designs/` |
| `egm-drift-report` skill | Compares design documents with the current code | List of differences |

This table is drawn from Google's announcement and third-party write-ups. Phase 0 checks it against the plugin's own README.

### How EGM and Vockpit fit together

EGM and Vockpit address the same stages from two sides. EGM supplies the conversation and the review discipline. Vockpit supplies the structured model, the diagrams, the checks that can fail, and the box-by-box build.

| Stage (section 25) | EGM does | Vockpit adds |
|---|---|---|
| 1. Brief | `egm-brainstorm`: the Elephant questions the brief and records the agreed direction | Nothing. `brief.md` is the input. |
| 2. Diagram pack | `egm-draft`: the Elephant writes the design document | `pack-draft` runs in the same Elephant session and writes the registry. All diagrams are generated from it and linked from the design document. |
| 3. Vetting | `egm-review`: Goldfish sessions review the document and the diagrams | The viewer for the human's own review; per-item approval tied to a hash; `vockpit check` |
| 4. Specifications | Implementation readiness check by a Goldfish on the change's `design.md` and specs | Spec skeletons generated from the diagrams; rule C25 |
| 5. Build | Nothing further; EGM hands an approved plan to a coding agent | One box at a time, each builder starting from a handoff card |
| 6. Close and after | `egm-drift-report`, run weekly, reads documents against code | `vockpit check` on every commit |

### Rules for using the two together

1. **The registry is the single source of truth for structure.** `design_draft.md` explains why, and links to generated diagrams. It does not restate boxes, tables, screens or flows. Where the EGM template asks for a list of files to change, the document points to the change's `tasks.md`.
2. **The Goldfish reviews the diagrams as well as the document.** The comprehension check is given the generated diagram pack with the document. If a fresh session cannot explain the system from the pictures, the pictures are not yet good enough for a human to vet. This is the main reason for adopting EGM: it tests the claim that the diagrams can be understood.
3. **Goldfish review comes before human vetting, never instead of it.** A clean review does not set an item to `vetted`. Only `vockpit approve`, run by the human, does.
4. **The builder is treated as a goldfish.** It receives a handoff card (section 27) and no drafting history. This is Vockpit's own rule, applied in the spirit of EGM. If a builder cannot build a box from its card and spec, the spec is incomplete.
5. **The drift report and `vockpit check` do different jobs.** `vockpit check` is exact and runs on every commit. The drift report is an AI reading that can catch what no rule covers, and can also be wrong. A finding from the drift report becomes a new check rule where possible.
6. **If the host cannot start fresh sessions, the review stops.** It is not imitated inside the Elephant's session.

### What changes in the template

- The EGM plugin is installed by `sdd <name>` and listed in `harness.yaml`, with its version.
- `sdd_lifecycle.md` names the EGM command for each design stage.
- `docs/designs/` is added to the folder structure for approved EGM design documents.
- `handoff.yaml` ships with the Elephant and Goldfish actors (section 27).

---

## 31. Release roadmap

The work is delivered as small releases. Every release goes through the same loop before the next one starts.

### The loop for every release

| Step | What | Done when |
|---|---|---|
| 1. Build | Implement the release scope, and nothing beyond it | Its exit test passes |
| 2. Use | Apply it to Vockpit itself and to one real project in `C:\dev` | A note of what was awkward is written in `docs/feedback/<version>.md` |
| 3. Publish | Push to GitHub, tag the version, update the README and the live demo page | A stranger can follow the README from clone to result |
| 4. Publicise | One post with a short screen recording, linking the demo page | Posted |
| 5. Gather feedback | Collect GitHub issues, comments and your own use notes for a fixed period (two weeks proposed) | Feedback summarised in the same file |
| 6. Decide | Review the scope of the next release against the feedback. Reorder, cut or add, with an ADR if the method changes. | Next release scope written down |

The scopes of releases after 0.1 are proposals. Step 6 may change them.

### Release 0.1: the drill-down map

The first release does one thing: turn a short description of a system into a diagram that can be drilled into, level by level.

**In scope**

| Part | Content |
|---|---|
| Registry | Boxes and edges only: `model/system.yaml` and `model/boxes/*.yaml` (section 7, without the `code` field) |
| Commands | `vockpit init`, `vockpit generate`, `vockpit check`, `vockpit view` |
| Checks | C01, C02, C03, C10, C26 |
| Diagrams | Generated L0, L1 and L2 box diagrams, each node linked to the level below |
| Viewer | One static page: click to zoom in, breadcrumb to zoom out, inspector showing a box's summary, inputs and outputs. Focus held in the page address. |
| One skill | `pack-draft`, structure only: an AI agent reads `brief.md` and writes the registry |
| Example | One small sample system, with its generated diagrams, published as the live demo page |
| Documents | README with a ten-minute quick start, `docs/method.md` (short), licence, changelog |
| Repository | Git, CI running the checks and tests, issue template asking what the user tried to model |

**Out of scope for 0.1**

Tables, screens, flows, technology components, layers, links to code and tests, status colours, fault location, specs and changes, vetting, EGM, hooks, and the template upgrade. All of these remain in the plan and arrive in later releases.

**Why this first**

- It is useful alone: any project gets a navigable map from one small file.
- It is the base that every later view attaches to.
- It can be shown in a thirty-second recording, which is what gets feedback.
- It is small enough to finish: four commands, five checks, one page.

**Exit test**

1. From an empty folder, `vockpit init`, a ten-line brief and `pack-draft` produce a registry that passes `vockpit check`.
2. `vockpit generate` then `vockpit view` shows L0; clicking reaches an L2 box in two clicks; the breadcrumb returns to L0.
3. Editing a generated diagram by hand makes `vockpit check` fail.
4. Each of the five checks fails on its own broken fixture.
5. Vockpit's own structure (section 21) is modelled with it and is the second example.

### Later releases (proposed)

| Release | Adds | Sections | Lets the user |
|---|---|---|---|
| **0.2 Data and flow** | Tables, data domains, flows; ERD and sequence diagrams; viewer lenses that show only what is linked to the focus; table cards | 24 | Open a box and see its tables and its steps in each use case |
| **0.3 UI, technology, layers** | Screens, navigation map, wireframes; technology components; layer diagram and layer rules | 24, 26 | See screen-by-screen navigation and what connects to view, model and database |
| **0.4 Code and tests** | Code symbols and markers, status colours, `vockpit test`, `vockpit locate` | 7, 9, 11 | Trace a failure to a box; see which boxes are built |
| **0.5 Stages and EGM** | Vetting with `vockpit approve`, change from a vetted scope with spec skeletons, EGM plugin for brainstorm, draft and review, handoff diagram and card | 25, 27, 30 | Go from brief to vetted diagrams to specs to build, with fresh-context review |
| **0.6 Harness and template** | `harness.yaml` and its diagram, working hooks, full skill set, upgraded template, `sdd <name>` calling `vockpit init` | 28, 29 | Start any new project with everything in place |
| **1.0** | Fixes from feedback, installable package, complete user guide | 16 | Adopt it without help |

The order after 0.1 follows the request as stated: the views for understanding a system come before the code linkage. If feedback on 0.1 shows more demand for tracing failures to boxes than for more views, 0.4 moves ahead of 0.2.

### Rules that apply from 0.1

Some discipline cannot wait for the release that automates it:

- Git, conventional commits and ADRs from the first commit (sections 14 and 17).
- Tests written before the code of each part (section 18).
- Each release is planned as boxes in Vockpit's own registry, so from 0.1 the tool is drawn with itself.
- Until the spec tooling exists (0.5), each release has one hand-written design note in `docs/designs/`, reviewed before building.

---

## 32. Build specification for release 0.1

The complete, self-contained specification for building release 0.1 is in `docs/designs/0.1-build-spec.md`. It is a separate file on purpose: the agent that builds 0.1 reads that one file and not this whole plan, which keeps its context small and stops it from building later releases early.

It contains the registry format, the five check rules, the diagram rules, the exact D2 output, the viewer's behaviour, the four commands, the sample system, an ordered task list with a commit per task, and the acceptance tests.

To build: open this folder in the coding agent and say, "Read `docs/designs/0.1-build-spec.md` and build it, task by task. Stop and ask if anything is unclear."

Each later release gets its own file in `docs/designs/`, written after the feedback on the release before it.
