---
deliverable: Code Compliance Review
aliases: []
filing: code_compliance
toc_exempt: false
required_sections:
  - Basis
  - The statutory chain, link by link
  - Certificates and schedules
  - Post-approval drawing revisions
  - Execution state of the statutory instruments
  - Findings and defects
  - Recommendations
  - Confidence, provenance and information gaps
---

# Report structure — Code Compliance Review

**Produced by the code-compliance-agent.** The structure every code compliance review follows.

This file is authoritative on **section order and section contents**. The agent config governs everything else — filenames, where to save, draft status, evidence rules. Where this file and the agent config disagree on structure, this file wins.

Output: `<job no.> - Code Compliance Review - YYYY-MM-DD - RevA.docx`, filed to the `filing.code_compliance` folder (config.json).

The `.docx` is built per the `deliverable-build` skill — on the firm's letterhead where one is configured.

No fixed ceiling — the statutory chain governs the length.

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

Traces the statutory chain link by link and reports where a link is missing, contradicted or out of sequence. **The practice is not a certifier and this document certifies nothing** — that limit is stated in the document, not assumed.

---

## Title page

Project · Client · Jurisdiction · Approval pathway · Data date · Revision · Prepared by · Status · Commercial-in-Confidence.

## 1. Basis

- **Why this review was commissioned** —  
- **What was read** — Each statutory instrument, certificate, schedule and drawing set, with its revision and date.
- **The limit of this review** — The practice is not a {{certifier}} or fire safety engineer. This review reports what the documents on file show and where they disagree. It certifies nothing, and it is not legal advice.

## 2. The statutory chain, link by link

- Table — `# · Link · Position · Evidence held · Finding`
- **Where the chain breaks** — The links that do not hold, and what each break means for the client. Rank them — a missing signature and a missing {{occupancy}} are not the same order of problem.

## 3. Certificates and schedules

- **Certificates held** — Each one: what it certifies, who issued it, its date, and the standard and edition it cites.
- **Competing or contradictory certificates** — Where two documents certify the same measure differently, set out both and say which is later and which is narrower. Do not pick a winner — that is the certifier's role.
- **Standards cited without an edition** — List them. Each is a latent dispute.
- **Exemptions and alternative solutions relied on** — What the exemption actually permits, and — separately — what it has been reported as permitting. Those are often not the same, and the difference is the finding.

## 4. Post-approval drawing revisions

- Table — `Discipline · Endorsed revision and date · Latest revision held · Revisions issued after endorsement · Finding`
- **Whether the endorsed set is held at all** — Where the working record contains only later revisions, say so — the project may be building to a set nobody has compared against the approval.

## 5. Execution state of the statutory instruments

- **[Instrument name]** — Signed / unsigned / partially executed. Every signature block, its state, and any blank date field.
- **The precise position** — One paragraph a lawyer could rely on.

## 6. Findings and defects

- **Findings, in order of consequence**
- Numbered list.
- **What is not a defect** — Matters that look like defects but are not — an exemption correctly relied on, a standard superseded but validly applied at the time. Stating these protects the credibility of the ones that are.

## 7. Recommendations

- **Immediate**
- Numbered list.
- **Before occupation or handover**
- Numbered list.
- **For the client's ongoing obligations**
- Numbered list.

## 8. Confidence, provenance and information gaps

- **Confidence in each finding** — High / Medium / Low, with the reason. A finding drawn from a licensed-copy limit or a partial set is not a high-confidence finding.
- **What was read, and what was read only in part** —  
- **What could not be answered from the documents held** —  
- **Where a specialist opinion is required** — Named discipline, and the question to put to them.
- **Status of this review** — DRAFT — for review. This review certifies nothing, is not the opinion of a {{certifier}}, and is not legal advice. An empty folder proves that the practice does not hold a document, not that the document does not exist. Verification is the owner's at sign-off — the review-and-issue procedure, the sign-off record.

---

## Fixed elements

- Marked `DRAFT — for review`. Not a certification, not the opinion of a {{certifier}}, and not legal advice.
- **Every standard is cited with its year or edition.** A standard cited without its year is the single most common source of dispute on these reviews — where a document omits it, that omission is itself recorded as a finding.
- Run the whole chain. A missing link is recorded and the chain continues — later links often reveal why an earlier one is missing.
- Where two documents certify the same measure differently, set out both and say which is later and which is narrower. **Do not pick a winner** — that is the certifier's role.
- Separate what an exemption actually permits from what it has been *reported* as permitting. The difference is usually the finding.
- Record signature blocks precisely: what is signed, by whom, in what capacity, on what date. Where a field is blank, record it as blank — never infer it was completed elsewhere.
- State a confidence level per finding, with the reason. A finding drawn from a partial set or a licensed-copy limit is not high confidence.
- **What is not a defect** is a required section. It protects the credibility of the ones that are.
