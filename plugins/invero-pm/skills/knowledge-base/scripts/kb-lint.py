r"""Validate knowledge packs - provenance, layout, and the licensing line.

    python kb-lint.py                         stats for every pack
    python kb-lint.py lint                    the gate, every pack: 0 clean, 1 problems
    python kb-lint.py lint --country us       one country (its overlay and shipped copies)
    python kb-lint.py lint --root <folder>    one pack folder, wherever it is
    python kb-lint.py gaps --country au       open gaps, by priority

A knowledge base that accretes unattributed claims is worse than none, because it is confidently
wrong in a domain where being confidently wrong costs money. The contract and the rules are in
knowledge/README.md; this file is the authority on what is enforced.

Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import kbpaths

REQUIRED = ("title", "source", "verified", "confidence", "licence")
CONFIDENCE = ("verified", "high", "provisional", "gap")
LICENCES = ("CC-BY-4.0", "own-words", "public-domain", "none")

BRANCHES = {"codes", "standards", "permitting", "payment", "safety", "contracts", "disciplines",
            "practice", "sector", "_meta"}
ROOT_FILES = {"INDEX.md", "README.md", "defaults.json", "terminology.json"}
DEFAULT_KEYS = ("country", "name", "language", "date_format", "currency", "area_unit",
                "building_code", "payment_law", "safety_regime", "regions", "regional_branches",
                "discipline_prefixes")

# Branches where the firm's procedure, if it has one, governs the topic. The file must name the
# procedure key so the precedence is machine-visible rather than a convention someone remembers.
GOVERNED_BRANCHES = ("payment", "safety")

# A quoted run long enough to be a reproduced clause rather than a term of art.
QUOTED_RUN = re.compile(r'["“][^"”]{80,}["”]')

FM = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)


def _squash(s: str) -> str:
    return " ".join(s.split())


def _year(v) -> str | None:
    m = re.search(r"(\d{4})", str(v or ""))
    return m.group(1) if m else None


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Minimal frontmatter parser - no YAML dependency."""
    m = FM.match(text)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        line = line.split(" #", 1)[0].strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, _, v = line.partition(":")
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            meta[k.strip()] = [x.strip() for x in v[1:-1].split(",") if x.strip()]
        else:
            meta[k.strip()] = None if v in ("", "null", "~") else v.strip("\"'")
    return meta, text[m.end():]


def entries(pack: Path) -> list[tuple[Path, dict, str]]:
    out = []
    for p in sorted(pack.rglob("*.md")):
        rel = p.relative_to(pack)
        if rel.parts[0] == "_meta" or (len(rel.parts) == 1 and p.name in ("INDEX.md", "README.md")):
            continue
        meta, body = parse_frontmatter(p.read_text(encoding="utf-8"))
        out.append((p, meta, body))
    return out


def lint_pack(pack: Path, layered: bool = False) -> tuple[int, list[str]]:
    """layered: an overlay sitting on a shipped pack, which may hold only corrections and gaps."""
    problems, n = [], 0
    label = pack.name

    # layout
    for f in ("defaults.json", "terminology.json"):
        if not (pack / f).is_file() and not layered:
            problems.append(f"{label}: missing {f}")
    for child in pack.iterdir():
        if child.is_dir() and child.name not in BRANCHES and not child.name.startswith("."):
            problems.append(f"{label}: '{child.name}/' is not a pack branch ({', '.join(sorted(BRANCHES))})")
        if child.is_file() and child.name not in ROOT_FILES:
            problems.append(f"{label}: unexpected file at pack root: {child.name}")

    defaults = {}
    if layered and not (pack / "defaults.json").is_file():
        shipped = kbpaths.SHIPPED / pack.name / "defaults.json"
        if shipped.is_file():
            defaults = json.loads(shipped.read_text(encoding="utf-8"))
    if (pack / "defaults.json").is_file():
        try:
            defaults = json.loads((pack / "defaults.json").read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            problems.append(f"{label}/defaults.json: not valid JSON: {e}")
        for k in DEFAULT_KEYS:
            if k not in defaults and not layered:
                problems.append(f"{label}/defaults.json: missing '{k}'")
    if (pack / "terminology.json").is_file():
        try:
            json.loads((pack / "terminology.json").read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            problems.append(f"{label}/terminology.json: not valid JSON: {e}")

    attribution = {}
    for lic, rule in (defaults.get("licence_attribution") or {}).items():
        try:
            attribution[lic] = (re.compile(rule["pattern"], re.I), rule.get("edition_group"))
        except (re.error, KeyError, TypeError) as e:
            problems.append(f"{label}/defaults.json: bad licence_attribution for {lic}: {e}")

    for p, meta, body in entries(pack):
        n += 1
        rel = f"{label}/{p.relative_to(pack).as_posix()}"
        branch = p.relative_to(pack).parts[0]

        if not meta:
            problems.append(f"{rel}: no frontmatter")
            continue
        for k in REQUIRED:
            if not meta.get(k):
                problems.append(f"{rel}: missing '{k}'")

        conf = meta.get("confidence")
        if conf and conf not in CONFIDENCE:
            problems.append(f"{rel}: confidence '{conf}' not one of {CONFIDENCE}")
        lic = meta.get("licence")
        if lic and lic not in LICENCES:
            problems.append(f"{rel}: licence '{lic}' not one of {LICENCES}")

        v = meta.get("verified")
        if v:
            try:
                if date.fromisoformat(str(v)) > date.today():
                    problems.append(f"{rel}: verified date {v} is in the future")
            except ValueError:
                problems.append(f"{rel}: verified '{v}' is not YYYY-MM-DD")

        # Licensed content that may be reproduced only with attribution must carry it, and the
        # attribution's edition must be the file's edition.
        if lic in attribution:
            pat, group = attribution[lic]
            m = pat.search(_squash(body))
            if not m:
                problems.append(f"{rel}: {lic} but missing the attribution this pack requires")
            elif group:
                want = _year(meta.get("edition"))
                if want and m.group(group) != want:
                    problems.append(f"{rel}: attribution cites {m.group(group)} but edition is "
                                    f"{meta.get('edition')} - attribute the edition the content is from")

        # Standards text is licensed everywhere: pointers and paraphrase only.
        if branch == "standards":
            if lic != "own-words":
                problems.append(f"{rel}: under standards/ so licence must be 'own-words', got '{lic}'")
            for q in QUOTED_RUN.findall(body):
                problems.append(f"{rel}: long quoted run looks like reproduced text: {q[:60]}...")

        if branch in GOVERNED_BRANCHES and not meta.get("governing"):
            problems.append(f"{rel}: under {branch}/ so must name its 'governing' procedure key")

        if conf == "provisional" and "verif" not in body.lower():
            problems.append(f"{rel}: provisional but does not say what would verify it")

    idx = pack / "standards" / "index.json"
    if idx.is_file():
        data = json.loads(idx.read_text(encoding="utf-8"))
        for std in data.get("standards", []):
            n += 1
            num = std.get("number", "?")
            for k in ("number", "title", "governs", "pm_trigger"):
                if not std.get(k):
                    problems.append(f"{label}/standards/index.json[{num}]: missing '{k}'")
            for k, val in std.items():
                if isinstance(val, str) and QUOTED_RUN.search(val):
                    problems.append(f"{label}/standards/index.json[{num}]: '{k}' contains a long "
                                    f"quoted run - paraphrase, never reproduce")
    return n, problems


def targets(country: str | None, root: str | None) -> list[tuple[Path, bool]]:
    """(pack folder, layered) pairs - layered when an overlay sits on a shipped pack."""
    if root:
        return [(Path(root), False)]
    names = [country.lower()] if country else kbpaths.countries(include_template=True)
    out = []
    for cc in names:
        roots = kbpaths.pack_roots(cc)
        if not roots:
            raise SystemExit(f"no pack for {cc!r} in {kbpaths.overlay_root()} or {kbpaths.SHIPPED}")
        has_shipped = any(label == "shipped" for label, _p in roots)
        out.extend((p, label == "overlay" and has_shipped) for label, p in roots)
    return out


def load_gaps(country: str) -> list[dict]:
    """Shipped gaps with the overlay's records laid over them by id."""
    by_id: dict[str, dict] = {}
    for _label, root in reversed(kbpaths.pack_roots(country)):
        p = root / "_meta" / "gaps.jsonl"
        if p.is_file():
            for line in p.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    try:
                        g = json.loads(line)
                        by_id[g["id"]] = g
                    except (json.JSONDecodeError, KeyError):
                        continue
    return list(by_id.values())


def stats(pack: Path) -> dict:
    es = entries(pack)
    by_conf: dict[str, int] = {}
    for _p, meta, _b in es:
        c = meta.get("confidence", "?")
        by_conf[c] = by_conf.get(c, 0) + 1
    idx = pack / "standards" / "index.json"
    n_std = len(json.loads(idx.read_text(encoding="utf-8")).get("standards", [])) if idx.is_file() else 0
    return {"files": len(es), "standards": n_std, "by_confidence": by_conf}


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate knowledge packs")
    ap.add_argument("cmd", nargs="?", default="stats", choices=("stats", "lint", "gaps"))
    ap.add_argument("--country", help="lowercase country code, e.g. au, us")
    ap.add_argument("--root", help="lint one pack folder directly")
    a = ap.parse_args()

    if a.cmd == "gaps":
        if not a.country:
            print("gaps needs --country")
            return 1
        gs = [g for g in load_gaps(a.country) if g.get("status") != "closed"]
        if not gs:
            print("no open gaps")
            return 0
        order = {"high": 0, "medium": 1, "low": 2}
        for g in sorted(gs, key=lambda x: order.get(x.get("priority"), 9)):
            print(f"  [{g.get('priority', '?')}] {g.get('id', '')} {g.get('question')}")
            print(f"      needs: {g.get('needs')}")
        return 0

    packs = targets(a.country, a.root)
    if a.cmd == "lint":
        total, problems = 0, []
        for pack, layered in packs:
            n, ps = lint_pack(pack, layered)
            total += n
            problems += [f"[{pack.parent.name}] {x}" for x in ps]
            print(f"checked {n:>3} items  {pack}")
        if problems:
            print(f"\n{len(problems)} problem(s):")
            for p in problems:
                print(f"  {p}")
            return 1
        print(f"\n{total} items: provenance complete, licensing line intact")
        return 0

    for pack, _layered in packs:
        s = stats(pack)
        conf = ", ".join(f"{k} {v}" for k, v in sorted(s["by_confidence"].items())) or "none"
        print(f"{pack}\n  files {s['files']}  standards {s['standards']}  confidence: {conf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
