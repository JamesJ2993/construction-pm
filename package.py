r"""Zip a plugin for upload to claude.ai (Customize > Plugins > Add > Upload plugin).

    python package.py project-manager

Writes dist\<name>-<version>.zip with .claude-plugin\plugin.json at the top level. Bytecode caches
are left out. Re-run after refresh.py so the upload carries the same version as the local install.
"""

from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).parent
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
SKIP_DIRS = {"__pycache__", ".git"}
SKIP_SUFFIXES = {".pyc"}


def main() -> int:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    name = sys.argv[1]

    market = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    entry = next((p for p in market["plugins"] if p["name"] == name), None)
    if entry is None:
        sys.exit(f"{name} is not in {MARKETPLACE}")
    source = (ROOT / entry["source"]).resolve()
    version = json.loads((source / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["version"]

    out = ROOT / "dist" / f"{name}-{version}.zip"
    out.parent.mkdir(exist_ok=True)
    files = sorted(p for p in source.rglob("*")
                   if p.is_file()
                   and not SKIP_DIRS.intersection(p.relative_to(source).parts)
                   and p.suffix not in SKIP_SUFFIXES)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            z.write(p, p.relative_to(source).as_posix())
    print(f"{out}  ({len(files)} files, {out.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
