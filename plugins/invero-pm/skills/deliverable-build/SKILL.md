---
name: deliverable-build
description: Build a client-ready .docx deliverable for a PM project — the report structure, the project's terms, the markdown draft with its contents marker, the md-to-docx → insert-toc → apply-letterhead chain, and the provenance, letterhead and contents gates. Use whenever a markdown draft becomes a .docx deliverable, whenever a deliverable fails a presentation check, or whenever an agent needs the build chain. The single source for build mechanics; report structures stay authoritative on section order and contents.
---

# Building a deliverable

Every client-facing `.docx` is built the same way. This skill is the single source for the mechanics;
the matching report structure is authoritative on **section order and contents**, and the producing
agent's own file on filing, naming and evidence rules.

Scripts are in `${CLAUDE_SKILL_DIR}/scripts/`. Structures are in `${CLAUDE_SKILL_DIR}/structures/`. Every
script takes the project's `config.json` (in its PM state folder) with `--config`, which is where the
letterhead, the template library and the terminology come from.

## 1. Start from the right structure — never a blank page

- **The firm's controlled template**, where `config.json → templates.dir` holds one for this deliverable.
  Read it for the sections, markers and guidance it carries. Never write into the template itself.
- **Otherwise the plugin's structure**, `structures/<deliverable>.md`:

| Deliverable | Structure | Typical producer |
|---|---|---|
| Project health check | `project-health-check.md` | project-health-check-agent |
| Monthly / weekly report | `project-report.md` | project-reporting-agent |
| Cost report | `cost-report.md` | project-reporting-agent, cost stream |
| {{Tender_evaluation}} | `tender-evaluation.md` | tender-analysis-agent |
| {{Scope_of_works}}, gap register, addenda | `scope-of-works.md` (+ `general-requirements.md`) | scope-of-works-agent |
| Site inspection report | `site-inspection-report.md` | site-report-agent |
| Claim and {{change}} assessment, {{payment_certificate}} | `claim-and-change-assessment.md` | cost-commercial-agent |
| {{Schedule}} analysis / review / baseline brief | `schedule-analysis.md` · `schedule-review.md` · `baseline-reissue-brief.md` | programme-intelligence-agent |
| Close-out review | `close-out-review.md` | handover-closeout-agent |
| Code compliance review | `code-compliance-review.md` | the PM, packaging code-compliance-agent's findings |
| Registers | `registers.md` | document-intelligence-agent |
| Instruction record · meeting position note · establishment review · first pass | `instruction-record.md` · `meeting-position-note.md` · `establishment-review.md` · `first-pass.md` | commissioned per project |

`python scripts/check-provenance.py --list --config <config.json>` prints every structure with its
required sections **rendered in the project's terms**.

**Write in the project's terms.** A `{{key}}` in a structure stands for the project's term
(`kb_resolve.py --terms` in the project-manager skill prints them) — "pay application" and "change
order" on a US job, "progress claim" and "variation" on an Australian one. The deliverable never
contains a placeholder. Dates in the project's `date_format`; money in `report.currency`.

## 2. Draft in markdown, with the contents marker

Markdown is the **build input, not the record** — draft it in the PM's state folder (`filing.drafts`) and
let the `.docx` be the deliverable of record. Put a `[[TOC]]` marker on its own line **immediately after
the title page content**: the contents page sits between the title page and the first section, is a
house element rather than a numbered section, and never counts against a page budget. Headings for the
structure's required sections are `##` headings, worded as the structure words them (in the project's
terms) — that is what the provenance gate looks for.

## 3. The build chain — in this order, skipping no step

```
python scripts/md-to-docx.py "<draft.md>" "<deliverable.docx>" --title "..." --config "<config.json>" --skip-h1 --status "DRAFT — for review"
python scripts/insert-toc.py "<deliverable.docx>"
python scripts/apply-letterhead.py "<deliverable.docx>" --config "<config.json>"
```

`md-to-docx.py` renders the markdown on the firm's letterhead when `report.letterhead` is set, so the
document inherits the house typography, headers, footers and margins from the start; without one it
builds on a plain base. `insert-toc.py` swaps the `[[TOC]]` marker for a live Word contents field (Word
offers to update it on first open). `apply-letterhead.py` confirms the letterhead — `already-letterheaded`
on a letterhead-based build, `skipped` when none is configured — and splices the letterhead in only for a
document built some other way.

## 4. The gates — prove it before handing back

```
python scripts/check-provenance.py --check "<deliverable>" --config "<config.json>" --structure "<deliverable name>"
python scripts/apply-letterhead.py --check "<deliverable.docx>" --config "<config.json>"
python scripts/insert-toc.py --check "<deliverable.docx>"
```

All three must pass (the letterhead gate passes as `n/a` when the firm has none). **The PM runs them
before anything goes to sign-off** — that is the gate.

**Provenance is the gate that catches what the other two cannot.** The letterhead and contents checks
test *appearance*, and appearance is exactly what a document invented from nothing gets perfectly right.
`check-provenance.py` asks whether the artefact descends from its controlled template or structure and
whether that structure survived being filled: for a `.docx`, the required section headings; for an
`.xlsx` against a firm template, its sheets and section labels. It fails on two grounds — no template or
structure matches, or the structure was lost — and a configured template library that is missing is an
**error, never a silent fallback**. It runs on `.xlsx` as well as `.docx`.

An inbound third-party document (the contractor's claim as served) is not built from the firm's
structures: record why with `--exempt "<reason>"`. An exemption that is not written down is
indistinguishable from an oversight.

## 5. Exemptions and marking

- **`.xlsx` deliverables are exempt** from the contents field and the letterhead — both are Word
  constructs. Provenance still applies. Workbook writes go through `invero-pm:safe-xlsx-update`.
- **Structures marked `toc_exempt: true`** (the First Pass letter) carry no contents page: no `[[TOC]]`
  marker, `insert-toc.py` not run, its `--check` not required.
- **The {{payment_certificate}} is one page**: no contents page, and `insert-toc.py --check` returns
  check-fail on it **by design**. The letterhead check still binds.
- Mark every output with `report.draft_marking` (default `DRAFT — for review`). Agents draft; a person
  issues.
- Where the commission says the project is a TEST project, carry the TEST marking prominently on the
  title page and in headers.
