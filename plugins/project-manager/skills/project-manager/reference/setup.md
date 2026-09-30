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
| `report` | `byline`, `currency`, `area_unit`, `cost_label` for the dashboard and health report |

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
python scripts/scan_state.py --dry-run  # what the scan would record, written nowhere
```
