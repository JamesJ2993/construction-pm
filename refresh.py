r"""Push edits in this marketplace's source into the installed plugin.

Claude Code runs plugins from a copy in ~\.claude\plugins\cache\, and `plugin update` only
re-copies when the version changes. So: bump the patch version in plugin.json and the matching
marketplace.json entry, then refresh the marketplace and the plugin.

    python refresh.py project-manager

Restart Claude Code (or /reload-plugins) afterwards.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"


def claude_exe() -> str:
    """`claude` on PATH, else the CLI the Windows desktop app bundles in a versioned folder."""
    on_path = shutil.which("claude")
    if on_path:
        return on_path
    base = Path(os.environ.get("APPDATA", "")) / "Claude" / "claude-code"
    found = sorted(base.glob("*/claude.exe"),
                   key=lambda p: [int(x) if x.isdigit() else x for x in p.parent.name.split(".")])
    if not found:
        sys.exit("claude CLI not found on PATH or in the desktop app")
    return str(found[-1])


def bump(version: str) -> str:
    major, minor, patch = (int(x) for x in version.split("."))
    return f"{major}.{minor}.{patch + 1}"


def main() -> int:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    name = sys.argv[1]

    market = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    entry = next((p for p in market["plugins"] if p["name"] == name), None)
    if entry is None:
        sys.exit(f"{name} is not in {MARKETPLACE}")
    manifest_path = ROOT / entry["source"] / ".claude-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    new = bump(manifest["version"])
    manifest["version"] = entry["version"] = new
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    MARKETPLACE.write_text(json.dumps(market, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{name} -> {new}")

    exe = claude_exe()
    for args in (["plugin", "marketplace", "update", market["name"]],
                 ["plugin", "update", f"{name}@{market['name']}"]):
        result = subprocess.run([exe, *args])
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
