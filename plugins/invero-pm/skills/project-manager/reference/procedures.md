# Procedures — the rules that govern each activity

Before any task, identify the rule that governs it and follow it. **Where a rule and convenience
conflict, the rule wins.** Where you must depart from one, that departure is a nonconformance: record it
in the project's `project-notes.md` and the activity log, and raise it with the owner.

## The firm's own management system

Firms with a management system (ISO 9001, an integrated management system, a QA manual) map its
documents in `config.json → procedures`:

```json
"procedures": {
  "claims": "QP-07 Payment Claim Assessment",
  "review_and_issue": "QP-03 Review and Issue",
  "safety": "SP-01 Safety Policy",
  ...
}
```

Where a key is set, **that procedure governs the activity and you cite it** in commissions, deliverables
and reports — it wins over this file and over the knowledge packs. Where it is `null`, the rule below
applies as written. A procedure and this skill genuinely in conflict: follow the procedure and flag the
conflict to the owner.

## The map

| Activity | Rule | `procedures` key |
|---|---|---|
| Any deliverable leaving for a client | Owner's review and sign-off is the only exit; drafts are marked; issue is a person's act | `review_and_issue` |
| Everything the agents produce | AI-assisted output is quality-controlled in the chain and **verified only at the owner's sign-off**; never presented as verified before it | `ai_verification` |
| A payment claim or {{change}} arrives | Statutory dates first, diarised the day it lands, from the recorded periods; assessment by `cost-commercial-agent`; the client serves | `claims` |
| A new project folder appears | Register on the owner's word; establish the project facts and the establishment documents (appointment, management plan, insurances); chase what is missing | `new_project` |
| Drawings, RFIs, revisions | Current issue vs. superseded discipline; a superseded document moves, never deletes; never overwrite a revision | `document_control` |
| Tendering and the ISSUED marker | The ISSUED marker is the owner's alone; issued scope changes only by addendum | `review_and_issue` |
| {{Schedule}} analysis | Comparative, against the accepted baseline, data date stated | `programme` |
| Reporting cycles | Cumulative; carry forward risks and actions; never drop an item silently | `reporting` |
| Head contract questions | Know the firm's role on the contract (`project_facts.role`) before commissioning advice | `legal` |
| Close-out | Checklist against the contract and the firm's close-out requirements; diarise the {{defects_period}} | `close_out` |
| Checking a design against the code | **Establish the governing code, edition and amendments from the project facts before citing a clause**; a clause cited against the wrong edition is a nonconformance, not a typo | `legal` |
| A change to a knowledge pack | `knowledge-curator-agent` is the only writer, to the overlay only, with source, date and reason recorded | — |
| An independent check before sign-off | Quality control by `independent-review-agent`; verification stays with the owner | `ai_verification` |
| File naming, revisions, records | Revision discipline; never overwrite a superseded revision; master copies live in their controlled location | `document_control` |
| Anything fails or goes wrong | Record it, propose the correction, raise it with the owner | `nonconformance` |
| Risks across the portfolio | Name them in reports with owner and treatment | `risk` |
| Mail and project data | Project-addressed mail only; nothing between clients | — |
| Site safety | Observe and report; never direct the contractor's means, methods or safety program | `safety` |
| A conflict of interest surfaces | Flag it to the owner; never adjudicate it yourself | — |
| The PM's own competence | Learn from the owner's corrections; record lessons; ask when a domain is new | `competency` |

## Standing cautions

- **Jurisdiction first.** Payment periods, building codes, safety regimes and permitting differ between
  countries and between regions inside a country. Every activity that touches them starts from the
  project facts and the knowledge pack for that region, never from another project's.
- **Watch dates.** Where a knowledge-pack file records a provision awaiting commencement or a watch date,
  and a run lands on or after it, say so in the report.
