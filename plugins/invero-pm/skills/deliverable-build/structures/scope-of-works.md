---
deliverable: {{Scope_of_works}}
aliases:
  - Scope of Works
  - Scope of Work
filing: scope_of_works
toc_exempt: false
required_sections:
  - Executive summary
  - General contracting requirements
  - Inclusions, exclusions and assumptions
  - Drawings
---

# Report structure — {{Scope_of_works}}

**scope-of-works-agent.** The structure of all five scope deliverables.

This file is authoritative on **section order and section contents**. The agent config governs
everything else — filenames, where to save, draft status, evidence rules. Where this file and the agent config disagree on structure, this file wins.

Issued to {{tenderer}}s → the project's procurement and {{tender}} folder
Internal only → the project's procurement and {{tender}} folder

**These are contract documents.** What a {{tenderer}} prices, what the {{Client}} pays for, and what
both parties argue about when they disagree.

Every `.docx` deliverable — the {{Scope_of_works}}, the Design Gap Register and every addendum — is
built per the `deliverable-build` skill, on the firm's letterhead where one is configured. The
`.xlsx` schedules are exempt — the letterhead is a Word construct.


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

# 1. {{Scope_of_works}} (.docx)

Built via `anthropic-skills:docx`. Seven sections, in this order.

### 1. Title page

Project · client · **package** · **contract form** · **the drawing set and revision the scope
derives from** · date · revision · prepared by (the firm) · commercial-in-confidence.

The drawing set and revision is not optional. A scope with no stated basis cannot be checked
against the design it came from.

### 2. Contents

Generated from the heading structure.

### 3. Executive summary

The package in short · the contract form · the documents the scope derives from, listed **with
revisions** · the {{tender}} close date where known.

If the design set is incomplete, say so **prominently here, at the front**. A scope derived from
a partial set is a partial scope regardless of how complete it reads.

### 4. General contracting requirements

Inserted **verbatim** from the firm's general contracting requirements — its own, where it keeps
them (`templates.dir`), otherwise `general-requirements.md` beside this file,
adapted once by the firm to its jurisdiction. Standing
across every {{tender}}: {{tender}} submission requirements · work health and safety · site requirements
· permits and authority requirements · quality, inspection and handover.

Numbered `G1.1, G2.4 …` — a sequence deliberately separate from the site-specific scope below.
Fill the bracketed project values (`[close date]`, `[site address]`, `[hours]`) from the project
documents, or list them in the gap register. **Do not rewrite this section** and do not derive it
from the project folder.

### 5. Site-specific {{scope_of_works}}

By element, in this order:

1. {{Preliminaries}}, site establishment, hoarding, temporary services, site accommodation
2. Demolition, strip-out, making safe, service isolation
3. Substructure, structure, structural steel
4. External fabric, roofing, waterproofing, glazing, facade
5. Internal partitions, linings, ceilings
6. Services — mechanical, electrical, hydraulic, fire, communications, controls
7. Finishes, floor coverings, painting, tiling
8. Joinery, fixtures, fittings, equipment
9. External works, landscaping, civil, drainage
10. Commissioning, testing, training, O&M documentation, as-builts, defects

**Each item is a one-liner. One obligation. No drawing or specification reference.**

```
4.11   The Contractor shall supply and install the level 2 bulkhead.
4.12   The Contractor shall set out and install the level 2 ceiling grid.
```

Never a table. If a sentence contains "and" joining two deliverables, it is two items. An item
running past about 25 words is probably two items.

**No per-item reference is deliberate.** A citation each line lets a {{tenderer}} price that line
without reviewing the set, then claim {{change}} on everything they did not open. The obligation
to review the design in full sits with the Contractor. Section 7 defines the full set being
priced against.

**Because there is no citation to resolve against, each item must be self-sufficient** — name
the element, the location and the standard. Never "as per drawings", never "as required".

Include the scope no drawing shows — protection of existing works · making good after other
trades · temporary works, propping, access, scaffold · builder's work in connection with services
· waste removal and cleaning · authority liaison, inspections, certificates · handover
documentation, warranties, spares. These are the most commonly omitted obligations.

Open this section with: *the Contractor is to satisfy itself as to the full content of the
documents listed at section 7, and no item of this scope is limited to any one drawing.*

### 6. Inclusions, exclusions and assumptions

Three sub-sections.

**Inclusions** — where scope might reasonably be read as excluded, say it is in.

**Exclusions** — what the contractor is not responsible for, **and who is**. An exclusion with no
named owner is a gap, not an exclusion.

**Assumptions** — access hours · site availability · existing conditions · base building capacity
· lead times · working calendar. Each one is a question the {{tenderer}} would otherwise have to ask,
or price a risk allowance against.

### 7. Drawings

The drawing register — number, revision, date, discipline, title. Plus the specification and any
other document forming part of the scope, each with its revision.

This section is what makes the scope enforceable without per-item references. It must be complete.

---

# 2. Scope Schedule (.xlsx)

Built via `anthropic-skills:xlsx`. **Mirrors the Word document item for item, same numbers**,
G-items first, then site-specific items.

`Item · Description · Included/Excluded · Drawing ref priced from · Qty · Rate · Amount · {{Tenderer}} comment`

The last five columns are left empty for the {{tenderer}}. **`Drawing ref priced from` is theirs to
state** — it puts the review obligation them and surfaces a {{tenderer}} who priced an item off
the wrong sheet.

**This is the file tender-analysis-agent compares returns against.** If the numbering drifts between the Word
document and this schedule, that comparison breaks silently. Never renumber existing items.

---

# 3. Design Gap Register (.docx)

Numbered. For each gap: **what is missing · what it affects · what it means if issued as-is · who
needs to resolve it · by when**, where the {{schedule}} drives a date.

Cover: items shown but not specified, or specified but not shown · undetailed junctions,
terminations and interfaces · missing or incomplete schedules · disciplines not yet issued ·
performance criteria not stated · conflicts between drawings, disciplines, or drawing and
specification · provisional or "to be confirmed" items still open · bracketed values in the
general contracting requirements that the project documents do not state.

**A gap is not scope.** Never close a gap by inventing a reasonable assumption and writing it as
an obligation.

---

# 4. Scope Traceability (.xlsx) — INTERNAL, NOT FOR ISSUE

`<job no.> - Scope Traceability - [Package].xlsx`

`Item · Description · Drawing ref (with revision) · Spec clause · Derived/Inferred`

Every item in the Word document appears here with the source it was derived from. This is how the
scope is checked back against the design, how a disputed item is defended later, and how a design
revision is traced to the items it affects.

**Saves to the project's procurement and {{tender}} folder, never to the {{tender}} documents folder.** Mark `INTERNAL — NOT FOR
ISSUE` in the filename banner and on the first sheet. It is never included in a {{tender}} pack.

---

# 5. Addendum (.docx) — during the {{tender}} period

`<job no.> - Scope Addendum No.1 - [Package].docx`

**One page. Around 400 words.** Six parts:

1. **Header** — project, package, addendum number, date, and the scope revision it attaches to
2. **What has changed** — each new document named with revision and date
3. **Scope items added or amended** — numbered, continuing the existing sequence
4. **Design gaps opened or closed** — cross-referenced to the gap register
5. **Effect on the {{tender}} period** — flag where an extension may be warranted; the decision is
   the {{Client}}'s
6. **Acknowledgement** — {{tenderer}}s to confirm receipt in their return

Numbering is sequential — Addendum No. 1, No. 2 — **never a revision letter**.

Reissue the Scope Schedule at RevB with any addendum that changes scope.

Three judgements:

- **If it will not fit one page, it is not an addendum** — the scope needs reissuing at RevB
- **A document that changes nothing still gets an addendum**, issued for information with scope
  expressly unaffected
- **A document that contradicts issued scope is not an addendum** — flag it and recommend a RevB
  reissue

---

## Fixed elements

- All marked `DRAFT — for review`
- **Every scope item is derived from a cited source**, recorded in the traceability file — not
  shown in the issued documents
- **Never scope from general construction practice.** The test is not "would a competent builder
  do this" — it is "do the documents require it"
- **No quantities.** Indicative quantities may be referenced and attributed to their source,
  never measured
- Active voice, present obligation: "The Contractor shall supply and install…"
- Consistent terminology — if it is a "bulkhead" at item 4.1 it is not a "drop ceiling" at 7.3
- No adjectives that cannot be tested. "High quality" and "as required" are unenforceable
