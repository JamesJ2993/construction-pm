---
title: Contract forms — what is in use, and what each calls the parties
source: domain-knowledge
verified: 2026-10-01
confidence: provisional
licence: own-words
applies_to: [all]
tags: [contracts, general-conditions]
---

# Contract forms in Australian construction

**Overview only.** This file tells a project manager which form they are probably holding and what
it calls the parties, so the agents use the contract's own words. It does not say what any clause
means. Read the executed contract, including its special conditions, before relying on anything.

**Provisional.** Written from general knowledge. What would verify it: a person confirms each form's
current status against the Standards Australia store and the ABIC publisher, and the curator moves
this file to `verified` with the date. Clause-level detail is tracked as `gap-contract-forms`.

| Form | Typical use | Contract administrator |
|---|---|---|
| AS 4000-1997 | Construct only, the commonest commercial head contract | Superintendent |
| AS 2124-1992 | Older construct-only form, still met on government and legacy work | Superintendent |
| AS 4902-2000 | Design and construct | Superintendent |
| AS 11000-2023 | Newer general conditions intended to succeed AS 4000 and AS 2124 | Check the executed form |
| ABIC MW / SW | Architect-administered commercial and simple works | Architect |
| AS 4905 / AS 4906 | Minor works | Superintendent |

## What changes between them, for a PM

- **Who certifies.** Under AS forms the Superintendent assesses claims and grants time; under ABIC it
  is the architect. Use the contract's term in every register entry and report.
- **Notices and time bars.** Each form sets its own notice periods for variations and extensions of
  time, and special conditions routinely change them. Record the contract's periods in
  `project_facts` at setup; never carry them from another job.
- **Security of payment sits beside the contract.** The State's Act applies whatever the form says,
  and a contract cannot contract out of it — see `payment/`.
- **Amendments are the contract.** Most head contracts carry long schedules of special conditions.
  The printed form is the starting point, not the answer.
