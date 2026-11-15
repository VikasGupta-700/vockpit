from pathlib import Path
import pytest
from vockpit import cli

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


def test_cli_check_good_and_generate(tmp_path, capsys):
    root = FIXTURES_DIR / "good"

    ret = cli.main(["generate", "--no-svg", "--root", str(root)])
    assert ret == 0
    out, err = capsys.readouterr()
    assert "Generated 4 diagrams." in out

    # check exits 0; may have C10 warnings when d2/SVGs are absent in CI
    ret = cli.main(["check", "--root", str(root)])
    assert ret == 0
    out, err = capsys.readouterr()
    assert "OK" in out
    assert "FAILED" not in out


def test_cli_check_broken_c01(capsys):
    ret = cli.main(["check", "--root", str(FIXTURES_DIR / "broken_c01")])
    assert ret == 1
    out, err = capsys.readouterr()
    assert "C01 ERROR" in out
    assert "FAILED:" in out


def test_cli_check_broken_c02(capsys):
    ret = cli.main(["check", "--root", str(FIXTURES_DIR / "broken_c02")])
    assert ret == 1
    out, err = capsys.readouterr()
    assert "C02 ERROR" in out
    assert "FAILED:" in out


def test_cli_check_broken_c03(capsys):
    ret = cli.main(["check", "--root", str(FIXTURES_DIR / "broken_c03")])
    assert ret == 1
    out, err = capsys.readouterr()
    assert "C03 ERROR" in out
    assert "FAILED:" in out


def test_cli_check_broken_c10(capsys):
    root = FIXTURES_DIR / "broken_c10"
    ret = cli.main(["generate", "--no-svg", "--root", str(root)])
    assert ret == 0
    capsys.readouterr()

    # Hand-edit a .d2 file
    d2_file = root / "docs" / "diagrams" / "L0_context.d2"
    d2_file.write_text(d2_file.read_text(encoding="utf-8") + "\n# hand edited", encoding="utf-8")

    # Run check -> should fail with C10 ERROR only
    ret = cli.main(["check", "--root", str(root)])
    assert ret == 1
    out, err = capsys.readouterr()
    assert "C10 ERROR" in out
    assert "FAILED:" in out


def test_cli_check_broken_c26(capsys):
    root = FIXTURES_DIR / "broken_c26"
    ret = cli.main(["generate", "--no-svg", "--root", str(root)])
    assert ret == 0
    capsys.readouterr()

    # C26 WARN must be present; total warning count may be higher when d2/SVGs absent (C10)
    ret = cli.main(["check", "--root", str(root)])
    assert ret == 0
    out, err = capsys.readouterr()
    assert "C26 WARN" in out
    assert "OK with" in out
    assert "FAILED" not in out
