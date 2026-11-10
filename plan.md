# Vibe Coding Cockpit: Diagram-Based AI Development & Flight Control System

> **Vision**: Transform AI-assisted ("Vibe") coding into a high-reliability **Flight Cockpit**. The developer acts as the aircraft pilot—controlling course, throttle, safety parameters, and decision gates from a high-altitude visual instruments panel, while AI subagent swarms handle low-level implementation.

---

## 1. Concept & Architectural Metaphor: The Pilot's Cockpit

In modern aviation, a pilot does not manually turn every turbine blade, solder electrical relays, or compute aerodynamic lift equations by hand. Instead, the cockpit provides:
1. **Instrument Panel**: High-altitude situational awareness (heading, altitude, fuel, weather).
2. **Flight Controls & Levers**: Autopilot toggles, throttle levers, flaps, trim, and landing gear controls.
3. **Emergency Circuit Breakers & Warning Horns**: Stall warnings, collision avoidance (TCAS), and automated abort gates.
4. **Flight Data Recorder (Black Box)**: Tamper-proof, immutable flight logs for post-flight safety audits.

### Translating Aviation to "Vibe Coding Cockpit"

```
+---------------------------------------------------------------------------------------------------+
|                                 VIBE CODING COCKPIT (PILOT UI)                                     |
+---------------------------------------------------------------------------------------------------+
|  [Flight Instrument Panel]                                                                        |
|  * Interactive D2 System Architecture Flow (Vector Zoom/Pan Canvas)                               |
|  * Real-Time Telemetry Overlay (Active Node Latency, Token Burn Rate, Cost/Minute)                 |
|                                                                                                   |
|  [Flight Controls & Levers]                                                                       |
|  * Model Routing Lever: [Prebuilt MCP Tool] <===> [Edge SLM (Phi-4)] <===> [Frontier LLM (GPT-4o)] |
|  * Throttle & Quota Lever: [Serverless Pay-As-You-Go] <===> [PTU Reserved Pool (50k TPM)]         |
|  * Hallucination Guardrail Knob: Similarity Threshold [ 0.70 ... 0.95 ]                           |
|  * Autopilot Disengage / HITL Gate: Manual Approval Required for Financial / Destructive Actions   |
|                                                                                                   |
|  [Navigation & Subagent Crew]                                                                     |
|  * Co-Pilot (Architect Agent) -> Navigator (Planner Agent) -> Flight Engineers (Coder Swarm)      |
|                                                                                                   |
|  [Black Box Flight Recorder]                                                                      |
|  * SHA-256 Provenance Hashes + Immutable WORM Audit Logs in Azure Blob Storage                    |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
                        +---------------------------------------------------+
                        |         BIDIRECTIONAL DIAGRAM-TO-CODE SYNC        |
                        +---------------------------------------------------+
                        |  Declarative Diagram Spec (.d2 / .json)           |
                        |                    ▲                              |
                        |                    │ Code-Linked Anchors          |
                        |                    ▼                              |
                        |  Target Codebase (Python / JS / REST APIs / DBs)  |
                        +---------------------------------------------------+
```

---

## 2. Recommended Project Directory & Foundation

Based on your established local workspace standards in `C:\dev\`, the canonical directory for this new project is:

```text
C:\dev\2026-Nov-10-Vibe-Coding-Cockpit\
```

### Why this location?
1. **Consistency**: Matches your established date-indexed naming schema (`2026-Oct-11-AI-103`, `2026-Oct-30-StudyIQ-Rakshit`, `2026-May-20-Angel1-Trading-Signal-Dashboard`).
2. **Isolation & Independence**: A pristine, dedicated workspace with its own Git repository, virtual environment, and CI/CD pipelines—unencumbered by legacy lab exercises.
3. **Launch & Open-Source Readiness**: Cleanly partitioned for eventual push to GitHub (`https://github.com/<user>/vibe-coding-cockpit`) and deployment to GitHub Pages for community demonstration.

---

## 3. Canonical Project Structure

```text
C:\dev\2026-Nov-10-Vibe-Coding-Cockpit/
├── goals/
│   └── tasks.md                      # Living chronological task board [x], [/], [ ]
├── docs/
│   ├── index.html                    # GitHub Pages Ready Single-Click Cockpit Dashboard
│   ├── architecture.md               # End-to-end Cockpit System Architecture
│   ├── modules.md                    # Core Cockpit Engine API & Module Specifications
│   ├── diagrams/                     # High-definition D2 & SVG Cockpit Diagrams
│   │   ├── cockpit_control_flow.svg  # Flight Instruments & Levers Topology
│   │   ├── decision_matrix.svg       # Multi-Gate Routing & Circuit Breakers
│   │   └── subagent_hierarchy.svg    # Co-Pilot & Specialist Swarm Hierarchy
│   └── templates/                    # Universal Diagram & Decision Templates
│       ├── architecture_template.d2
│       ├── decision_gate_template.md
│       └── cockpit_viewer_template.html
├── cockpit/                          # Core Engine & Flight Levers
│   ├── __init__.py
│   ├── controller.py                 # Master Pilot Flight Controller
│   ├── levers/                       # Modular Flight Control Levers
│   │   ├── router_lever.py           # Tool vs SLM vs Frontier LLM Triage
│   │   ├── quota_throttle_lever.py   # PTU / Rate Limit / Backoff Jitter Governor
│   │   ├── safety_shield_lever.py    # Jailbreak / Content Safety / Grounding Guardrails
│   │   └── hitl_pause_lever.py       # Human-in-the-Loop Approval & State Suspension
│   ├── telemetry/                    # Flight Instrument Telemetry Streamer
│   │   ├── otel_tracer.py            # OpenTelemetry GenAI Span Collector
│   │   └── cost_calculator.py        # Token & USD Burn Rate Meter
│   └── sync/                         # Diagram-to-Code Synchronizer
│       ├── d2_parser.py              # Bidirectional D2 Ast Parser & Code Linker
│       └── code_generator.py         # Scaffolding Code Harnesses from Visual Gates
├── swarms/                           # Co-Pilot & Autonomous Crew (AGM / Subagents)
│   ├── copilot_agent.py              # Lead Co-Pilot (Architectural Supervision)
│   ├── navigator_agent.py            # Route & Task Planner (Taskboard Maintainer)
│   └── engineer_agents/              # Worker Specialists (Backend, Frontend, Tester)
├── web/                              # Standalone Generative UI Cockpit Webapp
│   ├── index.html                    # Interactive Flight Deck with Visual Instruments
│   ├── css/cockpit.css               # Modern Aviation-Inspired Dark Deck Styling
│   └── js/
│       ├── cockpit_deck.js           # Zoom/Pan, Levers Dispatcher, Telemetry Gauges
│       └── visual_sync.js            # Diagram Node Highlighter & State Animator
├── AGENTS.md                         # Project-specific AI guidelines & pilot constraints
├── .gitignore                        # Clean standard git ignore
└── README.md                         # Public GitHub README with hero visuals & video plan
```

---

## 4. The 6 Core "Flight Levers" in the Cockpit

| Lever | Aviation Analog | Software / AI Function | Code Anchor |
|---|---|---|---|
| **1. Model Routing Lever** | Engine Throttle / Fuel Mix | Dynamically switches between **Prebuilt MCP Tools** ($0.0001), **Edge SLMs (Phi-4)** (<150ms), and **Frontier LLMs (GPT-4o)** for deep reasoning. | `cockpit/levers/router_lever.py` |
| **2. Quota & Throttle Governor** | Airspeed / Pitot Limiter | Automatically switches between **Serverless Consumption** and **PTU Pools**, managing HTTP 429 backoff with full jitter to avoid service stalls. | `cockpit/levers/quota_throttle_lever.py` |
| **3. Grounding & Refusal Knob** | Terrain Avoidance (GPWS) | Adjusts cosine similarity cut-off (0.70 to 0.95). Refuses out-of-scope speculation when groundedness drops below safety threshold. | `cockpit/levers/safety_shield_lever.py` |
| **4. Safety & Prompt Shield** | Cabin Fire Suppression | Intercepts adversarial jailbreak patterns ("Ignore prior rules") and content safety violations before prompts reach execution engines. | `cockpit/levers/safety_shield_lever.py` |
| **5. HITL Autopilot Disengage** | Manual Flight Override | Suspends autonomous agent loops in state `requires_action` for high-risk actions (financial transfers, schema drops) until manager JWT sign-off. | `cockpit/levers/hitl_pause_lever.py` |
| **6. Black Box Provenance Seal** | Flight Data Recorder | Writes SHA-256 cryptographic provenance seals to Immutable WORM storage for 100% regulatory auditability. | `cockpit/telemetry/cost_calculator.py` |

---

## 5. Bidirectional Diagram-Driven Development (DDD) Engine

The Cockpit solves the disconnect between architecture diagrams and reality:

1. **Forward Engineering (Diagram $\to$ Code)**:
   - The pilot defines a decision tree in declarative D2 syntax.
   - The Cockpit engine parses the gates and scaffolds the Python functions, route handlers, and unit test assertions automatically.
2. **Reverse Traceability (Code $\to$ Diagram)**:
   - When inspecting any node on the visual flight deck, clicking it immediately opens the exact code file and line number (`file://...#Lxx`).
3. **Live In-Flight Telemetry (Runtime $\to$ Diagram)**:
   - While tests or live workloads run, the diagram nodes glow:
     - 🟢 **Green**: Active flow, healthy latency (< 200ms), verified safety pass.
     - 🟡 **Yellow**: Throttled flow, exponential retry active, or SLM fallback engaged.
     - 🔴 **Red**: Safety shield trip, hallucination cut-off triggered, or HITL approval required.

---

## 6. Implementation & Launch Roadmap

### Phase 1: Workspace Scaffolding & Foundational Setup
- Initialize `C:\dev\2026-Nov-10-Vibe-Coding-Cockpit`.
- Initialize Git repository, configure language-appropriate `.gitignore`, and establish `AGENTS.md`.
- Set up lightweight Python virtual environment (`.venv`) with Azure AI SDK, OpenTelemetry, D2 compiler tooling, and FastAPI.

### Phase 2: Core Flight Levers & Engine Implementation
- Implement the 6 modular flight control levers in `cockpit/levers/`.
- Build the telemetry collector (`otel_tracer.py`, `cost_calculator.py`).
- Implement the bidirectional D2 parser and code linker.

### Phase 3: Interactive Flight Deck UI (Single-Click Webapp)
- Build `web/index.html` (and copy to `docs/index.html` for GitHub Pages).
- Implement full-screen mouse-roller zooming (0.10x to 5.0x), center-anchored drag-to-pan, and double-click auto-fit.
- Embed interactive sliders and toggle switches for the 6 flight levers.
- Implement live state animation on the SVG diagram canvas.

### Phase 4: Reference System Showcase Demos
- Wire up the 3 proven reference topologies into the Cockpit:
  1. **Azure Generative AI Enterprise Hub** (from AI-103).
  2. **StudyIQ Adaptive Spaced Repetition Platform** (from StudyIQ-Rakshit).
  3. **Minervini SEPA High-Growth Trading Engine** (from Angel One Dashboard).

### Phase 5: GitHub Publication, Presentation Deck & Video Launch Kit
- Create presentation slides deck (`docs/slides/vibe_coding_cockpit.md`) for YouTube / LinkedIn announcement.
- Build demonstration script showing how a developer steers an AI swarm from the Cockpit.
- Finalize GitHub repository documentation, badges, and automated GitHub Pages deployment.
