r"""PreToolUse hook: hold Claude's own Write and Edit calls to the PM's scope boundary.

guard.py binds the PM's scripts. This binds everything else that writes files in the session -
the orchestrator, every specialist subagent, and Claude itself - for the folders the owner has
registered, and nothing more:

  - A write inside a registered project's root is refused unless it is also inside one of that
    registration's write roots (the state folder and any extra_write roots).
  - A write to a registration file is refused. Registrations grant scope, so they change only by
    the owner's hand or by init_project.py on the owner's word - never by a tool call.
  - Every other path passes untouched. Projects that are not registered, and work that has
    nothing to do with the PM, are not affected.

Claude Code sends the tool call as JSON on stdin. Exit 0 lets it through; exit 2 blocks it and the
message on stderr goes back to Claude. An error inside the hook lets the call through with a
warning rather than breaking unrelated work - the scripts' own guard still stands behind it.

PM_SCOPE_OFF=1 lets refused writes through for one deliberate session, loudly, as guard.py does.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import project

PATH_KEYS = ("file_path", "notebook_path")


def target(payload: dict) -> Path | None:
    tool_input = payload.get("tool_input") or {}
    for k in PATH_KEYS:
        if tool_input.get(k):
            return Path(tool_input[k]).expanduser()
    return None


def registered() -> list[project.Project]:
    out = []
    for reg in project.registrations():
        try:
            out.append(project.load(reg))
        except project.ProjectError:
            continue  # an unusable registration grants nothing and blocks nothing
    return out


def verdict(path: Path) -> str | None:
    """None if the write may proceed, else the reason it is refused."""
    if project.inside(path, (project.projects_dir(),)):
        return (f"{path} is a PM project registration. Registrations set what the PM may read and "
                f"write, so they are changed by the owner by hand (or by init_project.py on the "
                f"owner's explicit word), never by a tool call.")
    for proj in registered():
        if project.inside(path, (proj.root,)) and not project.inside(path, proj.write_roots):
            roots = "\n".join(f"    {r}" for r in proj.write_roots)
            return (f"{path} is inside the registered project folder for {proj.name}, which the PM "
                    f"treats as read-only input. Writable roots for this project:\n{roots}\n"
                    f"File the output in one of those, or ask {proj.owner} to add the folder to "
                    f"extra_write in {proj.registration}.")
    return None


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
        path = target(payload)
        if path is None:
            return 0
        reason = verdict(path)
    except Exception as e:  # never break unrelated work on a hook fault
        print(f"invero-pm scope hook skipped: {e}", file=sys.stderr)
        return 0
    if reason is None:
        return 0
    if os.environ.get("PM_SCOPE_OFF") == "1":
        print(f"PM_SCOPE_OFF is set - allowing a write the scope boundary refuses:\n{reason}",
              file=sys.stderr)
        return 0
    print(f"Refused by the invero-pm scope boundary.\n{reason}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
