r"""Gap queue for a knowledge pack - what the agents know they do not know.

When an agent meets something the pack does not cover, it records a gap rather than guessing.

    python kb-gaps.py --country au                     open gaps by priority
    python kb-gaps.py --country au --brief <id>        research brief for one gap
    python kb-gaps.py --country au --next              brief the highest-priority gap
    python kb-gaps.py --country us --open --question "..." --needs "..." --why "..." [--priority high]
    python kb-gaps.py --country us --close <id> --resolution "..." --filed "payment/tx.md"

The shipped pack's gaps are read-only; opening or closing a gap writes the record to the owner's
overlay (see kbpaths.py), where it overrides the shipped record with the same id.

WHAT THIS DOES NOT DO: the research. A script cannot read a source and decide what it means. It
manages the queue and produces the brief; a model does the work and knowledge-curator-agent writes
the result. A gap closed without --filed is refused: an answer that was never written down has been
forgotten, not closed.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import kbpaths

ORDER = {"high": 0, "medium": 1, "low": 2}


def _today() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")[:10]


def load(country: str) -> list[dict]:
    """Shipped gaps with overlay records laid over them by id."""
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


def _overlay_rows(country: str) -> list[dict]:
    p = kbpaths.writable(country, "_meta/gaps.jsonl")
    if not p.is_file():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def _save_overlay(country: str, rows: list[dict]) -> None:
    p = kbpaths.writable(country, "_meta/gaps.jsonl")
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    tmp.replace(p)


def _upsert(country: str, record: dict) -> None:
    rows = [r for r in _overlay_rows(country) if r.get("id") != record["id"]]
    rows.append(record)
    _save_overlay(country, rows)


def log(country: str, action: str, target: str, detail: str) -> None:
    p = kbpaths.writable(country, "_meta/changelog.jsonl")
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": _today(), "action": action, "target": target, "detail": detail,
                            "by": "kb-gaps"}, ensure_ascii=False) + "\n")


def open_gaps(country: str) -> list[dict]:
    gs = [g for g in load(country) if g.get("status") != "closed"]
    return sorted(gs, key=lambda g: ORDER.get(g.get("priority", "low"), 3))


def cmd_list(country: str) -> int:
    gs = open_gaps(country)
    if not gs:
        print("no open gaps")
        return 0
    print(f"{len(gs)} open gap(s) in the {country} pack\n")
    for g in gs:
        print(f"  [{g.get('priority', '?'):<6}] {g['id']}")
        print(f"           {g.get('question')}")
        print(f"           needs: {g.get('needs')}")
        if g.get("why_deferred"):
            print(f"           deferred: {g['why_deferred']}")
        print()
    return 0


def cmd_brief(country: str, gid: str | None) -> int:
    gs = open_gaps(country)
    if not gs:
        print("no open gaps")
        return 0
    g = next((x for x in gs if x["id"] == gid), None) if gid else gs[0]
    if g is None:
        print(f"no open gap {gid!r}. Open: {', '.join(x['id'] for x in gs)}")
        return 1
    defaults = kbpaths.load_json(country, "defaults.json")
    print(f"RESEARCH BRIEF  {g['id']}   priority {g.get('priority')}   pack {country}\n")
    print(f"Question\n  {g.get('question')}\n")
    print(f"What would close it\n  {g.get('needs')}\n")
    if g.get("why_deferred"):
        print(f"Why it was deferred\n  {g['why_deferred']}\n")
    print("Rules for the answer")
    print("  - Cite the source. An answer without provenance cannot be filed.")
    print("  - Standards text may NOT be quoted, in any country. Paraphrase, always.")
    if defaults.get("licence_note"):
        print(f"  - {defaults['licence_note']}")
    print("  - Statutory periods: name the section that fixes each one. Never write the day count.")
    print("  - If research leaves you unsure, file it as provisional and say what would verify it,")
    print("    or reopen this gap with a sharper question. Never let a guess read as knowledge.")
    print("\nFiling")
    print("  Hand the result to knowledge-curator-agent - the only agent that writes to a pack.")
    print("  Then close this gap naming where the answer landed:")
    print(f"    python kb-gaps.py --country {country} --close {g['id']} \\")
    print('      --resolution "what was established" --filed "<path in the pack>"')
    return 0


def cmd_open(country: str, question: str, needs: str, why: str, priority: str, gid: str | None) -> int:
    existing = {g["id"] for g in load(country)}
    gid = gid or f"gap-{_today().replace('-', '')}-{len(existing) + 1:02d}"
    if gid in existing:
        print(f"gap {gid} already exists")
        return 1
    _upsert(country, {"ts": _today(), "id": gid, "priority": priority, "status": "open",
                      "question": question, "needs": needs, "why_deferred": why})
    log(country, "gap-opened", "_meta/gaps.jsonl", question[:120])
    print(f"opened {gid} [{priority}] in {kbpaths.writable(country)}")
    return 0


def cmd_close(country: str, gid: str, resolution: str, filed: str) -> int:
    g = next((x for x in load(country) if x["id"] == gid), None)
    if g is None:
        print(f"no gap {gid!r}")
        return 1
    if g.get("status") == "closed":
        print(f"{gid} is already closed")
        return 1
    if kbpaths.find(country, filed) is None:
        print(f"refused: --filed points at nothing in the {country} pack: {filed}\n"
              f"Write the answer into the pack first, then close the gap.")
        return 1
    _upsert(country, {**g, "status": "closed", "closed": _today(), "resolution": resolution,
                      "filed_to": filed})
    log(country, "gap-closed", filed, resolution)
    print(f"closed {gid}, filed to {filed}")
    print(f"remaining open: {len(open_gaps(country))}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Knowledge gap queue")
    ap.add_argument("--country", required=True, help="lowercase country code, e.g. au, us")
    ap.add_argument("--brief", metavar="ID", nargs="?", const="")
    ap.add_argument("--next", action="store_true")
    ap.add_argument("--open", action="store_true")
    ap.add_argument("--close", metavar="ID")
    ap.add_argument("--question")
    ap.add_argument("--needs")
    ap.add_argument("--why", default="")
    ap.add_argument("--priority", default="medium", choices=("high", "medium", "low"))
    ap.add_argument("--id")
    ap.add_argument("--resolution")
    ap.add_argument("--filed", help="path within the pack where the answer now lives")
    a = ap.parse_args()
    cc = a.country.lower()

    if a.next:
        return cmd_brief(cc, None)
    if a.brief is not None:
        return cmd_brief(cc, a.brief or None)
    if a.open:
        if not a.question or not a.needs:
            print("--open needs --question and --needs")
            return 1
        return cmd_open(cc, a.question, a.needs, a.why, a.priority, a.id)
    if a.close:
        if not a.resolution or not a.filed:
            print("--close needs --resolution and --filed")
            return 1
        return cmd_close(cc, a.close, a.resolution, a.filed)
    return cmd_list(cc)


if __name__ == "__main__":
    sys.exit(main())
