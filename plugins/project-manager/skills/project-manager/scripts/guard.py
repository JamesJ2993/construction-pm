r"""Scope guard for the PM agent.

A scope rule written only as prose drifts: a session that has forgotten the conversation it came
from will not honour it. So the boundary is enforced here, in code, and every file operation in the
PM's scripts goes through check().

The boundary comes from the active project's registration (see project.py):

  - READ  : the project root, the state folder, and any extra_read / extra_write roots.
  - WRITE : the state folder, plus any extra_write roots.

Nothing else - no sibling project, no parent folder, no drive root. Widening the boundary means
editing the registration file on the user's explicit word. The PM's scripts cannot do it: a
registration inside a writable root is refused at load.

Run `python guard.py` to print the live boundary, or `python guard.py <path> [read|write]` to test
one path.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import project

# Set PM_SCOPE_OFF=1 for one deliberate session outside the boundary. It is logged loudly rather
# than silently honoured, so an accidental export in a shell profile is visible.
_OVERRIDE = os.environ.get("PM_SCOPE_OFF") == "1"


class ScopeError(PermissionError):
    """Raised when a path falls outside the PM agent's scope."""


def _roots(mode: str) -> tuple[Path, ...]:
    if mode not in ("read", "write"):
        raise ValueError(f"mode must be 'read' or 'write', got {mode!r}")
    p = project.current()
    return p.write_roots if mode == "write" else p.read_roots


def _resolve(path) -> Path:
    return Path(path).expanduser().resolve(strict=False)


def allowed(path, mode: str = "read") -> bool:
    """True if path is inside an allowed root for this mode."""
    return project.inside(path, _roots(mode))


def _log_denial(path: Path, mode: str) -> None:
    """Record the refusal in the state folder. Best effort - never let logging mask the error."""
    try:
        state_dir = project.current().state_dir
        if not state_dir.is_dir():
            return
        rec = {"ts": datetime.now().astimezone().isoformat(timespec="seconds"),
               "action": "scope-denied", "mode": mode, "path": str(path)}
        with (state_dir / "scope-denials.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError:
        pass


def check(path, mode: str = "read") -> Path:
    """Return the path as given, or raise ScopeError naming the rule it broke.

    The boundary test resolves the path, but callers get their own spelling back: on Windows a
    mapped drive resolves to its longer UNC form, which can push deep paths past MAX_PATH.
    """
    given = Path(path).expanduser()
    p = _resolve(given)
    if allowed(p, mode):
        return given
    if _OVERRIDE:
        _log_denial(p, mode + " (ALLOWED BY PM_SCOPE_OFF)")
        return given
    _log_denial(p, mode)
    proj = project.current()
    permitted = "\n".join(f"    {r}" for r in _roots(mode))
    raise ScopeError(
        f"{mode} refused - outside the PM agent's scope for {proj.name}:\n"
        f"    {p}\n"
        f"Permitted {mode} roots:\n{permitted}\n"
        f"The boundary is set in {proj.registration}. Widen it there, deliberately, "
        f"on {proj.owner}'s word.")


def describe() -> str:
    """One-screen summary of the live boundary, for reports and dashboards."""
    p = project.current()
    return (
        f"PM agent scope - {p.name} ({p.id})\n"
        f"  registration: {p.registration}\n"
        f"  read : {', '.join(str(r) for r in p.read_roots)}\n"
        f"  write: {', '.join(str(r) for r in p.write_roots)}\n"
        f"  override active: {_OVERRIDE}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["--project"]:
        project.select(args[1])
        args = args[2:]
    if args:
        target, mode = args[0], (args[1] if len(args) > 1 else "read")
        try:
            print(f"ALLOWED  {mode}: {check(target, mode)}")
        except ScopeError as e:
            print(f"REFUSED  {e}")
            sys.exit(1)
    else:
        print(describe())
