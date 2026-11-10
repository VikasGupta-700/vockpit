# Vibe Coding Cockpit — Fable Plan (Draft 1)

| | |
|---|---|
| **Date** | 2026-11-10 |
| **Status** | Draft 1, awaiting review. Nothing in this plan has been built yet. |
| **Supersedes** | `plan.md` (kept unchanged for reference) |
| **Workspace** | `C:\dev\2026-Nov-10-Vibe-Coding-Cockpit` |

---

## 1. Goal

Build a development system in which software is designed, built, tested and debugged **one diagram box at a time**, and in which any problem can be traced to the exact box, at the exact diagram level, where it lives.

The Cockpit is a method plus a small toolset. It is meant to be dropped into any project and used by any developer or AI coding agent.

### What it must do

1. Describe a system as a hierarchy of boxes: a high-level scaffold, broken down level by level.
2. Tie every box to a specification, the code that implements it, and the tests that prove it.
3. Let a developer build one box, test that box alone, then integrate it with its neighbours.
4. Given a failing test, a stack trace, or a file and line, say which box is at fault and show its path through the levels.
5. Refuse to pass when a diagram, a spec, the code and the tests disagree.

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
8. **Prove before packaging.** The method is used to build the Cockpit itself, then one real project, before any public launch work.

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
│   └── boxes/
│       └── <l1-box-id>.yaml      # One file per subsystem: its L2 boxes and edges
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
├── src/cockpit/                  # THE TOOL (built with its own method)
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
│   ├── user-guide.md             # How to use the Cockpit on a project
│   ├── method.md                 # The box-by-box method, tool-independent
│   ├── diagrams/                 # GENERATED. Do not edit.
│   │   ├── L0_context.d2 / .svg
│   │   ├── L1_system.d2 / .svg
│   │   └── L2_<l1-box-id>.d2 / .svg
│   ├── viewer/
│   │   ├── index.html            # Interactive viewer
│   │   └── model.json            # GENERATED viewer data
│   └── decisions/
│       ├── README.md             # Index of decisions; when an ADR is required
│       ├── NNNN-<slug>.md        # One ADR per significant decision
│       └── log.md                # One-line entries for small decisions
│
├── templates/                    # Copied into other projects by `cockpit init`
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
│   └── ISSUE_TEMPLATE/bug.md     # Requires a box ID or `cockpit locate` output
│
└── .cockpit/                     # Local working files, not committed
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
      - cockpit.check.symbols:check_symbols     # module:function
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

The marker lets `cockpit locate` work from a line of code, and lets the logging helper tag log records. A check confirms the marker and the registry agree in both directions.

---

## 8. Diagram policy

| Diagram | When required | How produced | Where |
|---|---|---|---|
| L0 Context | Always | Generated | `docs/diagrams/L0_context.d2` |
| L1 System | Always | Generated | `docs/diagrams/L1_system.d2` |
| L2 Component, one per L1 box | Always | Generated | `docs/diagrams/L2_<id>.d2` |
| Sequence diagram | A box coordinates three or more others, or ordering matters | Hand-written D2 | `openspec/specs/<box-id>/behaviour.d2` |
| State diagram | A box has named states and transitions | Hand-written D2 | Same |
| Data model (ERD) | A box owns stored data | Hand-written D2 or Mermaid | Same |
| Decision gate table | `decision_gate: true` | Section in `spec.md` from template | Spec |

Rules:

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

1. Run `cockpit locate` with the failing test name, the stack trace, or `file:line`.
2. The tool prints the box and its path, for example `cockpit > check > check-symbols`, with links to the spec, code and tests.
3. Run `cockpit test <box-id>` to test that box alone.
4. If the box passes alone, run the integration tests on its edges. The fault is on an edge or in a neighbour.
5. If nothing at that level fails, move up one level and repeat.
6. Every bug report records the box ID. A fix starts by adding a failing test to that box.

---

## 12. Commands and checks

### Commands

| Command | Purpose |
|---|---|
| `cockpit init` | Add the folder structure, templates and agent rules to a project |
| `cockpit new box <id> --parent <id>` | Add a box to the registry and create its spec from the template |
| `cockpit new change <slug>` | Create the next numbered change workspace |
| `cockpit new adr <title>` | Create the next numbered ADR |
| `cockpit generate` | Produce diagrams, viewer data and `modules.md` from the registry |
| `cockpit check` | Run every consistency rule; non-zero exit on any failure |
| `cockpit status [box-id]` | Show lifecycle status for all boxes or one |
| `cockpit test <box-id>` | Run the unit tests of one box; `--edges` adds its integration tests |
| `cockpit locate <target>` | Map a file and line, test name or stack trace to a box path |
| `cockpit prompt <box-id>` | Print a `@box-change` card with spec, code and test locations for an AI agent |

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

Each rule has a fixture project in `tests/fixtures/broken_*` that must fail that rule and no other. This is how the checker itself is proven to work.

---

## 13. Logging

Two kinds of logging are covered.

### Logging by the Cockpit tool

- Structured JSON, one record per line, written to `.cockpit/logs/<date>.jsonl`. Human-readable summary on the console.
- Fields: `ts` (UTC), `level`, `run_id`, `command`, `box_id` when applicable, `event`, `detail`.
- Every check finding is logged with its rule ID and box ID.
- Log files are not committed.

### Logging in projects that use the Cockpit

- `cockpit.logging` provides a logger that adds `box_id` (from the `@box` marker) and a correlation ID to every record.
- Required events for a leaf box: entry with input summary, each decision taken with its reason, exit with outcome, and any error with the exception.
- Levels: DEBUG for internals, INFO for decisions and outcomes, WARNING for recoverable problems, ERROR for failures.
- Secrets, tokens and personal data are never logged. A check in the pre-commit hook scans for common secret patterns.
- Because every record carries `box_id`, a log line from a failure can be passed to `cockpit locate` directly.

---

## 14. Version control

| Topic | Rule |
|---|---|
| Repository | `git init` in Phase 0. Default branch `main`. |
| Branches | One branch per change: `change/NNN-<slug>`. No direct commits to `main` after Phase 0. |
| Commits | Conventional Commits. The scope is the box ID: `feat(check-symbols): resolve dotted class paths`. |
| Trailers | `Change: NNN` on every commit. `ADR: NNNN` when a commit implements a decision. |
| Granularity | One commit per box status transition where practical. |
| Pre-commit hook | Runs `cockpit check`, the unit tests for boxes whose files changed, and the secret scan. |
| Merge | Only when `cockpit check` and the full test suite pass. The PR template asks for the change number, boxes touched and ADRs. |
| Tags | `v0.N.0` at the end of each phase. |
| CI | GitHub Actions on every push: install, check, test, regenerate and compare. |
| Ignore | `.venv/`, `.cockpit/`, `__pycache__/`, `.env`, editor folders. |
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
| `.agent/hooks.json` | Antigravity hooks: after an edit, run `cockpit check` and the touched box's tests. |
| `.claude/settings.json` | Claude Code hooks doing the same, plus a pre-write secret scan that really scans. |

### Hard rules for agents

1. Do not write code under `src/` without an active change.
2. Do not edit files under `docs/diagrams/` or `docs/viewer/model.json`.
3. Work on one box per task. Finish its tests before starting another.
4. Do not store line numbers anywhere.
5. Do not report "verified" unless `cockpit check` and the relevant tests ran in this session and passed. Quote the output.
6. Record a decision (section 17) whenever a choice between alternatives is made.
7. After each task, report: what was built, inputs and outputs, where a human can steer, and the test output.

### Project skills (`.claude/skills/`)

| Skill | Does |
|---|---|
| `box-scaffold` | Break a box into children: update the registry, create specs, regenerate, show the diagram for review |
| `box-spec` | Write or revise a box's spec with requirement IDs and scenarios |
| `box-build` | Take one box from `specified` to `green`: stub, failing tests, implementation, commit |
| `box-integrate` | Write and pass integration tests for the edges of a box |
| `box-locate` | Given a failure, run `cockpit locate`, isolate the box, propose a failing test |
| `change-open` | Create a change workspace and its branch |
| `change-close` | Run checks, merge spec changes, archive, update the changelog |
| `adr-new` | Record a decision using the template and update the index |
| `diagram-sync` | Regenerate diagrams and report what changed |

Each skill is a short instruction file that calls the `cockpit` commands. The skills hold no logic of their own, so the same method works in any agent that can run a command.

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

### Phase 0 — Foundation

- `git init`, `.gitignore`, `.gitattributes`, `pyproject.toml`, virtual environment.
- Create the folder structure in section 6 (empty where content comes later).
- Write `AGENTS.md`, `CLAUDE.md`, the six rule files, `README.md` skeleton.
- Copy and adapt templates from the sources in section 5.
- Write ADRs 0001 to 0010.
- Evaluate `engineering-spec:init-spec` and the OpenSpec tool; record in ADR 0006.
- Declare the Cockpit's own L0 and L1 boxes in `model/system.yaml` by hand (section 21).
- **Exit test:** repository exists with one commit; folder tree matches section 6; ten ADRs present.
- **Tag:** `v0.0.0`

### Phase 1 — Registry and checks

- Boxes: `registry-load`, `registry-validate`, `resolve-symbols`, `resolve-tests`, `check-*` for rules C01 to C09 and C12 to C15, `cli`.
- Good and broken fixture projects.
- **Exit test:** `cockpit check` passes on the good fixture, and each broken fixture fails exactly its own rule. `cockpit check` passes on the Cockpit itself.
- **Tag:** `v0.1.0`

### Phase 2 — Generation and viewer

- Boxes: `generate-d2`, `generate-svg`, `generate-viewer-data`, `generate-modules-doc`, rules C10 and C11.
- Adapt the viewer to load `model.json`; add level drill-down and the inspector showing spec, code and test links.
- **Exit test:** the Cockpit's own L0, L1 and L2 diagrams are generated and open in the viewer; editing a generated file makes `cockpit check` fail.
- **Tag:** `v0.2.0`

### Phase 3 — Status, per-box testing and fault location

- Boxes: `status-compute`, `test-run`, `locate-file`, `locate-test`, `locate-trace`, `prompt-card`, `logging-helper`.
- Status colours in generated diagrams.
- **Exit test:** a fault deliberately placed in one box is traced to that box by `cockpit locate` from the stack trace alone; `cockpit test <box>` runs only that box's tests.
- **Tag:** `v0.3.0`

### Phase 4 — Agent workflow

- Boxes: `scaffold-init`, `scaffold-box`, `scaffold-change`, `scaffold-adr`.
- The nine skills, working hooks in `.claude/settings.json` and `.agent/hooks.json`, pre-commit hook, CI workflow, issue and PR templates.
- **Exit test:** an agent, given only "add box X", completes the full loop from change to archive with all checks passing and no manual correction.
- **Tag:** `v0.4.0`

### Phase 5 — Pilot on HelloWorld-SDD

- Run `cockpit init` there. Put it under version control. Remove the duplicate `service.py`. Move its boxes into a registry. Replace the hand-typed studio data with generated data.
- Complete its open task (time-of-day greeting) using the method.
- **Exit test:** `cockpit check` passes there; the mismatches listed in section 2 are gone.

### Phase 6 — Pilot on one real project

- Apply to `2026-May-20-Angel1-Trading-Signal-Dashboard` (smallest existing documentation, real code).
- Record every point where the method was awkward. Fix the tool or the method, with ADRs.
- **Exit test:** one real bug or feature in that project handled end to end with the method.
- **Tag:** `v0.5.0`

### Phase 7 — Packaging for others

- Installable package, complete user guide, worked example, `cockpit init` tested on an empty folder and on an existing project.
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
| GitHub Pages, slides, video kit | Deferred | After Phase 7 |
| Aviation naming | Optional | May be used for viewer styling only |

---

## 21. Starting scaffold: the Cockpit's own boxes

**L0:** `cockpit` — used by a Developer and an AI Agent; reads a Project Repository; calls the D2 tool, Git and pytest.

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
| `logging` | Structured logs with box ID | all | `.cockpit/logs/` |

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

---

## 23. Points to confirm

1. **File name.** This plan is saved as `fable-plan.md`, and `plan.md` is left untouched. Say if `plan.md` should be replaced instead.
2. **"AGM directory."** Read as the `.agent/` folder together with `AGENTS.md`. Correct this if something else was meant.
3. **Diagram levels.** Three structural levels plus sequence and state diagrams where needed. Full UML (class, activity, deployment diagrams) is not planned. Confirm or extend.
4. **Agents to support.** Both Antigravity (`.agent/`) and Claude Code (`.claude/`) are covered. Say if only one is needed.
5. **First language.** Python only at first.
6. **Second pilot.** Angel1 Trading Signal Dashboard is proposed for Phase 6.
7. **Duplicate folder.** `C:\dev\2026-NOV-10-VIBE-cooling-cockpit` holds a copy of `plan.md`. It has not been touched.
