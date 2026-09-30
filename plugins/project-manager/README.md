# project-manager

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
| Skill | `project-manager:project-manager` | The orchestrator: scans, dashboard, stage lifecycle, sign-offs |
| Skill | `project-manager:tender-documentation-review` | Reviews a multi-discipline tender set against the previous register and produces the next revision |
| Skill | `project-manager:concise-register-entries` | House style for register, RFI and defects entries |
| Skill | `project-manager:safe-xlsx-update` | Changes a live workbook without destroying images, rich text or the user's edits |
| Skill | `project-manager:highlight-sow-clarifications` | Cross-checks register references cited in a Scope of Works (Windows, Word and Excel) |
| Subagent | `project-manager:pm-reviewer` | Read-only reviewer of a finished stage output |
| Subagent | `project-manager:pm-project-analyst` | Read-only legwork inside the project folder |

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

## Project-specific rules and lessons

Each project's state folder holds two notes files:
- `project-notes.md`: rules that apply to that project only
- `lessons.md`: what the PM's daily review learned from your corrections

Both are read at the start of every run. The plugin's own files are never edited by the agent, so
updating the plugin never loses them.

## Setup and support

Free to use under the MIT licence. Paid setup, customisation and support for firms are available
through Invero Projects: see [SUPPORT.md](../../SUPPORT.md) or email james@inveroprojects.com.au.
