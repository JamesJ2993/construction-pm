# invero-pm

A Project Manager agent and its specialist team, for construction and fit-out projects in any
country. A Claude Code plugin.

Point it at a project folder and the PM keeps track of it for you:
- the latest drawing issue and its revision
- whether the clarifications register, checklist and scope are current against that issue
- what the programme (schedule) and cost plan say
- what is waiting on you

When work is needed, the PM briefs a specialist agent to do it: claims, programme analysis, tender
comparison, scope of works, health checks, site reports, code compliance and more. It checks what
comes back and puts it in front of you. Every deliverable runs through a strict loop: **brief →
produce → checks → independent review → you sign off**. Nothing counts as done until you approve it,
and statutory deadlines always come first.

## Works in any country

The PM adapts to where the project is. At setup you give the project's country and region (state,
province or territory). From then on, the agents work from:
- that place's building code and edition
- its payment law and deadlines
- its safety regime and permits
- its own terms: progress claim, variation and practical completion in Australia; pay application,
  change order and substantial completion in the US

Dates, currency and units follow the country too.

The plugin ships **knowledge packs** that hold this per-country detail:

| Pack | What's in it |
|---|---|
| Australia | In depth. NCC structure, editions and state variations; security of payment (VIC, NSW, QLD); WHS (VIC, NSW); planning pathways (VIC, NSW); five discipline review checklists; a referenced-standards index |
| United States | Starter. The national picture: I-Code adoption, prompt payment, liens and bonds, OSHA and State Plans, AIA and ConsensusDocs contracts, permitting, common referenced standards. **No state-specific law ships**; state files are written the first time a project needs them |
| Template | The empty layout, for any other country |

When a project lands somewhere a pack doesn't cover (a US state, a territory, a new country), the PM
tells you what's missing. With your OK, the knowledge curator researches it from primary sources and
writes it to your own copy. Everything it writes is marked **provisional** until a person checks it.
No agent fills one jurisdiction's gap from another's file.

Knowledge-pack content is a starting point for a professional, not legal advice. Every file says where
it came from, when it was checked and how far to trust it.

## What's in it

**Skills**

| Name | Does |
|---|---|
| `invero-pm:project-manager` | The orchestrator: setup, scans, dashboard, delegation, sign-offs, statutory clocks, daily review |
| `invero-pm:deliverable-build` | Builds client-ready .docx deliverables from 17 report structures; runs the provenance, letterhead and contents checks |
| `invero-pm:knowledge-base` | Reads, lints and extends the country knowledge packs; currency scans |
| `invero-pm:tender-documentation-review` | Reviews a multi-discipline tender set against the previous register and produces the next revision |
| `invero-pm:concise-register-entries` | House style for register, RFI and defects entries |
| `invero-pm:safe-xlsx-update` | Changes a live workbook without destroying images, rich text or your edits |
| `invero-pm:highlight-sow-clarifications` | Cross-checks register references cited in a scope of works (Windows, Word and Excel) |

**Specialist agents**, briefed by the PM:

| Agent | Does |
|---|---|
| `cost-commercial-agent` | Payment claims and changes under the project's payment law: dates first, every reason for withholding, a draft response for your client to serve |
| `programme-intelligence-agent` | Programme/schedule reliability, milestone drift, critical path, early warning, recovery options |
| `tender-analysis-agent` | Tender/bid comparison: scope line by line, price normalisation, exclusions, commercial risk |
| `scope-of-works-agent` | Scope of works for tender, scope schedule, design gap register, addenda |
| `project-health-check-agent` | A client-ready health check of seven pages or fewer, rated by stream |
| `project-reporting-agent` | Weekly and monthly reports, risk and action registers |
| `site-report-agent` | Site observation reports, in observation language, never as supervision |
| `handover-closeout-agent` | Close-out review: completion evidence, defects, certificates, warranties, live dates |
| `document-intelligence-agent` | Answers from the project's own documents, cited to clause and revision; registers on request |
| `code-compliance-agent` | Read-only check against the adopted building code; stops if the edition isn't established |
| `discipline-review-agent` | Read-only review of one discipline's drawings against its checklist |
| `independent-review-agent` | Quality control of a deliverable before sign-off; never calls itself verification |
| `knowledge-curator-agent` | The only writer to the knowledge packs; builds missing regions and countries on your OK |
| `industry-watch-agent` | Currency scan: what changed in the codes and laws, and which projects it touches |
| `pm-project-analyst` | Read-only legwork inside one project folder |

**A safety hook** that holds every Write and Edit to the project boundary (see Scope and safety).

## Requirements

- Claude Code
- Python 3.10+ with `pip install -r requirements.txt` (PyMuPDF, openpyxl, python-docx, Pillow)
- `highlight-sow-clarifications` only: Windows with desktop Word and Excel

## Getting started

Ask Claude to **"set up the PM on `<your project folder>`"**. It asks for:
- an id for the project
- your name
- the project's country and region

Then it:
1. Registers the project with `init_project.py --country <cc> --region <code>`. This creates a
   registration file in `~/.claude/pm-agent/projects/` and a state folder inside the project, with the
   country's defaults.
2. Adjusts `config.json` to match your folder layout.
3. Records the project facts: building code and edition, payment law and its periods, safety regime,
   contract form, and your role. It finds them in the contract and approvals, and asks you for what it
   can't find. It never guesses.
4. Shows which knowledge files apply and which are missing.
5. Shows you a dry-run scan before recording anything.

After that, `/pm` runs the full loop and `/pm all` runs it across every registered project. You can
also ask for "what's waiting on me", "approve the register", "PM dashboard" or "health report".

The default folder layout is a `Drawings/` folder with numbered stage subfolders (`2. Preliminary
Issue`, `3. Tender Issue`, …), plus `Tender/`, `Finance/` and `Programme/`. Everything is configurable;
see [skills/project-manager/reference/setup.md](skills/project-manager/reference/setup.md).

### Make it yours

These all go in the project's `config.json`:

| Setting | What it does |
|---|---|
| `report.letterhead` | Path to your letterhead `.docx`. Every deliverable is built on its headers, footers and margins |
| `templates.dir` | Your controlled template library. Deliverables are checked against your templates instead of the built-in structures |
| `procedures` | Map your management system's procedures (claims, review and issue, document control…). The agents follow and cite them |
| `terminology` | Override any term, e.g. `"client_rep": "Construction Manager"` |
| `tuning` | How long before a sign-off is chased, when a health check goes stale, how close a deadline must be to escalate |

## Example prompts

- "Set up the PM on `D:\Projects\Riverside Fit-out`. It's in Melbourne, Victoria. I'm Sam."
- "Set up the PM on `~/Projects/Austin Tenant Improvement`. It's in Texas."
- "/pm": scans, processes your dashboard answers, briefs whatever is needed, and reports statutory
  dates first, then what changed, then what's waiting on you.
- "Progress claim 7 came in this morning. Assess it." / "Pay application 4 arrived. Review it."
- "Write up today's site visit from my notes and photos."
- "The three tender returns are in. Compare them and recommend." / "Level the bids."
- "Check the tender set against the code for this project."
- "What's waiting on me?"
- "Approve the register sign-off: Rev C is fine, note the ceiling void clash stays open."
- "Give me a client-ready health check."

## Scope and safety

The agents read only the project folder you registered, and write only to the PM's own state folder
and the deliverable folders you allow. That boundary is enforced in code, not just written in a
prompt:
- **The scripts** (`scripts/guard.py`) refuse any path outside it.
- **The hook** (`hooks/hooks.json` → `scripts/scope_hook.py`) runs before every Write and Edit Claude
  makes, the specialists' included:
  - It refuses a write inside a registered project folder unless it's also inside that project's
    writable folders.
  - It refuses any write to a registration file.
  - It doesn't touch work in folders you haven't registered.
- **A registration the agents could edit is refused**, so they can't widen their own scope. Changing
  scope means you editing the registration yourself.

To check the boundary:

```
python skills/project-manager/scripts/test_guard.py
```

Project files are never modified. Registers and deliverables get a new revision; the original is never
overwritten. Email is read and draft only. The agents never issue anything, never serve a notice and
never rename anything to ISSUED. **Only you sign off.**

## What it reads, writes, runs and sends

**Reads**
- Files in the registered project folder: drawing PDFs, registers and cost plans (.xlsx), scopes and
  checklists (.docx), programme exports, contracts. Read-only.
- The plugin's knowledge packs, and your overlay in `~/.claude/pm-agent/knowledge/`.

**Writes**
- The project's state folder (default `<project>/.claude/pm-agent/`): `state.json`, `config.json`,
  logs (`*.jsonl`), `dashboard.html`, `history/` snapshots, drafts, and `deliverables/` (the default
  filing folders).
- In `~/.claude/pm-agent/`:
  - registrations, written by `init_project.py` when you register a project
  - the practice lessons playbook and proposals, in `practice/`
  - the knowledge overlay, in `knowledge/`
  - currency-scan snapshots, in `cache/`
- Deliverables in project folders only where you've added that folder to the registration's
  `extra_write`.

**Runs**
- **Python scripts** bundled in the plugin: scan, dashboard, health report, the document build chain
  and its checks, and the knowledge-pack tools.
- **The PreToolUse hook**, on every Write and Edit. It's a short Python check and doesn't touch the
  network.
- **Optionally `serve_dashboard.py`**, a local web server bound to `127.0.0.1` (port 8765 by default).
  It serves the dashboard and appends your answers and chat messages to the state folder. Other
  machines can't reach it.
- **`highlight-sow-clarifications`** runs PowerShell to drive the desktop Word and Excel already open
  on your machine, through COM automation (Windows only).
- **`safe-xlsx-update`** may open Excel through COM, read-only, to check a workbook before it's saved
  (Windows only).

**Sends and fetches**
- **No network requests during normal running**, and no telemetry.
- **Two network uses, and each needs your request:**
  - **A currency scan.** `kb-watch-sources.py` fetches the public pages listed in each knowledge
    pack's `_meta/sources.json` (legislation registers, code bodies, safety regulators) to see what
    changed.
  - **Knowledge research.** The knowledge curator uses web search and fetch to build a missing state
    or country file. The PM asks you first.
- **File content** Claude reads while working is processed by Anthropic as part of your Claude
  session, under your Claude plan's terms.
- **The email watch** runs only if you've connected an email connector. It searches your mailbox for
  project mail and never sends, labels or deletes.
- **Python packages** are installed by you, from `requirements.txt`. The plugin installs nothing.

## Rules and lessons that survive updates

The plugin is replaced on every update, so nothing that's yours lives inside it:
- **Each project's state folder** has `project-notes.md` (rules for that project only) and
  `lessons.md` (what the PM's daily review learned on that project).
- **`~/.claude/pm-agent/practice/lessons.md`** is the practice playbook: lessons that apply across
  projects, indexed, with client details removed.
- **`~/.claude/pm-agent/knowledge/`** holds your knowledge packs and corrections.

The agents read all of these at the start of every run, and never edit the plugin's own files.

## Setup and support

Free to use under the MIT licence. Paid setup, customisation and support for firms are available
through Invero Projects: see [SUPPORT.md](../../SUPPORT.md) or email james@inveroprojects.com.au.
