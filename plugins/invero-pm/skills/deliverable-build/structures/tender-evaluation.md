---
deliverable: {{Tender_evaluation}}
aliases:
  - Tender Evaluation
  - Bid Analysis
  - Bid Evaluation
filing: tender_evaluation
toc_exempt: false
required_sections:
  - Executive summary
  - {{Tender}} comparison matrix
  - Recommendation memo to the {{Client}}
  - Clarification / RFI schedule
---

# Report structure — {{Tender_evaluation}}

**tender-analysis-agent.** The structure every {{tender_evaluation}} follows.

This file is authoritative on **section order and section contents**. The agent config governs
everything else — filenames, where to save, draft status, evidence rules. Where this file and the agent config disagree on structure, this file wins.

Output: `<job no.> - {{Tender_evaluation}} - [Package] - RevA.docx`, filed to the `filing.tender_evaluation`
folder (config.json).

Every `.docx` produced under this structure is built per the `deliverable-build` skill — on the
firm's letterhead where one is configured.


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

## 1. Title page

Project name · client · **{{tender}} package** · report date · prepared by (the firm) ·
revision · **Commercial-in-Confidence** notice.

Name the package as the RFT names it, so the evaluation files alongside the documents it assesses.

## 2. Executive summary — one page, decision-first

- **Open with the recommendation and the normalised sums**
- Then the three or four findings that would change the decision if they turned out differently
- No preamble, no methodology narrative

A reader who stops after this page should be able to act.

If any submission is **materially incomplete**, that goes at the top of this page. An incomplete
return is a finding, not an obstacle to work around.

## 3. {{Tender}} comparison matrix

{{Tenderer}}s as columns, criteria as rows. Cover:

`Submitted sum · Normalised sum · Scope classification by major element · Key exclusions · {{Schedule}} · Commercial risk rating`

Keep cells short — detail sits in the sections behind it. If the matrix is wide, **split it by
theme rather than shrinking it to illegibility**.

Scope classification uses the four values, never anything else:

| Value | Meaning |
|---|---|
| Included | Priced within the lump sum, stated clearly |
| Excluded | Expressly excluded or qualified out |
| Provisional sum | Carried as PS/PC, not a firm price |
| **Not addressed** | Silent — no mention either way |

**"Not addressed" is a risk, never an inclusion.** Every one flows to section 5.

### Pricing build-up

Show the adjustments, not just the adjusted totals. The {{Client}} must be able to follow every
step:

```
Submitted sum (ex {{sales_tax}})          $X
  less PS/PC sums               ($X)
  less contractor contingency   ($X)
  plus [scope excluded]         $X
= Normalised comparison sum     $X
```

State that a normalised sum is an analytical construct for comparison, **not a price the
{{tenderer}} has offered**.

## 4. Recommendation memo to the {{Client}}

Addressed to the {{Client}}. State:

- The recommended {{tenderer}} and the reasoning
- The material risks that come with that recommendation
- What conditions should attach to award

Where the decision turns on the {{Client}}'s own risk appetite rather than on analysis, say so and
set out the trade-off instead of manufacturing a recommendation.

## 5. Clarification / RFI schedule

Grouped per {{tenderer}}. Each question traced back to the specific gap, exclusion or ambiguity that
generated it. **Numbered for issue.**

Keep each question closed enough to produce a usable answer — avoid open invitations to re-tender.

---

## Fixed elements

- Marked `DRAFT — for review`
- Exclusions quoted **verbatim**, then translated: *quoted text* → *what it means for the
  {{Client}}* → *exposure or "unquantified"*
- Every finding cites document name and page, clause or line item
- {{sales_tax}} treated explicitly and never mixed
- Commercial risk ranked against the **{{Client}}'s** exposure, not the contractor's

## What this report does not contain

- **No budget comparison.** Inputs are confined to the {{tender}} documentation and returns; the
  approved budget sits outside them. Say so rather than guessing.
- **No programme-versus-baseline test.** Assess the {{schedule}} *in the return*; whether it fits
  the project baseline is agent 01's question.
