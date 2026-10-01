# Setup — registration and config

A project needs two files. They are deliberately separate: the registration grants access, the
config describes the folder.

| File | Where | Who edits it | Holds |
|---|---|---|---|
| Registration | `~/.claude/pm-agent/projects/<id>.json` (or `$PM_AGENT_HOME/projects/`) | the owner, or `init_project.py` on their word | root, state folder, scope, owner, date format |
| Config | `<state folder>/config.json` | the owner or the PM | folder layout, filename patterns, required documents, skills, permissions |

Plus two notes files in the state folder, both read at the start of every run:
`project-notes.md` (project-specific rules and their history) and `lessons.md` (the daily review's
output).

Shared across every project, in the PM home (`~/.claude/pm-agent/`, or `$PM_AGENT_HOME`):

| Path | Holds | Written by |
|---|---|---|
| `projects/<id>.json` | Registrations | the owner, or `init_project.py` on their word — never a tool call (the hook refuses it) |
| `practice/lessons.md` | The practice playbook: an index, then `LSN-nnn` lessons, no client data | the PM at the daily review |
| `practice/proposals/` | Proposed new agents and skills, for the owner to install | the PM |
| `knowledge/<country>/` | The owner's knowledge-pack overlay — wins over the shipped pack | `knowledge-curator-agent` only |
| `cache/` | Currency-watch snapshots | `kb-watch-sources.py` |

## Registration

```json
{
  "id": "riverside-fitout",
  "name": "Riverside Fit-out",
  "root": "D:\\Projects\\Riverside",
  "state_dir": "D:\\Projects\\Riverside\\.claude\\pm-agent",
  "owner": "Sam",
  "python": "C:\\Python312\\python.exe",
  "date_format": "DD.MM.YYYY",
  "dashboard_port": 8765,
  "extra_read": [],
  "extra_write": [],
  "scope_tests": [
    {"path": "D:\\Projects\\Harbourside", "mode": "read", "allow": false, "why": "another project"}
  ]
}
```

| Key | Required | Meaning |
|---|---|---|
| `id` | yes | lowercase letters, digits, hyphens; the file name and the key in state.json |
| `name` | yes | shown on the dashboard and reports |
| `root` | yes | the project folder — readable, never written |
| `state_dir` | no | default `<root>/.claude/pm-agent`; the only folder written by default |
| `owner` | no | who signs off; used in labels and waiting-on items |
| `python` | no | interpreter for the scripts |
| `date_format` | no | `YYYY-MM-DD` (default), `DD.MM.YYYY`, `DD/MM/YYYY` or `MM/DD/YYYY` |
| `dashboard_port` | no | default 8765 |
| `extra_read`, `extra_write` | no | further roots; writable roots are also readable |
| `scope_tests` | no | paths `test_guard.py` must allow or refuse — pin the boundaries that matter |

A registration saved inside any of its own writable roots is refused at load.

## config.json

Start from [config.template.json](config.template.json) and change folder names to match the
project. Paths are relative to the project root; use `/` as the separator.

| Section | What it controls |
|---|---|
| `project_facts` | where the project is and what governs it — see below |
| `terminology` | overrides of the country pack's terms for this project (e.g. `"client_rep": "Construction Manager"`) |
| `aliases` | other names for the project — used by the email watch |
| `ignore_files`, `ignore_prefixes`, `skip_dirs` | clutter the scanner never lists (`~$` lock files, CAD folders) |
| `drawings.dir`, `drawings.stages` | the drawings folder and its stage subfolders, in issue order. `is_issue: false` marks a folder that never counts as the current set (existing conditions, lease plans) |
| `drawings.tender_stage` | the stage a Scope of Works should be written against; a SOW on an earlier stage raises a question |
| `drawings.skip_folders` | stage folders to ignore when picking the current set |
| `drawings.pinned_set_pattern` | substring that picks one set inside the current stage folder |
| `drawings.expected_disciplines`, `discipline_prefixes` | what a complete set contains, and how sheet numbers map to disciplines |
| `registers` | where clarifications registers live and how to recognise them; every match is kept as a revision history |
| `documents.<name>.find` | ordered searches `{dir, exts, pattern, depth}`; the newest match of the first search with a hit wins |
| `documents.<name>.folder` | the document is "present" when this folder has files; `exclude_latest` rejects a folder whose newest file matches |
| `programme` | programme folder, file types, and the milestone name read from filenames |
| `budget` | cost-plan folder and filename pattern, the row labels to read (`total`, `contract_sum`, `area`), and subfolders to count |
| `evidence_register` | optional requirements matrix to reconcile against numbered evidence folders (below) |
| `required_documents`, `doc_weights` | per-stage documentation health |
| `date_sensitive_docs`, `stale_ok`, `ignore_docs` | staleness rules and exclusions |
| `skills` | which skill governs each stage (see SKILL.md) |
| `permissions` | `evidence_refiling`, `stage_skeletons` — both off by default |
| `email.keywords` | email watch search terms |
| `report` | `byline`, `currency`, `area_unit`, `cost_label` for the dashboard and health report; `letterhead` (a `.docx` whose headers, footers, images and margins every deliverable is built on — `null` builds plain); `prepared_by`; `draft_marking` |
| `procedures` | the firm's own management-system documents, by activity — see [procedures.md](procedures.md). `null` means the plugin's rule applies as written |
| `tuning` | the dials: `approvals_chase_days`, `health_check_stale_days`, `programme_runs_per_project_day`, `deadline_horizon_bdays`, `repeat_deferral_cycles`, `mail_lookback_days`, `source_scan_stale_days`, `kb_entry_stale_days` (never below 90) |
| `filing` | deliverable type → folder. Relative paths sit under the state folder (default `deliverables/…`); a folder inside the project tree must also be in the registration's `extra_write` |
| `templates.dir` | the firm's controlled template library. When set, `check-provenance.py` checks deliverables against it and **a missing library is an error**, never a silent fallback |

### project_facts

Recorded at setup, kept current by the PM, read by every specialist. **Unknown is recorded as `null`
and raised — never guessed.**

| Key | Example (AU) | Example (US) |
|---|---|---|
| `country`, `region` | `au`, `vic` | `us`, `tx` |
| `address`, `client` | the site; the client entity | |
| `role` | `consultant project manager acting for the client` | `owner's representative` |
| `authority_having_jurisdiction` | the relevant building surveyor / council | `City of Austin Development Services` |
| `building_code` | `NCC 2022 with Victorian variations — building permit applied 3 March 2024` | `IBC 2021 as amended by the City of Austin — permit applied 3 March 2024` |
| `payment_law` | `Building and Construction Industry Security of Payment Act 2002 (Vic)` | `Texas Property Code ch. 28 (prompt pay) and ch. 53 (liens)` |
| `payment_periods` | `{"payment_response_due": "<n> business days after service — s <x>", ...}` — each with the section that fixes it | same shape |
| `safety_regime` | `OHS Act 2004 (Vic)` | `OSHA 29 CFR 1926 (federal OSHA)` |
| `contract_form`, `contract_periods` | `AS 4000-1997 with special conditions`; the contract's own notice and payment periods | `AIA A101/A201-2017 as amended` |

## Knowledge packs

`--country` at registration picks the pack (`knowledge/<country>/` in the plugin, overlaid by the owner's
`~/.claude/pm-agent/knowledge/<country>/`). `python scripts/kb_resolve.py` shows which pack and regional
files apply and which are missing; `kb_resolve.py --terms` prints the merged terminology. The pack layout
and how to add a country are in `knowledge/README.md` at the plugin root.

Document names in `required_documents` are the keys of `documents`, plus `drawing_set`,
`register`, `program` and `budget`, which the scanner supplies itself.

### Evidence register

```json
"evidence_register": {
  "label": "Certification",
  "dir": "Certificates & Permits",
  "file_pattern": "requirements.*matrix",
  "sheet_pattern": "requirement",
  "placeholders": ["_Requirement.txt"],
  "item_col": 0,
  "requirement_col": 2
}
```

The matrix sheet needs a header row with a `Status` column and a numeric item number in
`item_col`. Evidence for item N sits in a sibling folder whose name starts with N.

## Checking a new setup

```
python scripts/guard.py                 # the boundary as the PM sees it
python scripts/test_guard.py            # fixture refusals + this project's scope_tests
python scripts/kb_resolve.py           # the knowledge pack and regional files, and what is missing
python scripts/scan_state.py --dry-run  # what the scan would record, written nowhere
```
