---
deliverable: {{Payment_application}} & {{Change}} Assessment
aliases:
  - {{Payment_application}} Assessment
  - {{Change}} Assessment
  - Claim Assessment
  - Progress Claim Assessment
  - Variation Assessment
  - Pay Application Assessment
  - Change Order Assessment
filing: claim_assessment
toc_exempt: false
required_sections:
  - Statutory and contract dates
  - Executive summary
  - Basis and information gaps
---

# Report structure — {{Payment_application}} & {{Change}} Assessment

**cost-commercial-agent.** The structure every claim and {{change}} assessment follows.

This file is authoritative on **section order and section contents**. The agent config governs
everything else — filenames, where to file, draft status, evidence rules. Where this file and the
agent config disagree on structure, this file wins.

Output, filed to the `filing.claim_assessment` folder (config.json):
`<job no.> - {{Payment_application}} Assessment - Claim nn - RevA.docx`
`<job no.> - {{Change}} Assessment - <change no.> - RevA.docx`

The `.docx` is built per the `deliverable-build` skill — on the firm's letterhead where one is configured.

## House presentation rules

These bind every `.docx` built from this structure, above the section order below.

1. **Contents page, then the dates.** After the title page comes a contents page — a `[[TOC]]`
   marker in the draft, made live by `insert-toc.py` — then the dates panel (below), then the
   executive summary. The contents page never counts against a page budget.
2. **Prose over tables.** A table earns its place only for a genuine register or matrix — the dates
   panel, the valuation build-up, the cumulative {{change}} position. Everything else is prose.
3. **Start from the controlled structure, never a blank page.** Where the firm keeps a controlled
   template for this deliverable (`config.json → templates.dir`), start from it; otherwise follow
   this file's sections. `check-provenance.py` checks the required sections survived.
4. **Write in the project's terms.** A `{{key}}` in this file stands for the project's terminology
   (`kb_resolve.py --terms`). Write the deliverable in those words, never the placeholder.

**Build chain.** Follow the `deliverable-build` skill exactly — it carries the script chain and the
`--check` gates.

## Three artefacts, three jobs

A claim produces up to three documents, and confusing them is the fastest way to lose a dispute.
They are not alternatives.

| Artefact | What it is | Format |
|---|---|---|
| `<job no.> - Claims.xlsx` | **The assessment workbook.** One sheet per claim, item-by-item arithmetic, claimed {{change_plural}} split from base works, the reasons table, and the date calculator | `.xlsx` |
| `<job no.> - {{Payment_application}} Assessment - ... .docx` | **The determination.** The reasoned position that goes to the {{client}}, built to the section order below. Disputes turn on reasoning, and a spreadsheet argues badly | `.docx` |
| `<job no.> - {{Payment_certificate}} - ... .docx` | **What the {{client}} sees.** One page, figures only | `.docx` |

The **{{payment_response}} that is actually served** is none of these. Where the payment law
prescribes a form or content, it is a formal letter on the firm's correspondence template, and it
is served by a person — never by an agent.

{{Change_plural}} run the same way: a `{{Change_plural}}.xlsx` assessment workbook and a
{{change}} assessment `.docx` as the determination.

### The {{payment_certificate}} — a recorded exemption

The {{payment_certificate}} is **one page and carries no contents page**. The deviation is
deliberate and recorded here: there is no `[[TOC]]` marker, `insert-toc.py` is not run, and
`insert-toc.py --check` returns check-fail on it by design. The letterhead check still binds.

Two things bind it. It states the **capacity** the firm holds under the contract
(`project_facts.role`) rather than assuming one — where the firm is not the {{client_rep}}, the
certificate is a recommendation to the {{client}} and says so on its face. And it certifies the
amount payable **and nothing further**: not an approval of the work, not an acceptance that it is
free from defect, and no waiver of any right of the {{client}}.

### The date calculator

The workbook computes every date with `WORKDAY` against a **non-working days** sheet that the
project must populate — every public holiday in the project's region, and **any period the payment
law excludes from its count** (some jurisdictions exclude a holiday shutdown; the knowledge pack's
regional payment file says which, and names the section). An empty sheet silently excludes weekends
only, and the dates it produces will be wrong. Populate it, then check every computed date by hand.
The sheet is a calculator; the statute and the contract are the authority.

## The dates rule — above everything else in this file

**The dates panel appears immediately after the title page and the contents page, before the
executive summary.** Not in an appendix, not at the end, not folded into the summary prose. A reader
who opens the report and closes it ten seconds later must leave knowing the {{payment_response}}
deadline.

**Every period comes from the project's recorded facts, never from memory.** The statutory periods
are recorded in `project_facts.payment_periods` at setup, each with the section of the payment law
that fixes it; the contract's own periods are in `project_facts.contract_periods`. Where a period is
missing, the assessment does not guess it: it states the date as **unverified**, names what would
fix it, and the hand-back is `partial` with the gap named. Where the contract sets a shorter period
than the statute, the shorter governs.

This is the one section-order rule in this file that no commission may vary.

---

# Part A — {{Payment_application}} Assessment

## 1. Title page

Project · {{client}} · **claim number and claimed amount** · date of service or submission of the
claim · revision · prepared by (the firm) · **Commercial-in-Confidence** notice.

Also: the contract form applied (`project_facts.contract_form`) and the **applicable payment law
and jurisdiction** (`project_facts.payment_law`, `region`). On a project outside the firm's usual
jurisdiction this is not optional — periods do not transfer between jurisdictions.

## 2. Statutory and contract dates

A table, and one of the few in this file. One row each, with the basis column naming the section
of the statute or the clause of the contract:

| Item | Date | Basis |
|---|---|---|

- Date and **method** of service or submission of the claim
- **{{Payment_response}} deadline** — the statutory period or the contract period, whichever is
  shorter. Show the working-day count.
- **Payment due date** — the contract terms, within any statutory cap.
- Any **notice, lien or bond deadline** the payment law attaches to this claim (some jurisdictions
  run preliminary-notice or lien-recording clocks alongside the payment cycle).
- Whether an excluded period falls in the window.

Then, in bold prose beneath: **working days remaining as at the assessment date**, and an explicit
statement where the deadline is inside `tuning.deadline_horizon_bdays` working days or has passed.

## 3. Executive summary

Claimed, assessed, and the difference, in one short block of prose. The principal reasons for the
difference in a sentence each. Whether the assessment is complete or conservative pending
verification.

## 4. Assessment of the claim

The valuation build-up — a genuine pricing matrix, and it stays a table: claim line, claimed amount,
assessed amount, basis, reference.

Beneath it, prose on the significant lines only. Do not narrate every line of a fifty-line claim;
narrate the ones that moved and say the rest were assessed as claimed.

State explicitly how physical progress was verified, and where it was not.

## 5. Reasons for withholding

**The section a dispute turns on.** Every reason, each with its amount and its reference. Work
through the categories explicitly and record "none identified" where that is the answer:

valuation · defects · incomplete work · set-off · liquidated damages · back charges · other

A category considered and cleared is recorded as considered and cleared. Under many payment laws a
reason omitted from the {{payment_response}} cannot be raised later; treat every jurisdiction as
one of them unless the knowledge pack says otherwise.

## 6. {{Change_plural}} and time-related costs included in the claim

Each assessed on its merits, per Part B. Cross-reference any standalone {{change}} assessment.

## 7. {{Payment_response}}

The draft for the **{{client}} to serve or issue** — the firm prepares, the {{client}} (or the
{{client_rep}} where the contract gives it that job) serves. It carries every reason from section 5,
in the form the payment law and the contract require.

State plainly that the firm does not serve it, and that service and its date and method must be
recorded.

## 8. Basis and information gaps

What was read with dates, what was missing, what could not be verified, assumptions made, and the
conflict check. Where any date rests on a `provisional` knowledge-pack entry, say so. Where the
claim is significant, recommend that the {{client}} confirm the statutory position with their
lawyers.

---

# Part B — {{Change}} Assessment

## 1. Title page

Project · {{client}} · **{{change}} number and claimed amount** · date of the direction · revision ·
prepared by · Commercial-in-Confidence. Contract form and applicable payment law, as Part A.

## 2. Executive summary

Claimed, assessed, difference. Time claimed, time assessed. Whether a {{change}} exists at all.

## 3. Does a {{change}} exist

Under the contract: the clause relied on, the direction, **who gave it and whether they held
authority**, and whether it was in the required form and given within the contract's notice period.
This section can end the assessment — if no {{change}} exists under the contract, say so here and
value nothing. Where a notice was late, record it as a finding and assess the merits as well:
several jurisdictions let a tribunal set aside an unfair time bar.

## 4. Valuation

The mechanism applied, **in the contract's order** — typically agreed price, then schedule of rates,
then reasonable rates — stating which limb was used and **why the earlier limbs did not apply**. The
build-up as a table; the reasoning as prose.

## 5. Time

Assessed separately from cost. Whether time is claimed, whether the {{schedule}} evidences it, and
whether a {{time_extension}} assessment has been or should be commissioned from
`programme-intelligence-agent`. A {{change}} may carry cost without time, or time without cost.

## 6. Causation

Where the {{change}} traces to an RFI response or a drawing revision, the trace through document
control and **who caused it** — that determines who bears it. Drawing numbers with revisions, RFI
numbers, dates.

## 7. Cumulative position

{{Change_plural}} to date against the contract sum and contingency, and the forecast. A register,
and it stays a table.

## 8. Basis and information gaps

As Part A section 8.
