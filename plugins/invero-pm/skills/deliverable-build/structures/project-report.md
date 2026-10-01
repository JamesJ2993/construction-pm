---
deliverable: Project Report
aliases:
  - Monthly Report
  - Weekly Report
  - Project Reporting
filing: report
toc_exempt: false
required_sections:
  - Executive summary
  - Risk register
  - Action register
  - Information gaps and assumptions
---

# Report structure — Project Report

**project-reporting-agent.** The structure every weekly and monthly report follows.

This file is authoritative on **section order and section contents**. The agent config governs
everything else — filenames, where to save, draft status, evidence rules. Where this file and the agent config disagree on structure, this file wins.

Output: `<job no.> - Monthly Report - YYYY-MM - RevA.docx` / `<job no.> - Weekly Report - YYYY-MM-DD - RevA.docx`,
filed to the `filing.report` folder (config.json).

Every `.docx` produced under this structure is built per the `deliverable-build` skill — on the
firm's letterhead where one is configured.

**Confirm the cycle before writing.** Weekly reports are short and operational; monthly reports
are fuller and commercial. Do not pad a weekly into a monthly.


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

Project · client · report type and period · data date · revision · prepared by (the firm)
· distribution list · commercial-in-confidence notice.

Use the **period end date**, not the date the report was run.

## 2. Executive summary — one page

Written for a reader who will read nothing else and may need to decide something this week.

- Lead with **status and trajectory** — on {{schedule}} / behind / recovering, on budget / forecast
  overrun, and the direction of travel since last period
- Then the **two or three things that matter**, with their consequence
- Then **what is required from the client**, with dates
- No methodology, no restatement of detail, no throat-clearing

Carry a status indicator per stream — {{schedule}} / cost / design / safety — applied consistently
across periods. **A status that improves must be explainable by something that actually
happened.**

## 3. Detailed report sections

In this order:

1. **Period and data date** — reporting period, data date, revision, distribution list
2. **Progress this period** — what was actually completed, with evidence
3. **{{Schedule}} status** — % complete vs planned, forecast completion, variance against baseline
   in working days, critical path commentary
4. **Cost status** — approved budget, committed, spent to date, forecast final cost, variance;
   {{change_plural}} approved / pending / anticipated
5. **Design and approvals** — open RFIs, outstanding approvals, authority status
6. **Procurement** — packages awarded this period, packages still to let against need-by dates
7. **Site, quality and safety** — inspections, non-conformances, incidents
8. **Risks** — see section 4
9. **Actions** — see section 5
10. **Look-ahead** — what is planned next period, and what the project needs from the client to
    achieve it

Quantify wherever the data allows. *"Slab pour delayed"* is weak. *"Level 2 slab pour delayed 9
working days; critical path; forecast completion moves from 14 to 27 March 2026"* is a report.

## 4. Risk register

Live, carried forward each period. Each risk holds:

| Field | Notes |
|---|---|
| ID | **Stable across the project — never renumber** |
| Risk | Cause → event → consequence, not a one-word topic |
| Category | {{Schedule}} / Cost / Design / Approvals / Site / Commercial / External |
| Likelihood × Consequence | Consistent scale, stated at the top of the register |
| Rating | Derived, with movement since last period (↑ ↓ →) |
| Cost / time exposure | Quantified where possible, "unquantified" where not |
| Mitigation | The action being taken |
| Owner | A named party — The practice, client, contractor, consultant |
| Status | Open / Mitigated / Closed / Realised |
| Raised / last reviewed | Dates |

- A risk that has **occurred** is no longer a risk — close it, move it to an issue or {{change}},
  and say where it went
- Every High risk needs a stated mitigation and a named owner. If it has neither, **that absence
  is the reporting point**
- Show the movement. A register identical to last month has not been reviewed, or the project is
  not being managed — flag it either way

## 5. Action register

Each action: ID · description · owner · date raised · due date · status · source document.

- Reconcile against the previous period: closed, still open, newly raised, overdue
- **Report overdue actions separately and prominently**, with days overdue and owner — this is
  the single most useful thing in the report, because actions decay quietly
- Client-owned actions also appear in the executive summary's "required from client", with the
  date needed by
- **Never close an action without evidence.** If it looks done but nothing confirms it, mark it
  "believed closed — confirmation required"

## 6. Information gaps and assumptions

What was missing, what was assumed.

## 7. Appendices

Progress photos, {{schedule}} extract, cost summary, as relevant.

---

## Fixed elements

- Marked `DRAFT — for review`
- **Reporting is cumulative.** Each report carries forward the previous period's risks and
  actions and shows what moved. A report that silently drops an item is a defect
- **The weekly carries the cumulative rule too**, at a lower resolution. It runs a single
  *risks and actions — what moved* section using the same IDs as the monthly, showing rating,
  movement and what changed, plus anything realised and anything overdue. The mitigations and
  the full register stay in the monthly. Sections 3.4 to 3.6 — cost, design and approvals,
  procurement — are monthly-only; a weekly reports cost as a status indicator and nothing more
- Start by reading the previous report — it sets the carry-forward baseline and the established
  format for that client
- Every figure cites document name, date, page or line
- Actual / forecast / estimate distinguished in every cost and {{schedule}} statement

## Where it does not apply

Live `.xlsx` registers — risk, action — go to the project's reporting folder and are updated
in place each cycle rather than versioned. Their own columns carry the history.
