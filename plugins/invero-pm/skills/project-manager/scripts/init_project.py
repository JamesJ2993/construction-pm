r"""Register a project with the PM agent.

This is the one script that writes a registration, so it is the one place scope is granted. Run it
only on the user's explicit instruction.

  python init_project.py --id riverside-fitout --name "Riverside Fit-out" \
      --root "D:\Projects\Riverside" --country au --region vic [--owner "Sam"] [--state-dir PATH] \
      [--python PATH] [--date-format DD.MM.YYYY] [--port 8765]

Creates:
  <PM home>\projects\<id>.json     the registration (scope) - refuses to overwrite without --force
  <state dir>\config.json          copied from reference\config.template.json if absent
  <state dir>\project-notes.md     project-specific rules the PM reads every run
  <state dir>\lessons.md           lessons the PM's daily review records

The state folder defaults to <root>\.claude\pm-agent. The project folder itself is never written.

--country and --region select the knowledge pack (knowledge/<country>/). A new config.json takes the
pack's defaults - date format, currency, area unit, drawing discipline prefixes - and records the
country and region in project_facts. --date-format, when given, wins over the pack.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "knowledge-base" / "scripts"))
import kbpaths
import project

TEMPLATE = Path(__file__).parent.parent / "reference" / "config.template.json"

NOTES = """# {name} - project notes

Project-specific rules for the PM agent. It reads this file at the start of every run. Keep it to
what differs from the defaults: scope history, standing permissions and who granted them, naming
quirks, which skills govern which stage, how {owner} wants things reported.
"""

LESSONS = """# {name} - lessons

Generalisable lessons from the PM's daily review: corrections {owner} made, instructions given,
friction that repeated. The PM reads this file at the start of every run and edits existing lines
rather than appending near-duplicates.
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--id", required=True, help="lowercase letters, digits and hyphens")
    ap.add_argument("--name", required=True)
    ap.add_argument("--root", required=True, help="the project folder the PM reads")
    ap.add_argument("--owner", default="the project owner", help="who signs off; used in labels")
    ap.add_argument("--state-dir", help=r"default: <root>\.claude\pm-agent")
    ap.add_argument("--python", help="interpreter the PM should use for its scripts")
    ap.add_argument("--country", help="lowercase ISO country code - selects the knowledge pack (au, us, ...)")
    ap.add_argument("--region", help="state, province or region code within the country (vic, tx, ...)")
    ap.add_argument("--date-format", choices=project.DATE_FORMATS,
                    help="default: the country pack's date format, else YYYY-MM-DD")
    ap.add_argument("--port", type=int, default=8765, help="dashboard port")
    ap.add_argument("--force", action="store_true", help="overwrite an existing registration")
    args = ap.parse_args()

    if not project.ID_PATTERN.match(args.id):
        raise SystemExit(f"--id {args.id!r}: use lowercase letters, digits and hyphens")
    root = Path(args.root).expanduser()
    if not root.is_dir():
        raise SystemExit(f"--root {root} is not a folder")
    state_dir = Path(args.state_dir).expanduser() if args.state_dir else root / ".claude" / "pm-agent"

    country = args.country.lower() if args.country else None
    region = args.region.lower() if args.region else None
    pack = kbpaths.load_json(country, "defaults.json") if country else {}
    if country and not pack:
        print(f"note: no '{country}' knowledge pack yet - the PM can have the curator build a "
              f"provisional one with your OK. Registering with neutral defaults.")
    date_format = args.date_format or pack.get("date_format") or "YYYY-MM-DD"
    if date_format not in project.DATE_FORMATS:
        date_format = "YYYY-MM-DD"

    reg_path = project.projects_dir() / f"{args.id}.json"
    if reg_path.exists() and not args.force:
        raise SystemExit(f"{reg_path} already exists - pass --force to replace it")

    registration = {
        "id": args.id,
        "name": args.name,
        "root": str(root),
        "state_dir": str(state_dir),
        "owner": args.owner,
        "date_format": date_format,
        "dashboard_port": args.port,
        "extra_read": [],
        "extra_write": [],
    }
    if args.python:
        registration["python"] = args.python

    reg_path.parent.mkdir(parents=True, exist_ok=True)
    previous = reg_path.read_text(encoding="utf-8") if reg_path.exists() else None
    reg_path.write_text(json.dumps(registration, indent=2) + "\n", encoding="utf-8")
    try:
        proj = project.load(reg_path)  # validates, including the self-writable check
    except project.ProjectError as e:
        if previous is None:
            reg_path.unlink()
        else:
            reg_path.write_text(previous, encoding="utf-8")
        raise SystemExit(str(e))

    state_dir.mkdir(parents=True, exist_ok=True)
    made = []
    if not (state_dir / "config.json").exists():
        cfg = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        cfg["project_facts"]["country"] = country
        cfg["project_facts"]["region"] = region
        if pack:
            cfg["report"]["currency"] = pack.get("currency") or cfg["report"]["currency"]
            cfg["report"]["area_unit"] = pack.get("area_unit") or cfg["report"]["area_unit"]
            if pack.get("discipline_prefixes"):
                cfg["drawings"]["discipline_prefixes"] = pack["discipline_prefixes"]
            if pack.get("expected_disciplines"):
                cfg["drawings"]["expected_disciplines"] = pack["expected_disciplines"]
        (state_dir / "config.json").write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n",
                                               encoding="utf-8")
        made.append("config.json")
    elif country:
        print("note: config.json already exists - set project_facts.country/region in it by hand")
    for fname, text in (("project-notes.md", NOTES), ("lessons.md", LESSONS)):
        if not (state_dir / fname).exists():
            (state_dir / fname).write_text(text.format(name=args.name, owner=args.owner), encoding="utf-8")
            made.append(fname)

    print(f"registered {proj.id}: {reg_path}")
    print(f"state folder: {state_dir}" + (f" (created {', '.join(made)})" if made else ""))
    if pack:
        print(f"knowledge pack: {pack.get('name', country)} ({country}{'/' + region if region else ''}), "
              f"dates {date_format}, {pack.get('area_unit')}")
    print("next: python kb_resolve.py   (which knowledge files apply, and which are missing)")
    print("      edit config.json to match the project's folder layout, then run scan_state.py --dry-run")
    return 0


if __name__ == "__main__":
    sys.exit(main())
