---
deliverable: Site Inspection Report
aliases:
  - Site Report
  - Site Observation Report
filing: site_report
toc_exempt: false
required_sections:
  - Visit particulars and scope
  - Summary of observations
  - Observations
  - Progress
  - Defects and non-conforming work
  - Safety
  - Photographs
  - Onward actions
  - Basis and limitations
---

# Report structure — Site Inspection Report

**site-report-agent.** The structure every site inspection report follows.

This file is authoritative on **section order and section contents**. The agent config governs
everything else — filenames, where to save, draft status, evidence rules. Where this file and the agent config disagree on structure, this file wins.

Output: `<job no.> - Site Inspection Report - YYYY-MM-DD - RevA.docx`, filed to the `filing.site_report` folder (config.json) — dated by the **inspection date, not the write-up date**.

The `.docx` is built per the `deliverable-build` skill — on the firm's letterhead where one is configured.


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

## The language rule — above everything else in this file

The observation-language rule binds every line. **Observation, never supervision.** Work "was observed to be" in
a condition a date; it never "is compliant" and it is never "approved".

| Never write | Write instead |
|---|---|
| Approved | Observed to be in accordance with drawing X Rev B at the date of inspection |
| The works are compliant | No non-conformances were observed in the areas inspected |
| Inspected and passed | Inspected on a sample basis; items listed below require attention |
| We supervised the pour | Attended during the pour and observed the following |
| Certified complete | Recommended for {{completion}} subject to the attached list |

**The sampling qualifier is mandatory and appears in section 2**, not buried at the end: the
inspection covered the areas listed, on a sample basis, at the date and time stated, and is not
comprehensive verification of the works.

No variation of the section order may drop it.

---

## 1. Title page

Project · client · **inspection date and time** · revision · prepared by (the firm) ·
**Commercial-in-Confidence** notice.

Where the write-up date differs from the inspection date, both appear here — contemporaneous
records are evidence, later reconstructions are opinion (the site observation rules).

## 2. Visit particulars and scope

A short table — genuine record data, and one of the few tables here:

date · time of arrival and departure · weather · attendees and their organisations · who escorted

Then, in prose: **the areas and elements inspected**, and what was not inspected. Followed by
the sampling qualifier in full.

Gaps are recorded as gaps. Weather is never inferred, attendees are never assumed.

## 3. Summary of observations

The whole answer in one short block of prose. What was observed, in general terms, and whether
any non-conformances were observed in the areas inspected. Written in observation language
throughout — this is the section most likely to be quoted back.

## 4. Observations

The observations schedule — a genuine register, and it stays a table:

| # | Location | Observation | Observed against | Photo |
|---|---|---|---|---|

"Observed against" carries the **drawing number with its revision** or the specification clause.
An observation with no document reference is close to worthless later.

Beneath the table, prose on anything that needs more than a row.

## 5. Progress

Where the visit supports a claim assessment: progress against the {{schedule}}, **with enough
detail to justify a percentage** (the site observation rules). A bare percentage with no basis cannot support
a claim.

State explicitly that valuation of the claim is the claims procedure work for `cost-commercial-agent` and
is not performed here. This report supplies the observation; it does not value the claim.

Omit this section entirely where the visit does not support a claim — do not pad it.

## 6. Defects and non-conforming work

Factual: what was observed, where, against which document at which revision. **No opinion
culpability**, no direction as to remedy. A register, and it stays a table.

Status against previously recorded defects where relevant.

## 7. Safety

Anything unsafe observed, that it was reported to site management, and **to whom** (the firm's procedure).

Record the report, never a direction. The practice does not direct the {{builder}}'s safety
systems (the safety policy, the site observation rules).

Omit where nothing was observed — an empty safety section is better than a padded one, but say
"nothing unsafe was observed in the areas inspected" in section 3 rather than silently dropping
it.

## 8. Photographs

The photograph register — number, location, orientation, date, what it shows. Wide shot for
context then detail. Photographs without location and date context are of limited use later.

## 9. Onward actions

Dot points, each **routed to its correct procedure** and each with an owner:

- a defect → through the contract
- a {{change}} → the claims procedure
- a hazard → the firm's procedure
- an information gap or RFI → document control
- an instruction → through the contract, to the {{builder}}, in writing (the head contract procedure)

The report routes; it does not action, and it does not instruct.

## 10. Basis and limitations

What was read with dates, what the source notes covered and did not, the interval between
inspection and write-up, assumptions made, and any language translated out of the source notes
per the site observation rules.

Closing statement: the report records observations made on a sample basis at a moment in time.
It is not a certification of compliance, completion or occupancy, and the practice performs no
construction work.
