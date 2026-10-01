---
deliverable: {{Schedule}} Analysis
aliases:
  - Programme Analysis
  - Schedule Analysis
filing: programme_review
toc_exempt: false
required_sections:
  - Executive summary
  - Milestone movement
  - Critical path commentary
  - Early warning register
  - Recovery options
  - Information gaps and assumptions
---

# Report structure — {{Schedule}} Analysis

**programme-intelligence-agent.** The structure every {{schedule}} analysis follows.

This file is authoritative on **section order and section contents**. The agent config governs
everything else — filenames, where to save, draft status, evidence rules. Where this file and the agent config disagree on structure, this file wins.

Output: `<job no.> - {{Schedule}} Analysis - YYYY-MM-DD - RevA.docx`, filed to the `filing.programme_review` folder (config.json)

The `.docx` is built per the `deliverable-build` skill — on the firm's letterhead where one is configured.


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

## 1. Title page

- Project · client
- **{{Schedule}} revision and data date analysed**
- **Baseline compared against**
- Report date · revision · prepared by (the firm)
- Commercial-in-confidence notice

The data date is the {{schedule}}'s, not the date the analysis ran. Both {{schedule}}s must be named —
a comparative analysis with only one {{schedule}} identified cannot be checked.

## 2. Executive summary

Written as prose, not a grid. It carries, in this order:

- The two {{schedule}}s named — the one analysed and the baseline — each with revision and data date
- Status, current forecast completion, and variance against baseline **in working days**
- **Whether the {{schedule}} is reliable**, answered here in a sentence
- **The point of no return** — the date beyond which the current completion date cannot be
  recovered without an intervention the {{Client}} has not approved

The structural tests behind the reliability answer — open ends, thin logic, negative float,
constraint abuse, unrealistic durations, calendar issues — follow immediately as their own
section, as a headed list with a finding against each.

Reliability belongs here, at the front, not in a footnote. Every conclusion below inherits the
defects of the {{schedule}} it came from. If the {{schedule}} is not fit to be relied on, say so here
and say what would need to change.

## 3. Milestone movement table

One row per milestone. Columns:

`Milestone · Contractual date · Baseline date · Current forecast · Movement this period · Cumulative drift`

Group into contractual milestones, {{schedule}} milestones, and **{{Client}}-side milestones**.
{{Client}}-side items go first or are flagged — they are the only ones the client controls.

Show drift period on period. A milestone moving a few days each update is a trend, and the trend
is the finding.

## 4. Critical path commentary

- The driving chain **in plain language**, not a list of activity IDs
- Near-critical paths — low total float, tomorrow's critical path
- **Logic changes since the last update** — relationships added, removed, re-sequenced
- External and {{Client}}-side dependencies, separated from contractor-controlled work

Undisclosed logic change is the most common way a {{schedule}} shows a completion date it has not
earned. Always compare, always report.

## 5. Early warning register

Indicators ranked by exposure. Each carries **the date it becomes irrecoverable**.

Cover: activities trending late · float erosion rate · progress vs planned divergence ·
procurement against need-by dates · open RFIs and approvals on or near critical path.

The point of no return is the single most valuable line in the report. Never omit it because it
is hard to calculate — state it as a range if that is what the evidence supports.

## 6. Recovery options

For each option: what it involves · what it costs · what it requires and from whom · how much
time it recovers.

**Include doing nothing, with its consequence.** An options list without the null option is a
recommendation disguised as an analysis.

## 7. Information gaps and assumptions

- What could not be read or was not provided
- Assumptions made, particularly about **calendars and working days**
- Where the {{schedule}} conflicts with minutes or site evidence, both positions with sources

---

## Fixed elements

- Marked `DRAFT — for review` at the front
- Every date cites {{schedule}} name, revision, data date, activity ID
- Actual / forecast / estimate distinguished in every statement
- Delay characterised as excusable / compensable / contractor-culpable is **always marked
  preliminary**
- No formal delay analysis, no entitlement determination

## Where it does not apply

Live trackers built as `.xlsx` — early warning registers, milestone movement — go to
the project's reporting folder and are updated in place. They carry their own columns and do
not follow this structure.
