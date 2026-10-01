---
deliverable: Close-out Review
aliases:
  - Close-out Report
filing: close_out
toc_exempt: false
required_sections:
  - Executive summary
  - {{Completion}}
  - Statutory and handover deliverables
  - {{Defects_period}}
  - Final account
  - Findings and recommendations
  - Close-out determination
  - Basis, confidence and information gaps
---

# Report structure — Close-out Review

**Produced by the handover-closeout-agent.** The structure every close-out review follows.

This file is authoritative on **section order and section contents**. The agent config governs everything else — filenames, where to save, draft status, evidence rules. Where this file and the config disagree on structure, this file wins.

Output: `<job no.> - Close-out Review - YYYY-MM-DD - RevA.docx`, filed to the `filing.close_out` folder (config.json).

The `.docx` is built per the `deliverable-build` skill — on the firm's letterhead where one is configured.

No fixed page ceiling — the close-out record governs the length. A thin project produces a short review; do not pad, and do not compress the completeness matrices to fit an imagined budget.

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

Reviews a project's close-out position per the close-out procedure, against the close-out checklist Project Close-out Checklist — whether the file can close, and what stands in the way. It reports two positions separately and never lets one answer for the other: **the delivery position** (handed over, trading, defects being worked) and **the record position** (whether the contractual steps completed and the instruments are on file). "Completed" is a delivery status, not a compliance status — a project can be handed over and trading while the record cannot show the statutory chain closed.

**This review is not the certificate of {{completion}}, not a final certificate, not an audit and not legal advice.** It reports what the file shows. Certifying is a distinct act performed by whoever the contract names, within the contract's time and form.

---

## Title page

Project · Client · Data date · {{Completion}} date as evidenced (or "not certified") · {{Defects_period}} end · Revision · Prepared by · Status · Commercial-in-Confidence.

## 1. Executive summary

- **The close-out position in one paragraph** — can the file close; if not, the shortest true statement of why not.
- **The delivery position, stated separately** — handed over on what date, trading or occupied since when, defects position in one line.
- **The items that decide it** — the three to five findings that actually gate close-out, each with its owner.

## 2. {{Completion}}

- **The contractual test** — {{completion}} is the contract's definition, not a judgement about whether the building looks finished. Name the clause and quote the operative words.
- **The certificate** — issued or not, in the required form or not, within the contractual period or not. Where {{completion}} was not achieved, whether that was said, with reasons, within time.
- **The defects list at {{completion}}** — whether it distinguished items preventing {{completion}} from items for the {{defects_period}}.
- **The dates this fixes** — the evidenced {{completion}} date, and every clock that runs from it: the {{defects_period}}, security reduction dates, and the limitation period of the project's jurisdiction (name the event the jurisdiction runs it from — some run it from the occupancy approval, some from completion; the knowledge pack or the firm's lawyers settle which). Every date names the instrument that fixes it.

## 3. Statutory and handover deliverables

- Table — `Item · Held / Not held / Partial · Evidence (document, revision, date) · Finding` — one row per handover deliverable among the close-out checklist's contractual items: occupancy permit or certificate of final inspection · essential safety measures documentation · as-built drawings · O&M manuals and warranties · commissioning records and training · keys, access and asset registers. The checklist's other four contractual items — {{completion}} certification, defects tracking, security dates and the final account — are reported at sections 2, 4 and 5, where each belongs.
- **A ticked checklist row is not the instrument on file.** Cite the document itself — its title, author, date — never a handover pack's claim that it exists. Where the folder is empty, say so with the path and sweep date.

## 4. {{Defects_period}}

- **The register position** — defects tracked to closure with date raised, date rectified and evidence, or the gap stated.
- **The inspection regime** — the final inspection is the only one the close-out procedure mandates; every other walk-through is justified on the project's facts. The final inspection date must leave room for the full inspect → direct → rectify → re-inspect cycle **inside** the period, not merely for the inspection itself.
- **Security** — reduction and release dates diarised from the instrument; the minimum five business days' notice before any recourse to security; the contractor's statutory route to recover security after the period — the claims procedure.

## 5. Final account

- Table where the reconciliation warrants it — contract sum · approved {{change_plural}} · provisional sums · prime cost items · adjustments · liquidated damages · final position. The basis of every line recorded.
- **The final certificate** — issued or not, in the contractual form, within time.
- **Categories that cannot be priced** — where a line turns on an instrument not held (a rate, a date, an annexure), carry both computations and name the instrument that decides between them. Obtaining it is a precondition the certificate, stated as such — never a silent pick.

## 6. The PM's own file

- Table — `Item · Done / Outstanding · Reference` — one row per the close-out checklist file item bar one, nine of its ten: executed contract, annexures and amendments · instructions numbered · determinations with their reasoning and evidence · issued deliverables with review sign-offs · final design set with superseded material retained and marked · site records and photographs · AI working records in the PM's state folder · client material returned or destroyed per the engagement · the PM's own record retained (client confidentiality, records retention). The tenth, the records-retention date, is homed in the anchor-dates bullet below and at section 8.
- **The two anchor dates, resolved separately** — the **records-retention** period runs from the **{{occupancy}}** or final inspection (the length is the firm's records policy, often aligned to the jurisdiction's limitation period); the {{defects_period}} runs from **{{completion}}**. Two different anchors one form. Resolve each from its instrument; never compute one from the other.

## 7. Findings and recommendations

- **Findings, in order of consequence** — numbered list. Each names the document or absence behind it.
- **Absent instruments still exercisable** — for every instrument the record does not hold, state whether it can still be obtained or exercised and by when. If it can, it belongs below as a recommendation with a date against it, not only here as a gap.
- **Where the contract argues with itself** — two mechanisms that do not reconcile are administered both as written and reported as a finding for the {{Client}} to resolve. Never harmonise silently.
- **Recommendations** — grouped **immediate · before {{defects_period}} expiry · at final account**. Each tied to a finding, naming a party and what it resolves. No generic advice.

## 8. Close-out determination

- **Can the file close** — yes, or no with the close-out checklist items outstanding, each with an owner and the event that closes it.
- **Records retention** — the records-retention date set under the firm's records policy, from its correct anchor.
- **Learning** — client feedback sought and recorded in the firm's procedure; lessons-learned review held; anything that should change a procedure raised for the nonconformance register.

## 9. Basis, confidence and information gaps

- **What was read**, with revisions and dates.
- **What was missing**, split into *absent and due* (findings) and *absent because early or not applicable* (not findings).
- **Confidence in each finding** — High / Medium / Low, with the reason.
- **Assumptions made.**
- **Status of this review** — DRAFT — for review. Not a certification of {{completion}}, not a final certificate, not an audit, and not legal advice. An empty folder proves that the practice does not hold a document, not that the document does not exist. Verification is the owner's at sign-off — the review-and-issue procedure, the sign-off record.

---

## Fixed elements

- Marked `DRAFT — for review`. This review certifies nothing: it is not the certificate of {{completion}}, not a final certificate, not an audit and not legal advice.
- **Delivery status and record status are reported separately, always.** "Handed over and trading" answers neither whether the contractual steps completed nor whether the statutory record is closed.
- **Every date that starts a clock names the instrument that fixes it** — and the two anchors are never conflated: records retention runs from the {{occupancy}} or final inspection, the {{defects_period}} from {{completion}}.
- A checklist or handover pack row is a claim; the cited instrument on file is the evidence. Cite the instrument.
- An absent instrument still exercisable carries a "by when" and lands in the recommendations, because "still exercisable" is a status with an expiry.
- Where two contractual mechanisms do not reconcile, administer both and report the contradiction — choosing between them is construing the contract, which is the {{Client}}'s call or their lawyer's.
- Cite the source throughout: clause numbers, document titles, revisions, dates. An assertion without a reference is not usable in a construction dispute.
- The practice performs no construction work and directs no contractor's means, methods or safety systems — nothing here may be worded otherwise (the safety policy, the site observation rules).
