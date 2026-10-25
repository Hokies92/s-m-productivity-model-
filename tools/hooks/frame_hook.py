"""Claude Code PostToolUse hook: run the frame check on any Markdown or text file Claude writes or edits.

Exit code 2 sends the findings back to Claude, which must fix them before continuing (CLAUDE.md rule 1).
Configured in .claude/settings.json.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import frame_check  # noqa: E402

try:
    data = json.load(sys.stdin)
except ValueError:
    sys.exit(0)
path = (data.get("tool_input") or {}).get("file_path") or ""
p = pathlib.Path(path)
if p.suffix.lower() not in (".md", ".txt") or not p.exists():
    sys.exit(0)
try:
    rel = str(p.resolve().relative_to(ROOT))
except ValueError:
    rel = str(p)
if rel in frame_check.EXEMPT or any(part in frame_check.EXEMPT_DIRS for part in pathlib.Path(rel).parts) \
        or p.name.endswith(frame_check.EXEMPT_SUFFIXES):
    sys.exit(0)
faults = [f for f in frame_check.check_text(p.read_text(errors="ignore"), rel) if f[0] == "FAULT"]
if faults:
    lines = "\n".join(f"  {rel}:{line} [{kind}] {text[:120]}" for _, kind, line, text in faults)
    print("frame-check: this text labels the original as faulty or treats the sample as a company.\n"
          f"{lines}\nFor each: state what the thing is for (docs/MODEL.md section 6) or ask Scott. "
          "Do not relabel it with a softer fault word.", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
