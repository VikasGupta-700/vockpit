window.VOCKPIT_MODEL = {
  "diagrams": {
    "L0_context": {
      "title": "L0: Vockpit"
    },
    "L1_system": {
      "title": "L1: Vockpit"
    },
    "L2_checks": {
      "title": "L2: Checks"
    }
  },
  "edges": [
    {
      "data": "User commands",
      "from": "developer",
      "to": "cli"
    },
    {
      "data": "Model files",
      "from": "ai-agent",
      "to": "registry"
    },
    {
      "data": "Init command",
      "from": "cli",
      "to": "scaffold"
    },
    {
      "data": "Check command",
      "from": "cli",
      "to": "checks"
    },
    {
      "data": "Generate command",
      "from": "cli",
      "to": "diagrams"
    },
    {
      "data": "View command",
      "from": "cli",
      "to": "viewer"
    },
    {
      "data": "Starter model",
      "from": "scaffold",
      "to": "registry"
    },
    {
      "data": "Model data",
      "from": "registry",
      "to": "checks"
    },
    {
      "data": "Findings",
      "from": "checks",
      "to": "cli"
    },
    {
      "data": "Model items",
      "from": "registry",
      "to": "diagrams"
    },
    {
      "data": "Diagram objects",
      "from": "diagrams",
      "to": "d2-output"
    },
    {
      "data": "D2 script",
      "from": "d2-output",
      "to": "d2-tool"
    },
    {
      "data": "SVG output",
      "from": "d2-tool",
      "to": "d2-output"
    },
    {
      "data": "Diagram specs",
      "from": "diagrams",
      "to": "viewer-data"
    },
    {
      "data": "SVG data",
      "from": "d2-output",
      "to": "viewer-data"
    },
    {
      "data": "model.js and diagrams.js",
      "from": "viewer-data",
      "to": "viewer"
    },
    {
      "data": "Static HTML and assets",
      "from": "viewer",
      "to": "browser"
    },
    {
      "data": "Rendered diagrams and inspection",
      "from": "viewer",
      "to": "developer"
    },
    {
      "data": "Validated model files",
      "from": "check-schema",
      "to": "check-identity"
    },
    {
      "data": "Verified item IDs",
      "from": "check-identity",
      "to": "check-edges"
    },
    {
      "data": "Valid model graph",
      "from": "check-edges",
      "to": "check-freshness"
    },
    {
      "data": "Valid diagram nodes",
      "from": "check-edges",
      "to": "check-size"
    }
  ],
  "generator": "vockpit 0.1.0",
  "nodes": {
    "ai-agent": {
      "children": [],
      "diagram": "L0_context",
      "id": "ai-agent",
      "inputs": [],
      "kind": "person",
      "level": null,
      "outputs": [],
      "parent": null,
      "summary": "Drafts the model from a brief.",
      "title": "AI Agent"
    },
    "browser": {
      "children": [],
      "diagram": "L0_context",
      "id": "browser",
      "inputs": [],
      "kind": "external",
      "level": null,
      "outputs": [],
      "parent": null,
      "summary": "Displays the viewer.",
      "title": "Browser"
    },
    "check-edges": {
      "children": [],
      "diagram": "L2_checks",
      "id": "check-edges",
      "inputs": [],
      "kind": "box",
      "level": 2,
      "outputs": [],
      "parent": "checks",
      "summary": "Validates that edge endpoints exist and are valid (C03).",
      "title": "Check edges"
    },
    "check-freshness": {
      "children": [],
      "diagram": "L2_checks",
      "id": "check-freshness",
      "inputs": [],
      "kind": "box",
      "level": 2,
      "outputs": [],
      "parent": "checks",
      "summary": "Verifies that diagrams and viewer data match the model (C10).",
      "title": "Check freshness"
    },
    "check-identity": {
      "children": [],
      "diagram": "L2_checks",
      "id": "check-identity",
      "inputs": [],
      "kind": "box",
      "level": 2,
      "outputs": [],
      "parent": "checks",
      "summary": "Ensures IDs are unique and parents are valid L1 boxes (C02).",
      "title": "Check identity"
    },
    "check-schema": {
      "children": [],
      "diagram": "L2_checks",
      "id": "check-schema",
      "inputs": [],
      "kind": "box",
      "level": 2,
      "outputs": [],
      "parent": "checks",
      "summary": "Validates YAML structure, types, and required keys (C01).",
      "title": "Check schema"
    },
    "check-size": {
      "children": [],
      "diagram": "L2_checks",
      "id": "check-size",
      "inputs": [],
      "kind": "box",
      "level": 2,
      "outputs": [],
      "parent": "checks",
      "summary": "Warns if a diagram exceeds recommended node count (C26).",
      "title": "Check size"
    },
    "checks": {
      "children": [
        "check-schema",
        "check-identity",
        "check-edges",
        "check-freshness",
        "check-size"
      ],
      "diagram": "L2_checks",
      "id": "checks",
      "inputs": [
        "Model object"
      ],
      "kind": "box",
      "level": 1,
      "outputs": [
        "Findings"
      ],
      "parent": "vockpit",
      "summary": "Applies the rules.",
      "title": "Checks"
    },
    "cli": {
      "children": [],
      "diagram": "L1_system",
      "id": "cli",
      "inputs": [
        "Command"
      ],
      "kind": "box",
      "level": 1,
      "outputs": [
        "Exit code"
      ],
      "parent": "vockpit",
      "summary": "Parses commands and sets the exit code.",
      "title": "CLI"
    },
    "d2-output": {
      "children": [],
      "diagram": "L1_system",
      "id": "d2-output",
      "inputs": [
        "Diagrams"
      ],
      "kind": "box",
      "level": 1,
      "outputs": [
        "D2 files",
        "SVG files"
      ],
      "parent": "vockpit",
      "summary": "Writes D2 text and calls the D2 tool.",
      "title": "D2 output"
    },
    "d2-tool": {
      "children": [],
      "diagram": "L0_context",
      "id": "d2-tool",
      "inputs": [],
      "kind": "external",
      "level": null,
      "outputs": [],
      "parent": null,
      "summary": "Renders D2 text to SVG.",
      "title": "D2 Tool"
    },
    "developer": {
      "children": [],
      "diagram": "L0_context",
      "id": "developer",
      "inputs": [],
      "kind": "person",
      "level": null,
      "outputs": [],
      "parent": null,
      "summary": "Describes the system and reviews the diagrams.",
      "title": "Developer"
    },
    "diagrams": {
      "children": [],
      "diagram": "L1_system",
      "id": "diagrams",
      "inputs": [
        "Model object"
      ],
      "kind": "box",
      "level": 1,
      "outputs": [
        "Diagrams"
      ],
      "parent": "vockpit",
      "summary": "Decides which nodes and edges each diagram shows.",
      "title": "Diagrams"
    },
    "registry": {
      "children": [],
      "diagram": "L1_system",
      "id": "registry",
      "inputs": [
        "Model files"
      ],
      "kind": "box",
      "level": 1,
      "outputs": [
        "Model object"
      ],
      "parent": "vockpit",
      "summary": "Loads the model files.",
      "title": "Registry"
    },
    "scaffold": {
      "children": [],
      "diagram": "L1_system",
      "id": "scaffold",
      "inputs": [],
      "kind": "box",
      "level": 1,
      "outputs": [
        "Starter project"
      ],
      "parent": "vockpit",
      "summary": "Creates a starter project.",
      "title": "Scaffold"
    },
    "viewer": {
      "children": [],
      "diagram": "L1_system",
      "id": "viewer",
      "inputs": [
        "model.js",
        "diagrams.js"
      ],
      "kind": "box",
      "level": 1,
      "outputs": [],
      "parent": "vockpit",
      "summary": "The page that shows the diagrams.",
      "title": "Viewer"
    },
    "viewer-data": {
      "children": [],
      "diagram": "L1_system",
      "id": "viewer-data",
      "inputs": [
        "Model object",
        "Diagrams",
        "SVG files"
      ],
      "kind": "box",
      "level": 1,
      "outputs": [
        "model.js",
        "diagrams.js"
      ],
      "parent": "vockpit",
      "summary": "Writes the files the viewer loads.",
      "title": "Viewer data"
    },
    "vockpit": {
      "children": [
        "cli",
        "registry",
        "checks",
        "diagrams",
        "d2-output",
        "viewer-data",
        "viewer",
        "scaffold"
      ],
      "diagram": "L1_system",
      "id": "vockpit",
      "inputs": [],
      "kind": "system",
      "level": 0,
      "outputs": [],
      "parent": null,
      "summary": "Turns a description of a system into a diagram that can be drilled into.",
      "title": "Vockpit"
    }
  },
  "system": "vockpit",
  "version": 1
};
