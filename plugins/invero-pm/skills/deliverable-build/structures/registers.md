---
deliverable: Register
aliases:
  - Document Register
  - RFI Status Schedule
  - Approvals Tracker
  - Contract Obligations Summary
  - Design Gap Register
filing: register
toc_exempt: false
required_sections: []
---

# Report structure — Register

**document-intelligence-agent.**


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

## Read this first — when this file does NOT apply

**document-intelligence-agent's default output is a short cited answer in conversation, and it saves nothing.**
This file does not change that.

A question gets an answer, not a document:

```
Yes — the penetration is retained.
Source: A-2102 Rev C, 12 May 2026, Level 2 Slab Plan, grid E/4.
Note: deleted on Rev B; reinstated by RFI-047 response 8 May 2026.
```

The answer first, then the citation, then any caveat. No title page, no executive summary, no
preamble. If the answer is one line plus a drawing reference, that is the whole output.

**This file applies only when a register or schedule is explicitly requested.** Do not produce
one because a question touched a subject a register covers.

---

This file is authoritative on **section order and section contents** for the four register modes.
The agent config governs everything else. Where this file and the agent config disagree on
structure, this file wins.

Output → the `filing.register` folder (config.json)


Registers built as `.xlsx` are **updated in place each time rather than versioned**, since they
carry their own status columns.

---

## Common to all four

Title page and the standard report structure, then the register itself.

Title page: project · client · register type · data date · revision · prepared by (the practice
Projects) · commercial-in-confidence.

Every row cites document name, revision, date, and clause or drawing reference. **A row without a
revision is not a row.**

---

## 1. Document register

`<job no.> - Document Register - YYYY-MM-DD.md`

| Column | Notes |
|---|---|
| Document | Name as issued |
| Type | Drawing / specification / contract / minutes / correspondence |
| Number | Drawing or document number |
| Revision | **Mandatory** |
| Date | Issue date |
| Status | Current / superseded / preliminary / not for construction |
| Gaps | What is missing or expected but not held |

Build this first when working a project for the first time. It makes every later answer faster
and exposes gaps immediately.

Flag anything marked preliminary or "not for construction" that appears to be in use as
construction issue.

## 2. RFI status schedule

`<job no.> - RFI Register - YYYY-MM-DD.md`

| Column | Notes |
|---|---|
| RFI no. | |
| Question | |
| Raised by / date | |
| **Days outstanding** | On every open item |
| **Ball-holder** | Contractor / consultant / {{Client}} / authority |
| **What it blocks** | Procurement, fabrication, site work |
| Response / date | |
| Status | Open / closed |
| Scope impact | Whether the response added work |

- **Do not treat an RFI as closed because a response exists.** Closed means the question is
  answered and the answer is on a drawing or instruction
- A response that adds work is **a {{change}} in waiting** — flag it as such

## 3. Approvals tracker

`<job no.> - Approvals Tracker - YYYY-MM-DD.md`

| Column | Notes |
|---|---|
| Approval | {{planning_approval}}, {{building_permit}}, trade permits, service authority, {{occupancy}}, client approvals |
| Status | |
| Date given | |
| **Conditions attached** | |
| Expiry / lapse date | |
| Outstanding against **need-by date** | Driven by the {{schedule}} |

**Conditions of consent are frequently the forgotten scope.** Extract them and check they are
reflected in the design and the contract scope.

## 4. Contract obligations summary

`<job no.> - Contract Obligations Summary - RevA.md`

| Column | Notes |
|---|---|
| Obligation | Quoted, not paraphrased |
| Clause | |
| Who owes it | |
| To whom | |
| By when | |
| Consequence if missed | |
| **Time bar / notice requirement** | Flag prominently |

Identify the contract form and whether special conditions amend the standard clause. **A heavily
amended standard-form clause does not behave like the printed one.**

Time bars and notice requirements are the clauses that lose money quietly — they get their own
column, not a footnote.

---

## Fixed elements

- Anything issued externally is marked `DRAFT — for review`
- Quote source text for anything contractual or contested — short, exact, in quotes
- Distinguish what a document **states** from what has been **inferred**
- Never fabricate a clause number, drawing reference or revision. If it cannot be located, say so
  and say where you looked
- Where two documents conflict, present both with sources and flag it — never resolve silently
- Where confidence is low — poor scan, ambiguous wording, incomplete set — say so
