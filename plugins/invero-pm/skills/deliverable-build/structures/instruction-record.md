---
deliverable: Instruction Record
aliases: []
filing: register
toc_exempt: false
required_sections:
  - Instructions recorded
  - Effect of the instructions
  - What was not instructed
  - Caveats
  - References
---

# Report structure — Instruction Record

**Produced by the project manager who received the instruction.** The structure every instruction record follows.

This file is authoritative on **section order and section contents**. The agent config governs everything else — filenames, where to save, draft status, evidence rules. Where this file and the agent config disagree on structure, this file wins.

Output: `<job no.> - Instruction Record - [Subject] - YYYY-MM-DD - RevA.docx`, filed to the `filing.register` folder (config.json).

The `.docx` is built per the `deliverable-build` skill — on the firm's letterhead where one is configured.

Two pages. If it runs longer, it is probably two instruction records.

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

This record exists so that an instruction cannot later be disputed. It is made **by** The practice **of** an instruction received — it does not itself instruct, approve or vary anything.

---

## Title page

Record · Project · Client · Date of instruction · Received from · Received by · Received how · Revision · Status · Commercial-in-Confidence.

## 1. Instructions recorded

- **Instruction 1** — The instruction, in the giver's own words where they were given in words. Then, separately, what the practice understands it to mean.
- **Instruction 2** —  
- **Instruction 3** —  

## 2. Effect of the instructions

- **On the {{schedule}}** —  
- **On cost** —  
- **On scope** —  
- **On documents already issued** — What is superseded, what must be reissued, and by whom.
- **Actions arising**
- Table — `# · Action · Owner · Due`

## 3. What was not instructed

- Bulleted list.

## 4. Caveats

- **Ambiguities in the instruction** — Recorded, not resolved. Say what clarification has been sought and from whom.
- **Where the practice has assumed** —  
- **Authority** — Whether the person giving the instruction holds the delegated authority to give it. Where that is unconfirmed, say so.

## 5. References

- **Documents referred to** — Each document, with revision and date.
- **Related records** — Prior instruction records, approvals, RFIs or {{change_plural}} this one connects to.
- **Status of this record** — DRAFT — for review. This record is made by the practice of an instruction received. It does not itself constitute an instruction, an approval or a {{change}}. Sign-off on the sign-off record — the review-and-issue procedure.

---

## Fixed elements

- Marked `DRAFT — for review`, pending the sign-off record sign-off.
- **Quote the words** where the instruction was given in words. Do not paraphrase into project language — the paraphrase is what will be argued about. Record the practice's understanding separately, and label it as an understanding.
- A verbal instruction is confirmed back in writing **the same day**.
- Ambiguity is recorded in the caveats, never resolved silently.
- State whether the person giving the instruction holds the delegated authority to give it, and say so where that is unconfirmed.
- **What was not instructed** is a required section. It closes the gap between what was said and what will later be remembered.
