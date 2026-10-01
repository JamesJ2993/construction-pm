# Pipeline model — steps, statuses, state schema

## Steps (dashboard matrix columns)

| Step key | What it is | Governing skill (`config.json → skills`) |
|---|---|---|
| `drawing_intake` | Latest issue detected, revision parsed, discipline completeness verified | scanner (+ `--deep`) |
| `register_review` | Clarifications register built or adjudicated against the current set | `register_review` / `register_initial` |
| `register_signoff` | Pure gate — the owner approves the register revision | — |
| `doc_checklist` | Documentation checklist filled against the set | `doc_checklist` |
| `sow_check` | SOW citations verified against the signed-off register. Hard-gated on `register_signoff` | `sow_check` |
| `programme_review` | Programme vs milestone dates; slippage and risk flags | PM analysis |
| `cost_review` | Budget / committed / invoiced / variance; anomaly flags | PM analysis |

Cross-cutting (not columns): documentation health (every scan), evidence register reconciliation
(every scan, when configured), email watch.

## Step status enum

`pending | briefed | producing | in_review | awaiting_signoff | signed_off | blocked | n/a`

- `signed_off` is set only by the owner's approval (via `flip_gate`) — never agent-declared. The one
  exception: `drawing_intake` auto-flips to `signed_off` when the scan verifies a complete set,
  because it is a data check, not a judgement.
- Every `awaiting_signoff` or `blocked` step must have a matching `waiting_on` entry — the
  dashboard's waiting-on panel renders only from those entries.

## Waiting-on entry

```json
{"id": "<project id>-<slug>", "type": "statutory|approval|missing_input|question|external|email",
 "text": "...", "needed_from": "...", "raised": "YYYY-MM-DD", "due": "YYYY-MM-DD"}
```

`statutory` items carry a `due` date (required) — a deadline set by law or the contract: a payment
response, a payment or lien notice, a time bar. They sort above everything on the dashboard and persist
across scans until resolved. Data gates (`missing_input` raised by the scanner) clear themselves on the
next scan when the input appears. `approval` and `external` items persist across scans until resolved. `pm_state.resolve()`
moves an item into the project's `resolved` map, and the scanner never re-raises a resolved id.

## Documentation health

`config.json → required_documents[stage]` lists what must exist at each stage; `doc_weights`
weights the score. Per-document status:

- `current` — exists, and (for `date_sensitive_docs`) dated on/after the latest drawing issue
- `stale` — a date-sensitive document that predates the latest issue, unless listed in `stale_ok`
- `missing` — required at this stage, not found
- `not_required` — not required at this stage

Documents in `ignore_docs` are never scored. Score = weighted (current=1, stale=0.5, missing=0).
Bands: green ≥75, amber ≥50, red <50. Missing and stale required documents raise `missing_input`
waiting-on entries automatically.

## state.json (schema 2)

```
schema_version: 2, generated_at,
projects: { <id>: {
  name, path, aliases,
  drawing_stage: { current, latest_issue: {stage_folder, set_file, set_path, issue_date, modified,
                   revision, pinned, disciplines_detected, disciplines_missing}, stages_found },
  artifacts: { registers[], register, <each configured document>: {path, name, modified} | null },
  program:   { found, latest, milestone_dates[], conflict, governing_date, confirmed_date },
  cost:      { found, file, total, contract_sum, area, per_area, invoices, purchase_orders, quotes },
  evidence:  { label, matrix, counts, close_candidates[], unsupported_closed[] } | null,
  doc_health: { stage, docs{...}, score, band },
  pipeline:  { <step>: {status, detail, updated} },
  waiting_on: [ ... ], resolved: { <id>: {answer, resolution, ts} },
  standing_notes: [ ... ],
  last_scanned, scan_fingerprint } }
```

The scan refreshes everything it measures and carries forward what the owner decided: `pipeline`,
`resolved`, `standing_notes`, `program.confirmed_date`, and `approval` / `external` waiting-on
items.

Scanner behaviour worth knowing:
- Revision parsing handles both `T3/C1/P2` suffixes and alphabetic `Rev.U` schemes; date prefixes
  YYMMDD and YYYYMMDD.
- Stage = the last configured stage folder containing PDFs, skipping stages with
  `is_issue: false` and folders in `skip_folders` (e.g. a construction set that is really a
  base-building issue). `pinned_set_pattern` picks one set within that folder.
- A register revision under 20% of its predecessor's size raises a snapshot-loss question (the
  openpyxl in-place-save failure mode).
- Milestone dates are read from programme filenames written `DD.MM.YY` or `DD.MM.YYYY`; more than
  one distinct date raises a conflict question until the owner confirms one.
- The fingerprint (names + mtimes of every watched folder) skips unchanged projects; `--force`
  rescans, `--deep` re-runs the PyMuPDF discipline scan on the latest set.

## Audit trail

- `activity-log.jsonl` — every scan, brief, commission (with its id, specialist and envelope status,
  `no-return` included), stage run, render, resolution and lesson edit
- `approvals.jsonl` — every sign-off decision: ts, project, gate, decision, by, artifact, note
- `history/state-*.json` — snapshot before every mutating save
- `scope-denials.jsonl` — every path the guard refused
