# AGENTS.md

## Project Constraints and Standards for Vockpit

1. **Python & Package Guidelines**:
   - Python 3.10+ compatibility.
   - Runtime dependencies: `PyYAML` only.
   - Development dependencies: `pytest` only.
   - Console script entrypoint: `vockpit = vockpit.cli:main`.
   - All file operations must use `pathlib` with forward slashes for relative paths and avoid hardcoding OS path separators.
   - All files written as UTF-8 with LF line endings.

2. **D2 Integration**:
   - CLI tool `d2` is used only for converting `.d2` to `.svg`.
   - On Windows dev machine it may reside at `C:\Users\vikas\bin\d2.exe`. Ensure it is discoverable if present in PATH or `~/bin`.
   - Never require D2 for unit testing or model checking without `--no-svg`.

3. **Viewer Guidelines**:
   - Single static `index.html` file in `src/vockpit/assets/viewer/index.html`.
   - No external CDNs, frameworks, or network requests. Inline CSS and JS.
   - Must load `model.js` and `diagrams.js` via `<script>` tags.

4. **Task Sequence**:
   - Follow `docs/designs/0.1-build-spec.md` section 14 strictly.
   - Write tests before code for each task. Run `pytest` and commit after each task.
