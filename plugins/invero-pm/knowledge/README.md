# Knowledge packs

What the agents know about building in a particular country — its building code, referenced
standards, permits, payment law, safety law, contract forms and terms — and how much to trust each
fact. One pack per country, chosen from the project's `project_facts.country`.

| Pack | Status |
|---|---|
| [au/](au/INDEX.md) | Australia — written in depth: NCC, state variations, security of payment (VIC, NSW, QLD), WHS (VIC, NSW), planning (VIC, NSW), five discipline checklists, standards index |
| [us/](us/INDEX.md) | United States — **starter**: the national picture and US terms. State files are written on first use |
| [_template/](_template/INDEX.md) | Empty layout for any other country |

**A pack is a starting point, not legal advice.** Every file says how far it has been checked.
Findings that rest on a `provisional` file say so.

## How a pack is chosen

`kb_resolve.py` (in the project-manager skill) reads the project's `project_facts.country` and
`region` and looks in this order:

1. **The owner's overlay** — `~/.claude/pm-agent/knowledge/<country>/` (or `$PM_KB_ROOT/<country>/`).
   This is where `knowledge-curator-agent` writes. It survives plugin updates.
2. **The shipped pack** — this folder. Read-only: the plugin is replaced on every update, so nothing
   writes here.
3. **No pack** — the PM tells the owner, and with their OK commissions the curator to build one in
   the overlay from `_template/`, every file `provisional` until a person confirms it.

A file in the overlay wins over the shipped file at the same path. Regional files — `payment/vic.md`,
`codes/ca.md`, `permitting/nsw/approval-pathways.md` — are looked up for the project's region in each
of the pack's `regional_branches` (`defaults.json`). A missing regional file is reported, never
filled from another region or another country.

## Layout — the same in every pack

| Path | Holds |
|---|---|
| `INDEX.md` | What is in the pack and what is not yet |
| `defaults.json` | Date format, currency, units, language, the building code and payment and safety regimes in one line each, regions, regional branches, drawing discipline prefixes, licence attribution rules |
| `terminology.json` | The country's terms for the shared keys — `client`, `schedule`, `change`, `payment_application`, `completion`, `retention` … — used as `{{key}}` in report structures and agent text |
| `codes/` | The building code: structure, editions, which edition governs, regional adoption and amendments |
| `standards/` | Referenced standards — `README.md` and `index.json`. Pointers and paraphrase only |
| `permitting/` | Planning and building approvals, by region |
| `payment/` | Statutory payment, notice, lien and adjudication rules, by region. **No day counts** — each file names the section that fixes each period |
| `safety/` | Construction safety law, by region |
| `contracts/` | The standard contract forms and what each calls the parties |
| `disciplines/` | One review checklist per engineering discipline |
| `practice/`, `sector/<name>/` | Optional: practice benchmarks, sector notes |
| `_meta/` | `sources.json` (what the currency watcher polls), `gaps.jsonl` (known holes), `changelog.jsonl` |

## Frontmatter — every `.md` file except `INDEX.md`

```markdown
---
title: what this file is
source: URL, a named document, or "domain-knowledge"
verified: YYYY-MM-DD the claims were last checked
confidence: verified | high | provisional | gap
licence: CC-BY-4.0 | own-words | public-domain | none
applies_to: [VIC, NSW] or [all]     # optional - regions this file speaks for
edition: NCC 2025                   # optional
tags: [ncc, fire]                   # optional
governing: claims                   # REQUIRED under payment/ and safety/
supersedes: what this replaced      # optional
---
```

| Confidence | Means |
|---|---|
| `verified` | Checked against the cited source on the verified date |
| `high` | Standard practice, stated without a specific citation |
| `provisional` | Written from knowledge or a secondary source and **not yet checked**. The file must say what would verify it |
| `gap` | A known hole. The file records what is missing and why |

`governing` names the key in the project's `config.json → procedures` that governs the topic
(`claims`, `safety`, `legal` …). Where the firm has its own procedure, the procedure wins over the
pack; the pack orients and points.

## The rules `kb-lint.py` enforces

1. All five required keys present; `confidence` and `licence` from the allowed sets; `verified` a
   real date, not in the future.
2. A `provisional` file says what would verify it.
3. Files under `payment/` and `safety/` name their `governing` procedure key.
4. **Files under `standards/` are `own-words`**, and a long quoted run there is flagged as suspected
   reproduced text. Standards bodies license their text; paraphrase, always.
5. **Licence attribution, per pack.** Where `defaults.json → licence_attribution` sets a pattern for a
   licence (Australia: the ABCB attribution for NCC content under CC BY 4.0), every file under that
   licence must carry it, with the edition matching the file's own `edition`.
6. The pack has `defaults.json` and `terminology.json`, and no top-level folder outside the layout.

## Adding a country

Copy `_template/` to `~/.claude/pm-agent/knowledge/<country code>/` (lowercase ISO 3166 code: `gb`,
`nz`, `ca` …), fill `defaults.json` and `terminology.json` first, then the branches a project needs.
Or ask the PM to have the curator do it. Run `kb-lint.py lint --country <code>` before relying on it.
