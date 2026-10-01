r"""Which knowledge pack, and which regional files, apply to a project - and which are missing.

    python kb_resolve.py [--project ID]            the active project's pack, from config.json
    python kb_resolve.py --country us --region tx  any country and region, before setup
    python kb_resolve.py --terms                   the project's merged terminology
    python kb_resolve.py --json                    the same, machine-readable

The PM and every specialist read knowledge through this, so nobody guesses a path or answers a
Texas question from a California file. Lookup order (see knowledge/README.md): the owner's overlay,
then the shipped pack. A regional file missing from both is reported as MISSING - it is never
filled from another region or another country. The PM raises each missing file with the owner and,
on their OK, commissions knowledge-curator-agent to write it.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent.parent / "knowledge-base" / "scripts"))
import kbpaths  # noqa: E402
import project  # noqa: E402


def project_facts(project_id: str | None) -> tuple[dict, dict]:
    """(project_facts, terminology overrides) from the active project's config.json."""
    proj = project.select(project_id)
    cfg_path = proj.state_dir / "config.json"
    if not cfg_path.is_file():
        raise SystemExit(f"no config.json at {cfg_path} - run init_project.py")
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    return cfg.get("project_facts") or {}, cfg.get("terminology") or {}


def terms(country: str, overrides: dict | None = None) -> dict:
    merged = {k: v for k, v in kbpaths.load_json(country, "terminology.json").items()
              if not k.startswith("_")}
    merged.update({k: v for k, v in (overrides or {}).items() if v})
    return merged


def _regional(country: str, branch: str, region: str) -> list[str]:
    """Files that speak for this region in a branch, overlay copies first."""
    found: list[str] = []
    for label, root in kbpaths.pack_roots(country):
        base = root / branch
        for cand in (base / f"{region}.md", base / region):
            if cand.is_file():
                found.append(f"{label}: {cand.relative_to(root).as_posix()}")
            elif cand.is_dir():
                found += [f"{label}: {p.relative_to(root).as_posix()}" for p in sorted(cand.rglob("*.md"))]
    return found


def resolve(country: str | None, region: str | None) -> dict:
    out: dict = {"country": country, "region": region, "pack": [], "branches": {}, "missing": []}
    if not country:
        out["missing"].append("project_facts.country is not set - ask the owner, then record it")
        return out
    cc = country.lower()
    roots = kbpaths.pack_roots(cc)
    out["pack"] = [f"{label}: {p}" for label, p in roots]
    if not roots:
        out["missing"].append(
            f"no '{cc}' knowledge pack. Offer the owner a provisional pack built by "
            f"knowledge-curator-agent from knowledge/_template into {kbpaths.writable(cc)}")
        return out
    defaults = kbpaths.load_json(cc, "defaults.json")
    out["defaults"] = {k: defaults.get(k) for k in
                       ("name", "language", "date_format", "currency", "area_unit", "building_code",
                        "payment_law", "safety_regime")}
    regions = defaults.get("regions") or {}
    if region and regions and region.lower() not in regions:
        out["missing"].append(f"region '{region}' is not one of this pack's regions "
                              f"({', '.join(sorted(regions))})")
    for branch in defaults.get("regional_branches") or []:
        national = kbpaths.find(cc, f"{branch}/README.md")
        entry = {"national": str(national) if national else None, "regional": []}
        if region:
            entry["regional"] = _regional(cc, branch, region.lower())
            if not entry["regional"]:
                out["missing"].append(f"{branch}/{region.lower()}.md - no {branch} file for "
                                      f"{regions.get(region.lower(), region)}")
        out["branches"][branch] = entry
    if not region:
        out["missing"].append("project_facts.region is not set - regional files cannot be checked")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project")
    ap.add_argument("--country")
    ap.add_argument("--region")
    ap.add_argument("--terms", action="store_true", help="print the merged terminology")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    overrides: dict = {}
    if a.country:
        country, region = a.country, a.region
    else:
        facts, overrides = project_facts(a.project)
        country, region = facts.get("country"), facts.get("region")

    if a.terms:
        t = terms(country, overrides) if country else {}
        print(json.dumps(t, indent=2, ensure_ascii=False) if a.json
              else "\n".join(f"  {k:<22} {v}" for k, v in t.items()) or "no terminology - no pack")
        return 0

    r = resolve(country, region)
    if a.json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
        return 0
    print(f"country: {r['country'] or '?'}   region: {r['region'] or '?'}")
    for line in r["pack"]:
        print(f"  pack  {line}")
    for k, v in (r.get("defaults") or {}).items():
        print(f"  {k:<14} {v}")
    for branch, e in r["branches"].items():
        print(f"\n  {branch}/")
        print(f"    national  {e['national'] or '-'}")
        for f in e["regional"]:
            print(f"    regional  {f}")
    if r["missing"]:
        print("\nMISSING - raise with the owner before relying on this branch:")
        for m in r["missing"]:
            print(f"  - {m}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
