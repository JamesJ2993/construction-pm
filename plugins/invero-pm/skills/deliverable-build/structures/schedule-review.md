---
deliverable: {{Schedule}} Review
aliases:
  - Programme Review
  - Schedule Review
filing: programme_review
toc_exempt: false
required_sections:
  - Executive summary
  - Basis and what was reviewed
  - Position at the data date
  - Milestone movement
  - Critical path and float
  - Delay events and their treatment
  - Recommendations
  - Basis and information gaps
---

# Report structure — {{Schedule}} Review

**Produced by the programme-intelligence-agent.** The structure every {{schedule}} review follows.

This file is authoritative on **section order and section contents**. The agent config governs everything else — filenames, where to save, draft status, evidence rules. Where this file and the agent config disagree on structure, this file wins.

Output: `<job no.> - {{Schedule}} Review - YYYY-MM-DD - RevA.docx`, filed to the `filing.programme_review` folder (config.json).

The `.docx` is built per the `deliverable-build` skill — on the firm's letterhead where one is configured.

Seven pages is a ceiling, not a target. In markdown, hold under about 2,500 words.

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

**Analysis or Review?** A *{{Schedule}} Analysis* interrogates one submitted {{schedule}} against the contract. A *{{Schedule}} Review* asks whether the {{schedule}} can be relied on at all and where the project actually stands. Neither determines entitlement — that is an **{{time_extension}} Assessment**, and it is determined by a person.

---

## Title page

Project · Client · {{Schedule}} reviewed · Baseline compared against · Contractual Date for Completion · Position date of this review · Revision · Prepared by · Status · Commercial-in-Confidence.

## 1. Executive summary

- **The headline** — One paragraph. Whether the {{schedule}} held as a control document, and what the project's real position is against the contractual completion date. Lead with the answer.
- **Assessed position** — Forecast completion, the variance to the contractual date in working days, and the confidence attaching to that assessment.
- **The three findings that drive this**
- Numbered list.

## 2. Basis and what was reviewed

- **Documents read** — Each {{schedule}} file, its revision, its declared data date and its file date. Where the two disagree, say so — a {{schedule}} whose data date is not the date it was issued cannot be read at face value.
- **Contract form** — the standard form in `project_facts.contract_form`, or bespoke. The form changes how time is governed, so name it. If it is bespoke, say which clauses govern time, {{time_extension}} and liquidated damages.
- **What this review is not** — Not a formal delay analysis, not a critical path method assessment where the source file carries no logic, and not a determination of any party's entitlement to time or cost.

## 3. Is the {{schedule}} reliable?

- Table — `Test · Finding`
- **What would need to change for this {{schedule}} to be relied on** — A specific, short list the programmer can act on. Not 'improve the {{schedule}}'.

## 4. Position at the data date

- **Contractual Date for Completion** — Date, and the document it comes from. Where two documents state different times on the same day, record both.
- **Baseline forecast completion** — Date and variance to contractual.
- **Contractor's current forecast** — Date, or 'not stated — no update has been issued', which is itself a finding.
- **The PM's assessed forecast** — Date or range, with the basis. Label it an estimate.
- **Working days remaining** —  
- **Total float to completion in the baseline** —  
- **Liquidated damages exposure** — Rate per day and the clause.

## 5. Milestone movement


**{{Client}}-side milestones**

- Table — `Milestone · Contractual date · Baseline date · Current forecast · Movement this period · Cumulative drift`

**Contractual milestones**

- Table — `Milestone · Contractual date · Baseline date · Current forecast · Movement this period · Cumulative drift`

**{{Schedule}} milestones (no contractual force)**

- Table — `Milestone · Baseline date · Current forecast · Movement this period`
- **Activities absent from the {{schedule}}** — Any contractually required activity that does not appear. An absent activity cannot slip, and that is the point.

## 6. Critical path and float

- **The critical path** — As computed by the {{schedule}}. Where the file carries no logic, state that this is the practice's reconstruction from trade sequence, not the {{schedule}}'s output — and label it as such every time it is relied on.
- **Near-critical paths** — Paths within [n] days of critical.
- **Where the float went** — Whether contingency or float was consumed before work started, and by what.

## 7. Delay events and their treatment

- **Events recorded** — Each event, its date, its cause as recorded, and whether a notice was served within the contractual period.
- **Notices** — Served, late or absent. A late notice may bar entitlement — say so without determining it.
- **What this review does not determine** — Entitlement to an {{time_extension}} or to delay costs. That is an {{time_extension}} Assessment, produced separately under the {{time_extension}} Assessment template and determined by a person.

## 8. Recommendations

- **Immediate**
- Numbered list.
- **This month**
- Numbered list.
- **Before the next {{schedule}} update**
- Numbered list.

## 9. Basis and information gaps

- **What was read** — Each document, with revision, date and source.
- **Missing because it is overdue. (These are findings.)**
- Bulleted list.
- **Missing because it is early. (These are not findings.)**
- Bulleted list.
- **What could not be verified** —  
- **Assumptions made** —  
- **Status of this report** — DRAFT — for review. {{Schedule}} positions are issued by a person, not by an analysis. Verification is the owner's at sign-off — the review-and-issue procedure, the sign-off record.

---

## Fixed elements

- Marked `DRAFT — for review`.
- Every reliability test in section 3 is run and recorded, **including the ones that pass**. A reliability assessment listing only failures reads as advocacy.
- Where the source file carries no logic, any critical path stated is the practice's reconstruction from trade sequence — labelled as such **every time it is relied on**, not once in a footnote.
- Where no {{schedule}} update has been issued, movement is recorded as *not measurable*, never as zero.
- An activity that is contractually required but absent from the {{schedule}} is a finding. An absent activity cannot slip, and that is the point.
- No entitlement to time or cost is determined.
