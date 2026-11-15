from pathlib import Path

import yaml

from vockpit import analyze, checks, cli, registry


def _write(root: Path, rel: str, text: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def make_shop(root: Path) -> Path:
    """Single package under src/ -> analyzer descends one level."""
    _write(root, "src/shop/__init__.py", '"""Shop."""\n')
    _write(root, "src/shop/orders/__init__.py", '"""Order handling."""\n')
    _write(
        root,
        "src/shop/orders/service.py",
        '"""Order service."""\n'
        "import requests\n"
        "from shop.orders import repo\n\n\n"
        "class OrderService:\n"
        "    def create(self):\n"
        "        return repo\n\n\n"
        "def helper():\n"
        "    pass\n",
    )
    _write(root, "src/shop/orders/repo.py", '"""Order storage."""\n')
    _write(
        root,
        "src/shop/billing.py",
        '"""Billing."""\nimport json\nfrom shop.orders.service import OrderService\n',
    )
    _write(root, "src/shop/broken.py", "def (:\n")
    _write(root, "tests/test_x.py", "def test_x():\n    pass\n")
    _write(root, ".venv/lib/skipme.py", "x = 1\n")
    return root


def make_multi(root: Path) -> Path:
    """Two packages, no src/ -> no descent."""
    _write(root, "alpha/__init__.py", '"""Alpha."""\n')
    _write(root, "alpha/a_one.py", "from beta import b_one\nfrom . import a_two\n")
    _write(root, "alpha/a_two.py", "")
    _write(root, "beta/__init__.py", "")
    _write(root, "beta/b_one.py", '"""Beta one."""\n')
    _write(root, "data_tools/__init__.py", "")
    _write(root, "data_tools/2fast.py", "import alpha.a_one\n")
    return root


def test_analyze_skips_noise_and_records_warnings(tmp_path):
    a = analyze.analyze(make_shop(tmp_path / "shop"))
    paths = {m.path for m in a.modules}
    assert "src/shop/orders/service.py" in paths
    assert not any(".venv" in p or p.startswith("tests/") for p in paths)
    assert "src/shop/broken.py" not in paths
    assert any("broken.py" in w for w in a.warnings)
    assert a.test_files == 1


def test_analyze_descends_into_single_package(tmp_path):
    a = analyze.analyze(make_shop(tmp_path / "shop"))
    assert [u.id for u in a.units] == ["billing", "orders"]
    orders = next(u for u in a.units if u.id == "orders")
    assert sorted(orders.children) == ["orders-repo", "orders-service"]
    assert orders.summary == "Order handling."


def test_analyze_edges(tmp_path):
    a = analyze.analyze(make_shop(tmp_path / "shop"))
    assert ("billing", "orders") in a.l1_edges
    assert ("orders", "billing") not in a.l1_edges
    assert ("orders-service", "orders-repo") in a.l2_edges
    assert a.external["requests"] == 1
    assert "json" not in a.external


def test_analyze_no_descent_and_id_sanitising(tmp_path):
    a = analyze.analyze(make_multi(tmp_path / "multi"))
    assert [u.id for u in a.units] == ["alpha", "beta", "data-tools"]
    dt = next(u for u in a.units if u.id == "data-tools")
    assert list(dt.children) == ["data-tools-2fast"]
    alpha = next(u for u in a.units if u.id == "alpha")
    assert sorted(alpha.children) == ["alpha-a-one", "alpha-a-two"]
    assert ("alpha", "beta") in a.l1_edges
    assert ("data-tools", "alpha") in a.l1_edges
    assert ("alpha-a-one", "alpha-a-two") in a.l2_edges


def test_generated_model_is_valid(tmp_path):
    root = make_shop(tmp_path / "shop")
    a = analyze.analyze(root)
    files = analyze.build_model_files(a)
    assert set(files) == {"model/system.yaml", "model/boxes/orders.yaml"}
    for rel, text in files.items():
        _write(root, rel, text)
    assert [f for f in registry.validate_c01(root) if f.severity == "ERROR"] == []
    model, _ = registry.load(root)
    assert model is not None
    assert not [f for f in checks.check_c02(root, model) if f.severity == "ERROR"]
    assert not [f for f in checks.check_c03(model) if f.severity == "ERROR"]
    data = yaml.safe_load(files["model/system.yaml"])
    billing = next(b for b in data["boxes"] if b["id"] == "billing")
    assert billing["code"] == ["src/shop/billing.py"]


def test_report_contents(tmp_path):
    a = analyze.analyze(make_shop(tmp_path / "shop"))
    report = analyze.render_report(a)
    assert report.startswith("# Structure report: shop")
    for heading in ("## Overview", "## Structure", "## Dependencies", "## Warnings"):
        assert heading in report
    assert "requests" in report
    assert "src/shop/orders/service.py" in report


def test_cli_analyze_writes_and_refuses_overwrite(tmp_path, capsys):
    root = make_shop(tmp_path / "shop")
    assert cli.main(["analyze", str(root)]) == 0
    assert (root / "model" / "system.yaml").is_file()
    assert (root / "model" / "boxes" / "orders.yaml").is_file()
    assert (root / "docs" / "analysis.md").is_file()
    capsys.readouterr()

    assert cli.main(["analyze", str(root)]) == 1
    out, _ = capsys.readouterr()
    assert "--force" in out

    assert cli.main(["analyze", str(root), "--force"]) == 0
    assert cli.main(["check", "--root", str(root)]) in (0, 1)


def test_cli_analyze_bad_path_and_empty(tmp_path):
    assert cli.main(["analyze", str(tmp_path / "nope")]) == 2
    empty = tmp_path / "empty"
    empty.mkdir()
    assert cli.main(["analyze", str(empty)]) == 1
