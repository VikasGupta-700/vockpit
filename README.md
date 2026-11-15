# Vockpit

[![CI](https://github.com/VikasGupta-700/vockpit/actions/workflows/ci.yml/badge.svg)](https://github.com/VikasGupta-700/vockpit/actions/workflows/ci.yml)

*You steer. AI builds.*

Vockpit, the Vibe Coding Cockpit, lets you steer an AI-built system from its diagrams instead of its details. Instead of writing complex diagrams by hand or getting lost in source code, you define high-level components ("boxes") and connections ("edges") across three levels in simple YAML files. Vockpit validates the model, generates crisp D2 diagrams, and compiles an interactive single-page viewer where clicking any box zooms into its internals.

---

## Screenshot

```text
+--------------------------------------------------------------------------+
| Vockpit   You steer. AI builds.                                          |
| Context > Online Shop > Orders > Create order              [ Zoom out ]  |
+--------------------------------------------------+-----------------------+
|                                                  | Create order          |
|                                                  | create-order · L2     |
|            diagram (inline SVG)                  | Summary               |
|                                                  | Inputs / Outputs      |
|                                                  | Receives from / Sends |
|                                                  | to                    |
+--------------------------------------------------+-----------------------+
```

---

## Installation

Requirements: Python 3.10+ and [D2](https://d2lang.com) (for SVG rendering).

```bash
git clone https://github.com/vockpit/vockpit.git
cd vockpit
pip install -e .
```

---

## Quick Start

Get started in 5 simple commands:

```bash
# 1. Install editable package
pip install -e .

# 2. Initialise a new project in folder 'demo'
vockpit init demo
cd demo

# 3. Edit brief.md to describe your system, and ask your AI agent to run pack-draft

# 4. Generate the drill-down diagrams and viewer data
vockpit generate

# 5. Open the interactive viewer in your browser
vockpit view
```

---

## Live Demo

Explore the sample online shop demo in [`examples/shop/docs/viewer/index.html`](examples/shop/docs/viewer/index.html).

---

## What 0.1 Does Not Do Yet

Release 0.1 is focused purely on the drill-down map:
- Tables, screens, flows, technology components, and architecture layers are out of scope.
- Code links, test links, live status colors, and fault location are not yet supported.
- Specifications, changes, vetting, and approval workflows will come in future releases.
- Diagram editing from the viewer is not supported (the model is declarative YAML).
- No backend server, database, or user accounts are required.

---

## How to Give Feedback

We would love to hear your feedback! Please open an issue using the [Feedback Template](.github/ISSUE_TEMPLATE/feedback.md) or submit a GitHub Issue describing what you modeled, what worked well, what felt awkward, and what features you need next.
