# invero-pm

A Project Manager agent for construction and fit-out projects, for Claude Code.

Point it at a project folder and it keeps track of the documentation for you:
- the latest drawing issue and its revision
- whether the clarifications register, checklist and Scope of Works are current against that issue
- what the programme and cost plan say
- what is waiting on you

It keeps its state in a folder of its own and serves a live dashboard on your machine where you can
answer its questions. Stage work runs through a strict loop: **brief → produce → independent review
→ you sign off**. Nothing counts as done until you approve it.

## What's in it

| Component | Name | Does |
|---|---|---|
| Skill | `invero-pm:project-manager` | The orchestrator: scans, dashboard, stage lifecycle, sign-offs |
| Skill | `invero-pm:tender-documentation-review` | Reviews a multi-discipline tender set against the previous register and produces the next revision |
| Skill | `invero-pm:concise-register-entries` | House style for register, RFI and defects entries |
| Skill | `invero-pm:safe-xlsx-update` | Changes a live workbook without destroying images, rich text or the user's edits |
| Skill | `invero-pm:highlight-sow-clarifications` | Cross-checks register references cited in a Scope of Works (Windows, Word and Excel) |
| Subagent | `invero-pm:pm-reviewer` | Read-only reviewer of a finished stage output |
| Subagent | `invero-pm:pm-project-analyst` | Read-only legwork inside the project folder |

## Requirements

- Claude Code
- Python 3.10+ with `pip install -r requirements.txt` (PyMuPDF, openpyxl, python-docx, Pillow)
- `highlight-sow-clarifications` only: Windows with desktop Word and Excel

## Getting started

Ask Claude to **"set up the PM on `<your project folder>`"**. It will ask for an id, your name and
your date format, then:

1. It registers the project with `init_project.py`. That creates a registration file in
   `~/.claude/pm-agent/projects/` and a state folder inside the project.
2. It adjusts `config.json` to match your folder layout.
3. It shows you a dry-run scan before recording anything.

After that, `/pm` runs the full loop. You can also ask for "what's waiting on me", "approve the
register", "PM dashboard" or "health report".

The default layout expects a `Drawings/` folder with numbered stage subfolders (`2. Preliminary
Issue`, `3. Tender Issue`, …), plus `Tender/`, `Finance/` and `Programme/`. Everything is
configurable; see [skills/project-manager/reference/setup.md](skills/project-manager/reference/setup.md).

## Example prompts

- "Set up the PM on `D:\Projects\Riverside Fit-out`. I'm Sam and I use DD.MM.YYYY dates."
- "/pm" — scans the project, refreshes the dashboard and reports what changed and what is waiting
  on you.
- "What's waiting on me?"
- "The tender set has landed. Review it against register Rev B and produce Rev C."
- "Approve the register sign-off: Rev C is fine, note the ceiling void clash stays open."
- "Give me a health report for the project."
- "Check every clarification cited in section 7 of the Scope of Works against the latest register."

## Scope and safety

The agent reads only the project folder you registered, and writes only its own state folder.
That boundary is enforced in code (`scripts/guard.py`), not just written in the prompt:
- The scripts refuse any path outside it.
- A registration that the agent could edit is itself refused, so the agent can't widen its own
  scope.
- Registrations can carry `scope_tests` to pin the boundaries that matter to you.

To check the boundary:

```
python skills/project-manager/scripts/test_guard.py
```

Project files are never modified. Registers get a new revision letter; the original is never
overwritten. Email is read and draft only.

## What it reads, writes, runs and sends

**Reads.** Files in the registered project folder: drawing PDFs, registers and cost plans (.xlsx),
Scope of Works and checklists (.docx), programme files. Read-only.

**Writes.**
- The project's state folder (default `<project>/.claude/pm-agent/`): `state.json`, `config.json`,
  logs (`*.jsonl`), `dashboard.html`, `history/` snapshots and `reports/`.
- One registration file per project in `~/.claude/pm-agent/projects/`, written by
  `init_project.py` when you register a project.
- New register revisions and other deliverables, only when you ask for them.

**Runs.**
- Python scripts bundled in the plugin: scan, render the dashboard, write the health report.
- Optionally `serve_dashboard.py`, a local web server bound to `127.0.0.1` (port 8765 by
  default). It serves the dashboard and appends your answers and chat messages to the state folder.
  It is not reachable from other machines.
- `highlight-sow-clarifications` runs PowerShell to drive the desktop Word and Excel already open on
  your machine, through COM automation (Windows only).
- `safe-xlsx-update` may open Excel through COM, read-only, to check a workbook before it is
  saved (Windows only).

**Sends and fetches.**
- The plugin makes no network requests of its own, has no telemetry and contacts no external
  service.
- File content Claude reads while working is processed by Anthropic as part of your Claude
  session, under your Claude plan's terms.
- The email watch runs only if you have connected an email connector. It searches your mailbox and
  drafts replies, and never sends.
- Python packages are installed by you, from `requirements.txt`; the plugin installs nothing.

## Project-specific rules and lessons

Each project's state folder holds two notes files:
- `project-notes.md`: rules that apply to that project only
- `lessons.md`: what the PM's daily review learned from your corrections

Both are read at the start of every run. The plugin's own files are never edited by the agent, so
updating the plugin never loses them.

## Setup and support

Free to use under the MIT licence. Paid setup, customisation and support for firms are available
through Invero Projects: see [SUPPORT.md](../../SUPPORT.md) or email james@inveroprojects.com.au.
