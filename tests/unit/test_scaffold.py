from pathlib import Path
from vockpit import cli, scaffold


def test_init_and_check(tmp_path, capsys):
    target = tmp_path / "my_project"

    # First init: creates files and generates output
    ret = cli.main(["init", str(target)])
    assert ret == 0
    out, _ = capsys.readouterr()
    assert "created model/system.yaml" in out
    assert "created brief.md" in out

    # Files must exist
    assert (target / "model" / "system.yaml").is_file()
    assert (target / "model" / "boxes" / ".gitkeep").is_file()
    assert (target / "brief.md").is_file()
    assert (target / ".claude" / "skills" / "pack-draft" / "SKILL.md").is_file()
    assert (target / ".agent" / "skills" / "pack-draft" / "SKILL.md").is_file()
    assert (target / "docs" / "viewer" / "index.html").is_file()

    # Check must exit 0 and print OK (may have C10 WARN if d2/SVGs absent in CI)
    ret = cli.main(["check", "--root", str(target)])
    assert ret == 0
    out, _ = capsys.readouterr()
    assert "OK" in out
    assert "FAILED" not in out

    # Second init in the same folder: skips every file, does not run generate
    ret = cli.main(["init", str(target)])
    assert ret == 0
    out, _ = capsys.readouterr()
    assert "skip model/system.yaml (exists)" in out
    assert "skip brief.md (exists)" in out
    assert "Generated" not in out


def test_view_command(tmp_path, capsys):
    target = tmp_path / "view_project"
    # Before generate: view exits 2 with Run "vockpit generate" first.
    target.mkdir()
    ret = cli.main(["view", "--root", str(target), "--no-open"])
    assert ret == 2
    out, _ = capsys.readouterr()
    assert 'Run "vockpit generate" first.' in out

    # Init project
    cli.main(["init", str(target)])
    capsys.readouterr()

    # View with unknown id -> exits 2
    ret = cli.main(["view", "nonexistent-id", "--root", str(target), "--no-open"])
    assert ret == 2
    out, _ = capsys.readouterr()
    assert "No item with id 'nonexistent-id'." in out

    # View with valid id -> prints file:// ending in #/<id>
    ret = cli.main(["view", "core", "--root", str(target), "--no-open"])
    assert ret == 0
    out, _ = capsys.readouterr()
    assert "file://" in out
    assert "#/core" in out
