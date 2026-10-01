---
name: knowledge-base
description: Read, extend, lint and keep current the country knowledge packs the PM agents rely on — building codes and editions, referenced standards, permitting, statutory payment rules, safety law, contract forms and terminology, per country and region. Use when an agent needs to know which pack and regional files apply to a project, when a pack must be checked or extended, when a project lands in a country or region with no pack, or when the owner asks for a currency scan.
---

# Knowledge packs

One pack per country, in `${CLAUDE_PLUGIN_ROOT}/knowledge/<country>/` (shipped, read-only), overlaid by
the owner's `~/.claude/pm-agent/knowledge/<country>/` (or `$PM_KB_ROOT`). The layout, the frontmatter
contract and the lint rules are in `${CLAUDE_PLUGIN_ROOT}/knowledge/README.md` — read it before writing
anything. Shipped: **Australia** (in depth), **United States** (starter — the national picture; state
files are written on first use), and a blank **template**.

Scripts are in `${CLAUDE_SKILL_DIR}/scripts/`. Every one takes `--country <code>`.

## Which files apply to a project

```
python ${CLAUDE_PLUGIN_ROOT}/skills/project-manager/scripts/kb_resolve.py [--project <id>]
python ${CLAUDE_PLUGIN_ROOT}/skills/project-manager/scripts/kb_resolve.py --country us --region tx
python ${CLAUDE_PLUGIN_ROOT}/skills/project-manager/scripts/kb_resolve.py --terms
```

It reads the project's `project_facts.country` and `region`, names the pack (overlay first), lists the
national and regional file for each of the pack's regional branches, and lists everything **MISSING**. A
missing regional file is never filled from another region or another country — it is raised with the
owner.

## Reading a pack

- Check every file's `confidence` and `verified` date before relying on it. A finding resting on a
  `provisional` entry, or one older than the project's `kb_entry_stale_days`, says so.
- The pack is a triage tool, not the clause: it tells you whether a provision applies and what to check.
  Where a position turns on exact text, open the adopted code, the statute or the licensed standard.
- **No day counts in payment files.** They name the section that fixes each period; the project's own
  periods are in its `project_facts.payment_periods`.

## Changing a pack — the curator only

Only `knowledge-curator-agent` writes, and only to the overlay. To change a shipped file it writes the
corrected copy at the same path in the overlay. **Research for a missing regional file or a new country
needs the owner's OK first** — it sends queries to outside services.

## Lint, gaps, currency

```
python scripts/kb-lint.py lint [--country <cc>]       the gate: 0 clean, 1 problems
python scripts/kb-lint.py stats
python scripts/kb-gaps.py --country <cc>              open gaps by priority
python scripts/kb-gaps.py --country <cc> --brief <id> a research brief for one gap
python scripts/kb-gaps.py --country <cc> --open --question "..." --needs "..." --why "..."
python scripts/kb-gaps.py --country <cc> --close <id> --resolution "..." --filed "<path>"
python scripts/kb-watch-sources.py --country <cc> --check     NETWORK: fetches the pack's sources
python scripts/kb-watch-sources.py --country <cc> --diff <id>
python scripts/kb-watch-sources.py --country <cc> --manual <id> --note "..."
```

`kb-watch-sources.py` is the only script that makes network requests. Run it only when the owner asks for
a currency scan; `industry-watch-agent` judges what its diffs mean. A failed fetch is never "no change".
Gaps and watch state are written to the overlay, never to the shipped pack.

## Adding a country

Copy `${CLAUDE_PLUGIN_ROOT}/knowledge/_template/` to `~/.claude/pm-agent/knowledge/<code>/` (lowercase
ISO 3166 code), fill `defaults.json` and `terminology.json` first, then the branches a project needs, and
run `kb-lint.py lint --country <code>`. Or have the curator do it, on the owner's OK.
