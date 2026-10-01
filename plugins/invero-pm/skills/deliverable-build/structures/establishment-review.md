---
deliverable: Establishment & Procurement Trail Review
aliases:
  - Establishment and Procurement Trail Review
filing: report
toc_exempt: false
required_sections:
  - Purpose and basis
  - Establishment position
  - Statutory position
  - Procurement trail
  - Delivery and close-out snapshot
  - Gaps to close
  - Deliverables commissioned from this review
  - Basis and information gaps
---

# Report structure — Establishment & Procurement Trail Review

**Produced by the document-intelligence-agent.** The structure every establishment & procurement trail review follows.

This file is authoritative on **section order and section contents**. The agent config governs everything else — filenames, where to save, draft status, evidence rules. Where this file and the agent config disagree on structure, this file wins.

Output: `<job no.> - Establishment and Procurement Trail Review - RevA.docx`, filed to the `filing.report` folder (config.json).

The `.docx` is built per the `deliverable-build` skill — on the firm's letterhead where one is configured.

No fixed ceiling — the chase list governs the length. Do not pad the narrative.

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

Two questions: was the project established properly, and can the procurement decisions be traced through the record. It is a review of what the practice holds. It is **not an audit** and it makes no finding about any party's conduct.

---

## Title page

Project · Client · Review type · Data date · Governing procedures · Revision · Prepared by · Status · Commercial-in-Confidence.

## 1. Purpose and basis

- **Why this review was commissioned** — Who asked, when, and what question they need answered.
- **What was swept** — Folders swept and the date. Cite paths.
- **What this review is not** — Not an audit, not an assurance opinion, and not a finding about any party's conduct or competence.

## 2. Establishment position

- Table — the project start-up procedure / the project establishment procedure requirement · Position · Evidence or the folder swept`
- **The establishment position in one line** —  

## 3. Statutory position

- **Statutory payment position** — Whether the payment law is recorded (`project_facts.payment_law`), and whether claim, response and payment dates have been diarised for every live claim against the statutory periods recorded in `project_facts.payment_periods` — the {{payment_response}} deadline and the payment due date, each with the section of the payment law that fixes it, and the contract's own periods where shorter. Where the payment law bars a reason omitted from the {{payment_response}}, say so.
- **Building approvals and certification** — Permit, {{certifier}} appointment where the jurisdiction uses one, notice of commencement, mandatory inspections. Where a jurisdiction-specific chain applies, set it out link by link.
- **Insurances and securities** — Whether each required policy is held and current, and whether cover was in place before work commenced.

## 4. Procurement trail


**{{Tender}} issue**

- **What was issued, to whom, and when** — Package, document set and revision, {{tenderer}} list, issue date, closing date. Whether an addendum was issued and to all {{tenderer}}s equally.

**{{Tender}} returns**

- **What came back** — Each return, its date, and whether it was conforming.

**Evaluation and award**

- **How the decision was made and recorded** — The evaluation instrument, the criteria, the recommendation, and the written approval to award. Where the approval is not on file, say so — an award with no recorded approval is a control finding regardless of whether the choice was sound.

**Contract execution**

- **The executed instrument** — Parties as named on the face of the instrument, date, contract sum, and the drawing set the contract names. Where the named set is not the set held, that gap is a finding.

**{{Change_plural}} to the awarded contract**

- Table — `{{Change}} · Value (ex {{sales_tax}}) · Instruction file · Approval on file · Position`

## 5. Delivery and close-out snapshot

- **Where the project actually is** — Enough context for the reader to weigh the findings above. Not a status report.

## 6. Gaps to close

- Table — `# · Document outstanding · Who holds it · Position · Target`

## 7. Deliverables commissioned from this review

- **What follows from this review** — Each deliverable, the template it will be built from, who produces it, and when.

## 8. Basis and information gaps

- **What was read** — Each document, with revision, date and source.
- **What was swept and found empty** — Folder path and sweep date. That is a citation.
- **What could not be verified** —  
- **Assumptions made** —  
- **Status of this review** — DRAFT — for review. An empty folder proves that the practice does not hold a document, not that the document does not exist. This is a record review, not an audit, an assurance opinion or a due diligence report. Verification is the owner's at sign-off — the review-and-issue procedure, the sign-off record.

---

## Fixed elements

- Marked `DRAFT — for review`.
- Each establishment item is marked Held, Not held or Not applicable — and where it is not held, **whether it was due yet**. The phase test separates a finding from a non-finding.
- Follow the procurement trail in order and **stop at the first break**. Do not reconstruct a trail from inference and present the reconstruction as the record.
- In the chase list, distinguish **retrieval** (it exists, we do not hold it) from **procurement** (it does not exist yet). They take different words and different time.
- The practice's own gaps are named first and named plainly.
- An empty folder proves the practice does not hold a document, not that it does not exist. Cite the folder path and the sweep date — that is a citation.
