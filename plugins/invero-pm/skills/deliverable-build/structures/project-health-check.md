---
deliverable: Project Health Check
aliases:
  - Health Check
filing: health_check
toc_exempt: false
required_sections:
  - Health indicator summary
  - Stream findings
  - Recommendations
  - Basis and information gaps
---

# Report structure — Project Health Check

**project-health-check-agent.** The structure every health check follows.

This file is authoritative on **section order and section contents**. The agent config governs
everything else — filenames, where to save, draft status, evidence rules. Where this file and the agent config disagree on structure, this file wins.

Output: `<job no.> - Project Health Check - YYYY-MM-DD - RevA.docx`, filed to the `filing.health_check` folder (config.json).

The `.docx` is built per the `deliverable-build` skill — on the firm's letterhead where one is configured.

**Seven pages is a ceiling, not a target.** The ceiling binds the `.docx`; in markdown, hold under
about 2,500 words. A thin project produces a shorter report — do not pad.


## House presentation rules

These bind every `.docx` built from this structure, above the section order below.

1. **Contents page, then executive summary.** After the title page comes a contents page — a
   `[[TOC]]` marker in the draft, made live by `insert-toc.py` — then the executive summary. It is
   a house element, not a numbered section, and never counts against a page budget.
2. **Prose over tables.** A table earns its place only for a genuine register or matrix — risk and
   action registers, milestone movement, comparison and classification matrices, drawing registers,
   pricing build-ups. Everything else is prose and headed lists.
3. **Start from the controlled structure, never a blank page.** Where the firm keeps a controlled
   template for this deliverable (`config.json → templates.dir`), start from it; otherwise follow
   this file's sections. `check-provenance.py` checks the required sections survived.
4. **Write in the project's terms.** A `{{key}}` in this file stands for the project's terminology
   (`kb_resolve.py --terms`): {{client}}, {{schedule}}, {{change}}, {{payment_application}} and so
   on. Write the deliverable in those words, never the placeholder.

**Build chain.** Follow the `deliverable-build` skill exactly — it carries the script chain and the
`--check` gates.

---

## Page 1 — Title page

Project · client · **data date** · revision · prepared by (the firm) ·
commercial-in-confidence.

Also: the previous health check this one compares against, or a note that this is the first.

## Page 2 — Health indicator summary

The whole answer one page.

One row per stream, **all six shown** even where a stream is not applicable, so the reader sees
nothing was skipped:

`Stream · Rating · One-line basis`

| Stream | Drawn from |
|---|---|
| {{Schedule}} | the project's {{schedule}} folder |
| Cost & Commercial | the project's cost and commercial folder |
| Design & Documentation | the project's design and drawings folder |
| Procurement | the project's procurement and {{tender}} folder |
| Site & Safety | the project's site and delivery folder |
| Project Governance | the project's project admin folder, the project's client correspondence folder, the project's reporting folder |

Then **the overall rating with its reason**. Driven by the worst stream, never an average. Streams
rated not applicable are excluded entirely.

Five permitted ratings — no others:

| Rating | Meaning |
|---|---|
| Green | Evidenced as tracking to plan. Requires evidence, not merely absence of bad news |
| Amber | A live issue with a known path back. Something specific must be named |
| Red | Material threat to time, cost, quality or safety — **or a control absent altogether** |
| Insufficient information | The folder does not contain what is needed. Never a euphemism for Red |
| Not applicable | Phase not yet reached. State the phase reason |

**The test separating Red from insufficient information: was the document due yet?** Establish it
from the {{schedule}}.

## Pages 3–5 — Stream findings

One short block per stream: rating · what the evidence shows · what it means.

**These blocks flex in both directions.** Cut them when findings overrun; let them compress to a
line or two each when there is little to say. Four blocks reading "the folder is empty and here is
why that matters" is a correct report on an unpopulated project.

Do not pad by restating another agent's analysis — that duplicates a document the practice has issued and buries
the finding.

**Governance findings are grouped by the party who owns them** — The practice's to resolve, then the
{{Client}}'s. State our own gaps plainly and first. An undifferentiated list reads as either
self-flagellation or blame-shifting.

## Page 6 — Recommendations

Dot points, grouped by urgency: **immediate · this month · this quarter**.

Each one:

- Tied to a specific finding
- Names a party — The practice, client, contractor, consultant. An unowned recommendation is noise
- Names a timeframe
- Says what it resolves: "obtain X so that Y can be rated / so that Z stops accruing"
- Where the fix is to get a document that does not exist, says who holds it

No generic project management advice. *"Improve communication"* is not a recommendation.

## Page 7 — Basis and information gaps

- **What was read**, with dates
- **What was missing**, split into *empty because neglected* (the findings) and *empty because
  early* (correct, not findings)
- What could not be verified
- Assumptions made
- Status of the report

**Never drop this page.** On a poorly documented project it is the most valuable page in the
report, and often the longest.

---

## Fixed elements

- Marked `DRAFT — for review`
- Every rating cites the document and date behind it. **A rating with no citation is downgraded to
  insufficient information**
- **Absence-driven ratings cite the folder path and sweep date** — "the project's cost and commercial folder, empty at 20 July 2026". That is a citation
- Carry the caveat that an empty folder proves **The practice does not hold the document**, not that it
  does not exist
- Where the position differs from the last issued report or a prior agent output, say so and say
  why
- State on page 7 that this is **not a certification, audit, assurance opinion or due diligence
  report**
