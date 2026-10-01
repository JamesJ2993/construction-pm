---
deliverable: Cost Report
aliases: []
filing: cost_report
toc_exempt: false
required_sections:
  - Executive summary
  - Basis of report
  - Contract award reconciliation
  - Committed cost position
  - Client-side billing
  - {{Change_plural}}
  - {{Retention}}, security and final-claim readiness
  - Forecast final cost
  - Recommendations
  - Basis and information gaps
---

# Report structure — Cost Report

**Produced by the project-reporting-agent, cost stream.** The structure every cost report follows.

This file is authoritative on **section order and section contents**. The agent config governs everything else — filenames, where to save, draft status, evidence rules. Where this file and the agent config disagree on structure, this file wins.

Output: `<job no.> - Cost Report - YYYY-MM-DD - RevA.docx`, filed to the `filing.cost_report` folder (config.json).

The `.docx` is built per the `deliverable-build` skill — on the firm's letterhead where one is configured.

Six pages is a ceiling, not a target. In markdown, hold under about 2,200 words.

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

## Read this first

This is the **cost stream only**. It is not a monthly report and must not be padded into one. Where a monthly report is what was asked for, use the Project Reporting structure instead.

---

## Title page

Project · Client · Report type · Reporting period · Data date · Revision · Prepared by · Distribution · Currency · Commercial-in-Confidence.

## 1. Executive summary

- **Status at the data date** — Five cost streams, each rated and each given a trajectory. All five appear even where one is not applicable, so the reader sees that nothing was skipped.
- Table — `Stream · Status · Trajectory`
- **The headline position** — All figures ex {{sales_tax}} at the data date. Every line states its basis. Where a position cannot be stated, say so in the table rather than omitting the line — an absent row reads as a nil balance.
- Table — `Position · Amount · Basis`
- **The three things that matter** — Three, not ten. Each one names the amount at risk, the instrument that is missing or contradicted, and the consequence if it is not resolved. Anything smaller belongs in the body.
- Numbered list.
- **What is required, and by when** — Each row names a document or a decision, the party who holds it, and a date driven by a contractual or statutory event — not by convenience.
- Table — `# · Required · From · By`

## 2. Basis of report

- **Scope** — What this report covers and, just as important, what it does not. State plainly that it is a cost position drawn from documents on the project file, not an audit, a certification or a due diligence report.
- **Evidence rules applied** — State the rules the figures obey so the reader can test them.
- Bulleted list.
- **Parties, as the source documents record them** — Legal entity names and ABNs exactly as they appear on the instruments — not as they are spoken about on site.
- Table — `Role · Party`

## 3. Contract award reconciliation

- **The {{tender}} field** — {{Tenderer}}s and totals, ex {{sales_tax}}, with the variance to the lowest. This is a genuine comparison matrix, so a table is warranted.
- Table — `{{Tenderer}} · {{Tender}} total (ex {{sales_tax}}) · Variance to lowest`
- **{{Tender}} to contract** — Whether the executed contract price matches the accepted {{tender}}, and what explains any difference.
- **Contract to purchase order** — Whether the base purchase order matches the executed contract sum.
- **The reconciliation result** — Stated as a single figure with a direction.

## 4. Committed cost position

- **What is committed by purchase order** — Each PO, its value, and what it covers. State the total.
- **What is committed outside the purchase-order system** — Commitments evidenced by invoice or instruction but not covered by a PO. This is a control finding, not merely a number — say so.
- **What is uncommitted** — Scope that must still be let, and the budget line it will draw against.

## 5. Client-side billing

- **What has been invoiced to the client** — Each invoice: number, date, amount, what it covers, and whether the supporting cost schedule is held.
- **What cannot be substantiated** — Any invoiced amount for which the supporting schedule or breakdown is not on file. Name the amount. An unsubstantiated invoice is a finding even where nobody has queried it.

## 6. {{Change_plural}}

- **The {{change}} position** — Approved, submitted and anticipated, each as a count and a value.
- Table — `{{Change}} · Description · Value (ex {{sales_tax}}) · Approval instrument · Status`
- **{{Change_plural}} billed without an approval instrument** — The total, and each one named. Where nothing has been billed without approval, say so explicitly.

## 7. {{Retention}}, security and final-claim readiness

- **{{Retention}} or security held** — The percentage, the basis in the contract, and the amount. Where the contract contradicts itself on the percentage, set out both readings and state that a ruling is required before the final claim.
- **Release dates** — {{Completion}} release and end-of-defects release, each with the clause that governs it.
- **Statutory payment dates** — For every live claim, the statutory periods recorded in `project_facts.payment_periods` — the {{payment_response}} deadline and the payment due date, each with the section of the payment law that fixes it, and the contract's own periods where shorter. Where the payment law bars a reason omitted from the {{payment_response}}, say so. A date with no recorded period is stated as unverified, never estimated.

## 8. Forecast final cost

- **The forecast** — Contract sum, plus approved {{change_plural}}, plus assessed anticipated {{change_plural}}, plus remaining contingency drawdown.
- **Where a forecast cannot be stated** — Say so plainly and give the reason — most often that no approved budget or cost plan is held. Do not manufacture a forecast from an unapproved figure.
- **Contingency** — Original, drawn, remaining, and the rate of drawdown against {{schedule}}.

## 9. Recommendations

- **Immediate**
- Numbered list.
- **This month**
- Numbered list.
- **This quarter**
- Numbered list.

## 10. Basis and information gaps

- **What was read** — Each document, with its revision, date and where it came from.
- **Missing because it is overdue. (These are findings.)**
- Bulleted list.
- **Missing because it is early. (These are not findings.)**
- Bulleted list.
- **What could not be verified** —  
- **Assumptions made** —  
- **Where this differs from the last issued report, and why** —  
- **Status of this report** — DRAFT — for review. This is a management cost report. It is not a certification, an audit, an assurance opinion or a due diligence report, and it does not determine any party's entitlement. Verification is the owner's at sign-off — the review-and-issue procedure, the sign-off record.

---

## Fixed elements

- Marked `DRAFT — for review`.
- Every figure carries a basis — **Actual** (an instrument on file, cited), **Derived** (arithmetic from actuals, working shown) or **Estimate** (labelled, with the reason no better figure exists). **A figure with no basis is not reported.**
- All figures ex {{sales_tax}} unless expressly stated, and the currency is named on the title page.
- Where a position cannot be stated — most often forecast final cost with no approved budget on file — say so and give the reason. Never manufacture a forecast from an unapproved figure.
- Legal entity names and ABNs exactly as they appear on the instruments.
- Security of payment dates stated for every live claim — the claims procedure.
- State that this is not a certification, audit, assurance opinion or due diligence report.
