from pathlib import Path
from vockpit import checks, registry

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


def test_good_fixture_has_no_findings():
    root = FIXTURES_DIR / "good"
    findings = checks.run_model_checks(root)
    # C10 (SVG freshness) requires d2 to have been run; exclude it so CI passes without d2
    non_freshness = [f for f in findings if f.rule != "C10"]
    assert non_freshness == []


def test_broken_c01_fixture():
    root = FIXTURES_DIR / "broken_c01"
    findings = checks.run_model_checks(root)
    assert len(findings) > 0
    assert all(f.rule == "C01" for f in findings)


def test_broken_c02_fixture():
    root = FIXTURES_DIR / "broken_c02"
    findings = checks.run_model_checks(root)
    assert len(findings) > 0
    assert all(f.rule == "C02" for f in findings)


def test_broken_c03_fixture():
    root = FIXTURES_DIR / "broken_c03"
    findings = checks.run_model_checks(root)
    assert len(findings) > 0
    assert all(f.rule == "C03" for f in findings)


def test_c02_parent_not_l1(tmp_path):
    model_dir = tmp_path / "model"
    model_dir.mkdir(parents=True)
    (model_dir / "system.yaml").write_text(
        """system:
  id: shop
  title: Online Shop
  summary: Sells online.
boxes:
  - id: storefront
    title: Storefront
    summary: Web shop.
""",
        encoding="utf-8",
    )
    boxes_dir = model_dir / "boxes"
    boxes_dir.mkdir()
    (boxes_dir / "other.yaml").write_text(
        """parent: other
boxes:
  - id: something
    title: Something
    summary: Desc.
""",
        encoding="utf-8",
    )
    findings = checks.run_model_checks(tmp_path)
    assert any(f.rule == "C02" and "not an L1 box" in f.message for f in findings)


def test_c03_edge_system_id_or_self():
    from vockpit.registry import System, Actor, Box, Edge, Model
    sys = System("shop", "Shop", "Desc")
    actor = Actor("customer", "Customer", "person")
    box = Box("orders", "Orders", "Desc", level=1, parent="shop")
    edge1 = Edge("shop", "orders", "Data", "model/system.yaml")
    edge2 = Edge("orders", "orders", "Loop", "model/system.yaml")
    model = Model(sys, [actor], [box], [edge1, edge2])

    findings = checks.check_c03(model)
    assert any(f.rule == "C03" and "uses system id" in f.message for f in findings)
    assert any(f.rule == "C03" and "self-referencing" in f.message for f in findings)

