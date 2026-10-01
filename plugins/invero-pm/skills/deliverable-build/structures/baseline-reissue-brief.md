---
deliverable: {{Schedule}} Baseline Acceptance & Reissue Brief
aliases:
  - Baseline Acceptance and Reissue Brief
  - Baseline Acceptance & Reissue Brief
filing: programme_review
toc_exempt: false
required_sections:
  - Purpose and status
  - Accepted baseline and approved calendar
  - Governing key dates
  - Information gaps, assumptions and caveats
  - References
---

# Report structure — {{Schedule}} Baseline Acceptance & Reissue Brief

**Produced by the programme-intelligence-agent.** The structure every {{schedule}} baseline acceptance & reissue brief follows.

This file is authoritative on **section order and section contents**. The agent config governs everything else — filenames, where to save, draft status, evidence rules. Where this file and the agent config disagree on structure, this file wins.

Output: `<job no.> - Baseline Acceptance and Reissue Brief - YYYY-MM-DD - RevA.docx`, filed to the `filing.programme_review` folder (config.json).

The `.docx` is built per the `deliverable-build` skill — on the firm's letterhead where one is configured.

No fixed ceiling — section 4 governs the length, and it must be complete.

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

This brief does two things at once: it records which {{schedule}} has been accepted as the baseline, and it tells the programmer exactly what to change before reissuing.

---

## Title page

Document · Project · Accepted baseline · Data date of accepted baseline · Superseded candidate · Report date · Revision · Prepared by · Status · Commercial-in-Confidence.

## 1. Purpose and status

- **What this brief does** —  
- **What has been accepted, and by whom** — The instrument of acceptance — an instruction record, an approval, a meeting decision — with its date.
- **What this brief does not do** — It does not approve an {{time_extension}}, it does not accept any delay event, and acceptance of a baseline is not acceptance of the durations or logic within it.

## 2. Defects carried from the {{schedule}} analysis

- Table — `# · Defect raised · Status at this brief · Carried to section 4?`

## 3. Accepted baseline and approved calendar

- **The accepted baseline** — Filename, revision, data date, and the scenario it represents.
- **The approved working calendar** — Working week, shift pattern, public holidays, RDOs, shutdown periods. State it explicitly — a calendar that is implied by the bar positions is not a declared calendar.
- **What is superseded** — The candidate no longer live, and the date it was superseded. It is retained, never deleted.

## 4. Governing key dates

- Table — `Milestone · Date · Source`

## 5. What the programmer must do in the reissue


**Declare the approved calendar in the {{schedule}} file**

- **Instruction** —  

**Convert constrained activities to logic-driven scheduling**

- **Instruction** — Name each activity and the predecessor it should take.
- Table — `Activity ID · Activity · Current constraint · Required logic`

**Issue the native file or a verifiable tabulation**

- **Instruction** — The native file, or a tabulation carrying activity ID, duration, early and late dates, predecessors, successors and total float. A PDF of a bar chart is not a verifiable {{schedule}}.

**Rebadge the file as the accepted baseline**

- **Instruction** — Filename, revision and the note that the superseded scenario is withdrawn.

## 6. What the practice will verify on receipt

- Numbered list.
- **What will happen if the reissue does not meet these criteria** —  

## 7. Information gaps, assumptions and caveats

- **What was read** — Each document, with revision, date and source.
- **What could not be verified** —  
- **Assumptions made** —  
- **Status of this brief** — DRAFT — for review. Acceptance of a baseline is not acceptance of the durations, logic or resourcing within it, and it grants no {{time_extension}}. Verification is the owner's at sign-off — the review-and-issue procedure, the sign-off record.

## 8. References

- Bulleted list.

---

## Fixed elements

- Marked `DRAFT — for review`. {{Schedule}} positions are issued by a person.
- **Every instruction in section 4 is specific enough to execute without a follow-up call** — name the field, the activity, the value.
- **One scenario only** in the governing key dates. Two live date sets is the condition this brief exists to end.
- The acceptance criteria in section 5 are stated **before the reissue arrives**. Criteria invented after it lands are not a fair test and will not survive challenge.
- Every defect previously raised is carried forward with its current status, including the ones now closed.
- Acceptance of a baseline is **not** acceptance of the durations, logic or resourcing within it, and it grants no {{time_extension}}. Say so.
- The superseded scenario is retained, never deleted.
