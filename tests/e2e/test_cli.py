from pathlib import Path
import pytest
from vockpit import cli

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


def test_cli_check_good_and_generate(tmp_path, capsys):
    # First test that good fixture with generate passes check
    root = FIXTURES_DIR / "good"

    # Run generate in good fixture with --no-svg if d2 is not available, or with d2
    ret = cli.main(["generate", "--root", str(root)])
    assert ret == 0
    out, err = capsys.readouterr()
    assert "Generated 4 diagrams." in out

    # Now check should exit 0 with OK
    ret = cli.main(["check", "--root", str(root)])
    assert ret == 0
    out, err = capsys.readouterr()
    assert out.strip().endswith("OK")


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
    # Generate into broken_c10
    ret = cli.main(["generate", "--root", str(root)])
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
    # Generate into broken_c26
    ret = cli.main(["generate", "--root", str(root)])
    assert ret == 0
    capsys.readouterr()

    # Run check -> should exit 0 with OK with 1 warning(s)
    ret = cli.main(["check", "--root", str(root)])
    assert ret == 0
    out, err = capsys.readouterr()
    assert "C26 WARN" in out
    assert "OK with 1 warning(s)" in out.strip()
