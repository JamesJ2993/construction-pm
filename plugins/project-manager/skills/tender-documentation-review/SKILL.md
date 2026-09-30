---
name: tender-documentation-review
description: Review a multi-discipline tender drawing set (architectural plus structural, mechanical, electrical, hydraulic, fire) against the previous clarifications register — adjudicating every carried item, hunting cross-discipline coordination conflicts, and producing the next register revision with a sign-off summary. Use when a tender or construction drawing issue arrives and needs reviewing, when asked to "review the tender drawings", "do the tender documentation review", "close off the register against the new set", or to produce the next register revision. Must be completed and signed off before any Scope of Works is written from the same drawings.
compatibility: Python 3.10+ with PyMuPDF, openpyxl and Pillow.
---

# Tender Documentation Review

A tender issue is the first set where the disciplines can be checked against each other. Earlier
preliminary reviews can only ask "is the architecture complete?" — this one asks **"do the
disciplines agree?"**, which is where the money and the buildability risk sit.

## The gate

**The Scope of Works is not written until this review is signed off.** Writing scope from an
unreviewed set is how unresolved coordination gets priced as though it were resolved. Produce the
register revision and the sign-off summary, hand both over, and stop.

## Before starting

Confirm the drawing set is **complete**. Services packages routinely lag the architectural issue,
and a half-uploaded set produces a register full of false "not issued" findings. List what arrived,
by discipline, and ask before reviewing.

Load `project-manager:concise-register-entries` for the writing style and
`project-manager:safe-xlsx-update` before any workbook write.

## Step 1 — Index and map

Extract sheet number, title, discipline, revision and date from every title block. Use **PyMuPDF**,
not page images — it is far cheaper, and title-block text comes out exact.

```python
import fitz
doc = fitz.open(pdf)
for i, page in enumerate(doc, 1):
    r = page.rect
    strip = fitz.Rect(r.x1 * 0.72, r.y0, r.x1, r.y1)   # title block, right-hand strip
    txt = page.get_text('text', clip=strip)
```

Then:

- **Reconcile both ways** against the issued drawing register sheet: sheets listed but missing, and
  sheets present but unlisted.
- **Build the renumbering map from the previous issue.** Sheets get renumbered wholesale between
  revisions (on one job A3601→A6601, A3002→A6004, A3701→A6701). Build this map *before* adjudicating
  anything — without it, carried items read falsely as "sheet deleted" and get wrongly closed.
- Record the revision letter and date on every sheet. Mixed revisions within one "issue" are common
  and are themselves a register item.

## Step 2 — Zone matrix

Map which sheets, from which disciplines, cover the same physical area. This is the artefact that
makes coordination findable, and it drives the allocation in Step 3.

## Step 3 — Review, allocated by zone, not by discipline

Allocating one agent per discipline recreates the silo that causes the conflicts. Allocate by
**physical zone or system**, each agent holding every discipline for its area:

| Zone | Typical overlay |
|---|---|
| Ceiling void | architectural RCP + existing services RCP vs mechanical ductwork, electrical lighting, fire sprinklers, structural beams |
| Shopfront / facade | shopfront plans, sections, elevations vs structural portal, electrical to signage and screens |
| Back of house | BOH plan and elevations vs hydraulic (sinks, HWU, waste), mechanical exhaust, electrical and comms |
| Feature zones | zone detail sheets vs structural (raised or sunken floors, loading), hydraulic (planting), electrical |
| Floor / structure | finishes and level plans vs structural slab, penetrations, set-downs |
| Fixtures | joinery and fixture sheets vs electrical power/data, mechanical supply |

Give each agent a shared brief containing: the sheet index, the renumbering map, its zone
allocation, the carried items routed to it, and a strict JSON output contract.

**Mandatory agent instruction — write early.** Each agent must write a complete output JSON as soon
as it has covered its inherited items, then refine. Agents that hold findings only in context lose
everything to a session or credit limit. This has happened twice; it is not hypothetical.

Also run a light **adequacy pass per new discipline package** — completeness, schedules,
specifications, dead callouts — but do not turn it into a full fresh review of every sheet unless
asked. Coordination is the higher-value pass.

### Auditing a quantity schedule against its own plan

Where a sheet carries a schedule with lengths or counts, reconcile it to the plan rather than
reading it. Extract the tags with coordinates and pair each to its dimension; do not eyeball a
render. Three checks find nearly everything:

- **Back-solve the printed total.** If the stated total does not equal the sum of the rows,
  substitute each row in turn until it reconciles — that identifies the wrong cell exactly. A total
  that reconciles only with the row above's value is a copied cell, not a rounding difference.
- **Closing dimension chains prove which figure is right.** Where a schedule and a plan disagree,
  test the plan's chain: a perimeter whose legs sum to zero in both axes settles it without asking.
- **Renumbered sub-tables orphan plan tags.** When a row is deleted between issues, every tag below
  it shifts. Check *each* plan tag against the new numbering — the failure is always the one tag
  that was missed, so a tag appearing more times than its QTY and another appearing zero times are
  the same defect seen from both ends.

State the corrected quantity and load, not just that the schedule is wrong — that is what gets
priced. Check whether the erroneous figures also feed a compliance calculation (J7, NCC Section J);
a schedule error inside a calculation with a thin margin is a higher-priority finding than the
schedule error itself.

## What is and is not a coordination finding

A real finding is one a contractor could not build or price through:

- **Physical clash or inadequate clearance** — always state the measured figure. "Ceiling at 3000
  AFFL against duct soffit at AFFL +3.019 = 19mm" is a finding; "possible clash" is noise.
- **Two disciplines showing different geometry** for the same element — differing levels, sizes or
  positions.
- **Responsibility gap** — an element every discipline defers to another, or to a base-building or
  lessor scope that is not documented.
- **Provision without a source** — a fixture needing power or water with nothing serving it, or a
  service terminating at nothing.

**A markup removed is not a conflict resolved.** If a previous revision carried clash annotations
and the new one does not, overlay the geometry yourself and confirm the services actually moved.
Deleted markups with unchanged geometry is the single most common false close.

## Step 4 — Adjudicate the carried items

Every item in the previous register gets a verdict against the new set: **Closed / Partially
Addressed / Open**. Route each to whichever zone agent now holds the answering sheets.

- A renumbered or redrawn sheet is not, on its own, a resolution.
- Where a previously closed item is contradicted by the new set, **reopen it** and say so
  explicitly in the heading — a reversal buried in body text gets missed.
- Items that were open only because a discipline had not been issued are the ones most likely to
  close now. They are also the ones most likely to be *falsely* closed: check the new drawing
  actually answers the question, rather than merely existing.

## Step 5 — Build the register revision

- Carry every row forward unchanged. **Never renumber, never reuse a ref.** New items continue from
  the highest existing number.
- Keep the previous column structure. Add the finding at the foot of `Description of Issue` under a
  heading generated from the Status cell — never typed:

  ```python
  desc = f"{issue}\n\nTENDER REVIEW {date} — {entry['status'].upper()}\n{findings}"
  ```
- Leave `Response` completely blank. It belongs to the design team.
- Every row carries a snapshot cropped from the relevant sheet. Resolve images through an explicit
  `row -> source file` map, never a folder keyed by ref number.

## Step 6 — Sign-off summary

The gate artefact. Hand over with the register:

- Sheets issued vs sheets reviewed, by discipline, and any reconciliation gaps
- Carried items adjudicated, with status movement (how many closed, partially addressed, reopened)
- Coordination conflicts found, by zone, with the measured clearances
- Open items that will need **assumption / PC sum / exclusion** treatment in the Scope of Works,
  listed by reference so the pricing basis is traceable

State plainly what could not be reviewed and why. Then stop and wait for approval.

## Bundled tooling

`scripts/dwgtool.py` renders and crops sheets from a page-image set — `overview` for a whole sheet,
`tiles` for readable text, `zoom` by fractional coordinates, `snap` to cut a register snapshot. Set
`SRC` and `NAME` at the top for the job. Small annotations are legible at 300dpi when zoomed;
always zoom before concluding anything about a dimension or note.

## Guardrails

- Never write into the tender issue folder. It is read-only input.
- Never overwrite an existing register — always a new revision letter.
- Confirm the set is complete before the first write.
- Do not write the Scope of Works from this run.
