from __future__ import annotations

from pathlib import Path
import shutil

from vockpit import d2


def init_project(target: Path) -> int:
    target = target.resolve()
    target.mkdir(parents=True, exist_ok=True)

    assets_init = Path(__file__).parent / "assets" / "init"
    sys_yaml_dest = target / "model" / "system.yaml"
    sys_yaml_existed = sys_yaml_dest.is_file()

    files_to_create: list[tuple[str, Path | str]] = [
        ("model/system.yaml", assets_init / "system.yaml"),
        ("model/boxes/.gitkeep", ""),
        ("brief.md", assets_init / "brief.md"),
        (".claude/skills/pack-draft/SKILL.md", assets_init / "pack-draft" / "SKILL.md"),
        (".agent/skills/pack-draft/SKILL.md", assets_init / "pack-draft" / "SKILL.md"),
    ]

    for rel_path, source in files_to_create:
        dest_file = target / Path(rel_path)
        if dest_file.exists():
            print(f"skip {rel_path} (exists)")
        else:
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(source, Path):
                shutil.copyfile(source, dest_file)
            else:
                dest_file.write_text(source, encoding="utf-8")
            print(f"created {rel_path}")

    if not sys_yaml_existed:
        from vockpit.cli import cmd_generate
        d2_bin = d2.find_d2_executable()
        no_svg = False
        if not d2_bin:
            print("d2 not found on PATH. Generating with --no-svg.")
            no_svg = True
        return cmd_generate(target, no_svg=no_svg)

    return 0
