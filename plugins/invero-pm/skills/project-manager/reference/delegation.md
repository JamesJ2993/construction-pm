# Delegation — who does what, the commission, the status envelope

Specialists are plugin subagents, named `invero-pm:<agent>` when you commission them. A `{{key}}` below
stands for the project's term.

## The map, from trigger to specialist

| Trigger | Specialist |
|---|---|
| **{{Payment_application}} or {{change}} received; a payment deadline running** | `cost-commercial-agent` — **statutory clock, top of the priority order. Commission it the day the claim lands** |
| {{Schedule}} file new or changed, delay signal, {{time_extension}} question | `programme-intelligence-agent` |
| {{Tender_return}}s arrive, comparison or recommendation needed | `tender-analysis-agent` |
| Design set ready for {{tender}}, scope drafting, documents arriving after scope issue (addendum) | `scope-of-works-agent` |
| Reporting cycle due, risk register stale, actions need chasing | `project-reporting-agent` |
| Monthly audit, takeover, "how is it going" | `project-health-check-agent` |
| A question the documents can answer; document, RFI or approvals registers | `document-intelligence-agent` |
| Site visit notes to write up; observed progress needed for a claim | `site-report-agent` |
| {{Completion}} approaching; handover or close-out completeness | `handover-closeout-agent` |
| A design set or scope needs checking against the adopted building code, its standards, the permitting pathway or safety regime | `code-compliance-agent` — the commission carries **the governing code, edition and amendments** and the document that fixes them; it stops without them, by design |
| One discipline's drawings need reviewing against its checklist | `discipline-review-agent` — **name the discipline**, and confirm its review file exists in the pack first (`kb_resolve.py`) |
| A finished deliverable is bound for sign-off and its acceptance criteria are written down | `independent-review-agent` — quality control, never verification |
| A pack needs a change — a new fact, a correction, a missing regional file or country | `knowledge-curator-agent` — the only pack writer; research only on the owner's OK |
| The owner asks for a currency scan | `industry-watch-agent` — never in routine triage; it makes network requests |
| Read-only legwork inside one project — inventory, sheet index, what changed since a date | `pm-project-analyst` |

Skills you run yourself, in this session, named in `config.json → skills`:

| Stage | Skill |
|---|---|
| Register review against a new set | `invero-pm:tender-documentation-review` (`skills.register_review`; first register `skills.register_initial`) |
| Register wording | `invero-pm:concise-register-entries` |
| Any workbook write | `invero-pm:safe-xlsx-update` |
| Scope citations against the signed-off register | `invero-pm:highlight-sow-clarifications` — only after register sign-off |
| Documentation checklist | the firm's own checklist skill if `skills.doc_checklist` names one; otherwise mark the project's checklist ✓ / ✗ / N-A against the current drawings yourself, with a note on every ✗ and every N-A |
| Building any `.docx` deliverable, and the gates | `invero-pm:deliverable-build` |
| Knowledge packs — reading, linting, gaps | `invero-pm:knowledge-base` |

## The commission

Give every specialist a precise commission. A commission missing a fact the specialist needs does not
degrade — it stops.

```
Commission <WRK-yyyymmdd-n>  ·  project <id>  ·  root <absolute path>
What changed:      <the diff or mail item that triggered this, with paths>
Deliverable:       <what to produce> — structure <structures/<file>.md or the firm's template>
File to:           <absolute path of the filing folder>  (config.json → filing.<key>)
Project facts:     country/region, contract form, role, and the facts this specialist needs
                   (building code + edition; payment law + periods; safety regime …)
Terms:             config.json → terminology (kb_resolve.py --terms)
Acceptance:        <the criteria the independent review will check against>
Lessons bearing:   LSN-…, LSN-…  (or none bearing)
Producing agent:   <for independent-review-agent only: the agent whose work is reviewed>
Budget:            <a soft time budget proportionate to the work>
Open your hand-back with the status envelope.
```

Scope every commission to **one project folder** and say so. A specialist working one project has no
business reading another — commercial-in-confidence applies between projects inside the same run.

## The status envelope

Every specialist opens its hand-back with this block, exactly as YAML front matter:

```yaml
---
status: complete | partial | blocked
agent: <specialist name>
commission: <the commission id>
deliverable: <absolute path, or none>
gates: provenance=pass letterhead=pass toc=pass   # n/a for read-only work; .xlsx carries provenance only
lessons_applied: [LSN-021, LSN-047]              # or none bearing
blocked_on: <one line — only when status is blocked>
---
```

`complete` — the deliverable is filed and the gates pass. `partial` — real work came back but something
named is outstanding (an unverified statutory date is always `partial`). `blocked` — the commission could
not proceed; the missing fact is in `blocked_on`. There is a fourth status that you write and a specialist
never does: **`no-return`**.

**No commission runs forever.** When one errors, returns nothing, or runs well past its budget:

1. Retry **once**, same commission id, marked as a retry.
2. If the retry also fails, record it `no-return` with what is known, put the outstanding work in a
   waiting-on item, and **carry on**. The rest of the portfolio still runs.
3. Name it in the report. A `no-return` is a reportable fact, never a silent omission — and never grounds
   for the cycle's state write to be skipped.

**Never infer a run is dead from its age alone** while it may still be running in another session.

## The whole portfolio at once

- **Prioritise before you parallelise.** Statutory → time-critical against a {{schedule}} or {{tender}}
  date → the owner's change requests → routine triage → housekeeping.
- **Independent projects run in parallel** — launch their specialists together (several Agent calls in one
  message), long analyses in the background, and collect results before writing shared state.
- **Commission from the diff, not the folder.** The scan and the mail sweep already say what changed; the
  specialist reads deeply so you do not have to.
- **Within one project, one writer at a time.** Sequence commissions that write into the same project;
  parallelise across projects. Read-only specialists — `code-compliance-agent`,
  `discipline-review-agent`, `independent-review-agent`, `pm-project-analyst`, and
  `document-intelligence-agent` answering a question — are not writers.
- **State is written once, at the end — and never held hostage.** After the cycle's commissions return or
  are closed out as `no-return`: one read-modify-write of state.json, one entry per project.

## Model tier, with a hard floor

The specialists carry a default tier: statutory, client-facing and judgement-heavy work runs on `opus`
(cost-commercial, programme-intelligence, tender-analysis, code-compliance, scope-of-works,
project-health-check, independent-review); structured, gate-protected work on `sonnet`
(document-intelligence, site-report, project-reporting, handover-closeout, discipline-review,
knowledge-curator, industry-watch). Override per commission where the stakes demand it — up for a
tender-critical discipline review, down for a pure-mechanical register build. **Never below the floor:**
claims and {{change_plural}}, {{time_extension}} assessments, anything client-facing, anything bound for
sign-off runs at its default tier or higher.

## Load — what gives way, and in what order

A full portfolio is the normal condition. When the work exceeds the cycle — judged on live statutory
clocks, commissions in flight, deadlines inside `deadline_horizon_bdays` — what gives way, in order:

1. Housekeeping — deferred to the daily review.
2. Report prose — compresses to dot points; a quiet project gets one line.
3. Routine-triage depth — a quiet project gets its scan diff checked and nothing else this cycle.

What never gives way: statutory work; one writer per project; commercial-in-confidence scoping; the
owner's sign-off as the only exit. **Name every deferral in the report.** The same item deferred for
`repeat_deferral_cycles` consecutive cycles is reported as a capacity signal, not deferred again quietly.
