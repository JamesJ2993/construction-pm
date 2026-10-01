---
deliverable: Meeting Position Note
aliases: []
filing: report
toc_exempt: false
required_sections:
  - Purpose
  - What is outstanding, who holds it, and by when
  - What this note is not
---

# Report structure — Meeting Position Note

**Produced by a person, not an agent.** The structure every meeting position note follows.

This file is authoritative on **section order and section contents**. The agent config governs everything else — filenames, where to save, draft status, evidence rules. Where this file and the agent config disagree on structure, this file wins.

Output: `<job no.> - Meeting Position Note - YYYY-MM-DD - RevA.docx`, filed to the `filing.report` folder (config.json).

The `.docx` is built per the `deliverable-build` skill — on the firm's letterhead where one is configured.

Two to four pages. It is held in one hand in one meeting.

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

Written for one person to hold in one meeting. It answers the questions that will actually be asked, in the order they will be asked, and it gives the honest answer rather than the comfortable one. It is **not minutes and not a report**.

---

## Title page

Project · Prepared for · Data date · Reads with · Revision · Prepared by · Status · Commercial-in-Confidence.

## 1. Purpose

- **The meeting** — Who is in the room, and what they will want to know.
- **What this note does** — The two or three questions it answers.

## 2. [Questione — write it as the question that will be asked]

- **[The answer, in one line.]** — Then the evidence that supports it, cited.
- **One qualification, stated rather than buried** — Where the answer rests on something reported rather than evidenced, say so here — not in a footnote.

## 3. [Question two]

- **[The answer, in one line.]** —  

## 4. What is outstanding, who holds it, and by when

- Table — `# · Outstanding · Who holds it · Position · Target`
- **The practice's own gaps** — Named first and named plainly. A list that puts everyone else's failures first reads as blame-shifting.

## 5. What this note is not

- **Scope of this note** — Not minutes, not a report, and not a determination. It records the practice's position at the data date for use in one meeting.
- **Status** — DRAFT — for review. Verification is the owner's at sign-off — the review-and-issue procedure, AI output verification.

---

## Fixed elements

- Marked `DRAFT — for review`. Issued by a person, not by an agent.
- **Each section is headed with the question that will be asked**, and opens with the answer in one line before any evidence.
- Where the answer rests on something reported rather than evidenced, the qualification is stated in the body — not buried in a footnote.
- Distinguish what is contractually due (a demand) from what is not a listed deliverable (a request). The distinction changes the words used in the room.
- The practice's own gaps are named first.
- Name the report it reads with, and which governs where the two differ.
