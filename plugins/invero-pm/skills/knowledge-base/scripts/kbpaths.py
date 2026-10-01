r"""Where the knowledge packs live, and which copy wins.

Two roots, read in this order:

  overlay  $PM_KB_ROOT, else $PM_AGENT_HOME/knowledge, else ~/.claude/pm-agent/knowledge.
           The owner's packs and every edit the knowledge curator makes. Survives plugin updates.
  shipped  <plugin>/knowledge. Read-only: Claude Code replaces the plugin on every update, so
           nothing is ever written here.

A pack is one folder per country under a root, named by lowercase ISO 3166 code (au, us, gb ...).
A file in the overlay wins over the shipped file at the same relative path. Writes go to the
overlay only - writable() refuses anything else.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
SHIPPED = PLUGIN_ROOT / "knowledge"
TEMPLATE = "_template"


def overlay_root() -> Path:
    if os.environ.get("PM_KB_ROOT"):
        return Path(os.environ["PM_KB_ROOT"]).expanduser()
    home = os.environ.get("PM_AGENT_HOME") or Path.home() / ".claude" / "pm-agent"
    return Path(home).expanduser() / "knowledge"


def cache_dir() -> Path:
    """Working state that is not knowledge - source snapshots."""
    return overlay_root().parent / "cache"


def _pack_names(root: Path) -> set[str]:
    if not root.is_dir():
        return set()
    return {p.name for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")}


def countries(include_template: bool = False) -> list[str]:
    names = _pack_names(overlay_root()) | _pack_names(SHIPPED)
    if not include_template:
        names.discard(TEMPLATE)
    return sorted(names)


def pack_roots(country: str) -> list[tuple[str, Path]]:
    """Existing copies of a pack, overlay first: [("overlay", path), ("shipped", path)]."""
    cc = country.lower()
    out = []
    for label, root in (("overlay", overlay_root()), ("shipped", SHIPPED)):
        if (root / cc).is_dir():
            out.append((label, root / cc))
    return out


def find(country: str, rel: str) -> Path | None:
    """The winning copy of a file in a pack, or None."""
    for _label, root in pack_roots(country):
        p = root / rel
        if p.exists():
            return p
    return None


def load_json(country: str, rel: str) -> dict:
    """A JSON object from a pack, overlay keys laid over shipped keys."""
    merged: dict = {}
    for _label, root in reversed(pack_roots(country)):
        p = root / rel
        if p.is_file():
            merged.update(json.loads(p.read_text(encoding="utf-8")))
    return merged


def inside(p: Path, root: Path) -> bool:
    q, r = Path(p).resolve(), Path(root).resolve()
    return q == r or r in q.parents


def writable(country: str, rel: str = "") -> Path:
    """A path in the overlay copy of a pack. Refuses the shipped pack and anything outside."""
    base = overlay_root() / country.lower()
    target = (base / rel) if rel else base
    if inside(target, SHIPPED):
        raise PermissionError(f"refusing to write inside the shipped plugin: {target}")
    if not inside(target, base):
        raise PermissionError(f"refusing to write outside the overlay pack {base}: {target}")
    return target
