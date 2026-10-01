r"""Project registration: which folder the PM works on, and what it may touch.

A registration is a small JSON file in the PM home - ~/.claude/pm-agent/projects/<id>.json, or
$PM_AGENT_HOME/projects/<id>.json. It names the project root, the PM's state folder, and any extra
read or write roots. guard.py builds the scope boundary from it and nothing else.

Registrations live outside every project and are written only by init_project.py, which runs on the
user's explicit instruction. A registration that sits inside one of its own writable roots is
refused: the PM's scripts can write there, so they could otherwise widen their own scope.

Selecting a project: pass --project <id> to a script, or set PM_PROJECT. With exactly one project
registered, it is selected automatically.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")
DATE_FORMATS = ("YYYY-MM-DD", "DD.MM.YYYY", "DD/MM/YYYY", "MM/DD/YYYY")


class ProjectError(RuntimeError):
    """No usable project registration."""


def home() -> Path:
    return Path(os.environ.get("PM_AGENT_HOME") or Path.home() / ".claude" / "pm-agent")


def projects_dir() -> Path:
    return home() / "projects"


@dataclass(frozen=True)
class Project:
    id: str
    name: str
    root: Path
    state_dir: Path
    registration: Path
    extra_read: tuple[Path, ...] = ()
    extra_write: tuple[Path, ...] = ()
    owner: str = "the project owner"
    python: str | None = None
    date_format: str = "YYYY-MM-DD"
    dashboard_port: int = 8765
    scope_tests: tuple[dict, ...] = ()

    @property
    def write_roots(self) -> tuple[Path, ...]:
        return (self.state_dir, *self.extra_write)

    @property
    def read_roots(self) -> tuple[Path, ...]:
        """Everything writable is also readable."""
        out: list[Path] = []
        for p in (self.root, *self.extra_read, *self.write_roots):
            if p not in out:
                out.append(p)
        return tuple(out)


def variants(root: Path) -> set[Path]:
    r"""Both spellings of a root.

    On Windows a mapped drive letter resolves to its UNC target, so W:\x and \\server\share\x are
    the same place. Holding both forms lets either spelling match while a different folder still
    does not.
    """
    out = {Path(root)}
    try:
        out.add(Path(root).resolve(strict=False))
    except OSError:
        pass
    return out


def inside(path: Path, roots) -> bool:
    try:
        p = Path(path).expanduser().resolve(strict=False)
    except OSError:
        p = Path(path)
    return any(p == v or p.is_relative_to(v) for r in roots for v in variants(r))


def _paths(values) -> tuple[Path, ...]:
    return tuple(Path(v) for v in (values or []))


def load(path: Path) -> Project:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise ProjectError(f"cannot read registration {path}: {e}") from e

    missing = [k for k in ("id", "name", "root") if not data.get(k)]
    if missing:
        raise ProjectError(f"{path} is missing {', '.join(missing)}")
    if not ID_PATTERN.match(data["id"]):
        raise ProjectError(f"{path}: id {data['id']!r} must be lowercase letters, digits and hyphens")
    if data.get("date_format", "YYYY-MM-DD") not in DATE_FORMATS:
        raise ProjectError(f"{path}: date_format must be one of {', '.join(DATE_FORMATS)}")

    root = Path(data["root"])
    proj = Project(
        id=data["id"],
        name=data["name"],
        root=root,
        state_dir=Path(data.get("state_dir") or root / ".claude" / "pm-agent"),
        registration=Path(path),
        extra_read=_paths(data.get("extra_read")),
        extra_write=_paths(data.get("extra_write")),
        owner=data.get("owner") or "the project owner",
        python=data.get("python"),
        date_format=data.get("date_format", "YYYY-MM-DD"),
        dashboard_port=int(data.get("dashboard_port", 8765)),
        scope_tests=tuple(data.get("scope_tests", [])),
    )
    if inside(proj.registration, proj.write_roots):
        raise ProjectError(
            f"refusing {path}: the registration sits inside a folder the PM can write to, so the "
            f"PM could rewrite its own scope. Keep registrations in {projects_dir()}.")
    return proj


def registrations() -> list[Path]:
    d = projects_dir()
    return sorted(d.glob("*.json")) if d.is_dir() else []


_current: Project | None = None


def select(project_id: str | None = None) -> Project:
    """Choose the active project for this process and export PM_PROJECT for child processes."""
    global _current
    pid = project_id or os.environ.get("PM_PROJECT")
    regs = registrations()
    if pid:
        path = projects_dir() / f"{pid}.json"
        if not path.is_file():
            known = ", ".join(p.stem for p in regs) or "none"
            raise ProjectError(f"no registration for {pid!r} in {projects_dir()} (registered: {known})")
    elif len(regs) == 1:
        path = regs[0]
    elif not regs:
        raise ProjectError(
            f"no project registered in {projects_dir()}. Register one with init_project.py.")
    else:
        raise ProjectError(
            "several projects are registered (" + ", ".join(p.stem for p in regs) + "). "
            "Pass --project <id> or set PM_PROJECT.")
    _current = load(path)
    os.environ["PM_PROJECT"] = _current.id
    return _current


def current() -> Project:
    return _current or select()


def reset() -> None:
    """Forget the active project (tests)."""
    global _current
    _current = None
