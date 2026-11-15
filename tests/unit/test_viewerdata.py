from pathlib import Path

from vockpit import diagrams, registry, viewerdata

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


def test_build_model_js_matches_expected():
    root = FIXTURES_DIR / "good"
    model, _ = registry.load(root)
    assert model is not None

    diags = diagrams.build(model)
    model_js = viewerdata.build_model_js(model, diags)

    expected_path = root / "expected_model.js"
    expected_content = expected_path.read_text(encoding="utf-8")

    # Normalize line endings
    assert model_js.replace("\r\n", "\n") == expected_content.replace("\r\n", "\n")


def test_build_diagrams_js():
    no_svg = viewerdata.build_diagrams_js(None)
    assert no_svg.strip() == "window.VOCKPIT_SVG = {};"

    svg_map = {"L0_context": "<svg>test</svg>"}
    with_svg = viewerdata.build_diagrams_js(svg_map)
    assert "window.VOCKPIT_SVG = {" in with_svg
    assert '"L0_context": "<svg>test</svg>"' in with_svg
