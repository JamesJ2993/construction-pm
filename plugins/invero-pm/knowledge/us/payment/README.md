---
title: Getting paid in US construction — pay applications, prompt payment, liens and bonds
source: Miller Act, 40 U.S.C. 3131-3134; Prompt Payment Act, 31 U.S.C. 3901-3907; AIA Document A201-2017 Article 9 (https://www.aiacontracts.com)
verified: 2026-10-01
confidence: provisional
licence: own-words
applies_to: [all]
governing: claims
tags: [commercial, payment, prompt-payment, liens, retainage, miller-act]
---

# Getting paid in US construction

**There is no US equivalent of a security of payment Act** covering all construction. The payment
position on a project is set by four things together, and a project manager has to know which of
them apply before assessing anything:

1. **The contract** — the pay application cycle, what the owner's representative certifies, retainage,
   and the notice and claims procedures. On AIA documents, A201 Article 9 runs the payment cycle.
2. **The state's prompt payment law** — most states set deadlines for an owner to pay a contractor
   and for a contractor to pay its subcontractors, with interest on late payment. Private and public
   work are often treated differently.
3. **The state's mechanics' lien law** — unpaid contractors, subcontractors and suppliers can usually
   lien private property. Many states require **preliminary notices** early in the job and impose
   strict deadlines for recording a lien after completion. Lien rights are the trades' real leverage
   and the owner's real exposure.
4. **On public work, bonds instead of liens.** Public property cannot be liened. The federal
   **Miller Act** requires payment and performance bonds on federal construction contracts above a
   threshold, and most states have "Little Miller Acts" for state and local work. The federal
   **Prompt Payment Act** sets federal agencies' payment deadlines.

**Provisional.** The federal statutes are named from the US Code; the state picture is a general
description. What would verify it: a person confirms the federal citations at uscode.house.gov and
the curator moves the file to `verified`. **State rules are never taken from this file.**

## The pay application cycle (AIA practice)

- The contractor submits a **pay application** — AIA G702 (the application and certificate) with
  G703 (the continuation sheet, line by line against the schedule of values).
- The **Architect** (or the owner's representative named in the contract) reviews it against the
  work in place and **certifies** an amount, or withholds certification in whole or part **with
  written reasons**.
- The owner pays the certified amount within the contract's period, less **retainage**.
- Lien waivers are exchanged with each payment — conditional for the current payment, unconditional
  for the last one received. Several states prescribe the waiver forms by statute.

## Why a project manager must care

- **Deadlines are statutory as well as contractual.** A late or unexplained withholding can carry
  interest under the state prompt payment act, and some states restrict what can be withheld and
  require it to be itemised in writing within a set time.
- **Reasons belong in writing, at the time.** Like the Australian position, a withholding with no
  contemporaneous written reason is the hardest to defend later.
- **Liens follow unpaid trades.** Paying the general contractor does not stop a subcontractor from
  liening the property if the GC does not pay them. Lien waivers and joint checks exist because of
  this.
- **Retainage is capped in some states**, often differently for public and private work.

## Built per state, on first use

This pack carries **no state payment periods** — the same no-day-counts rule as every pack. When a
project is registered in a state with no file at `payment/<state>.md`, the PM commissions the
knowledge curator (with the owner's OK) to write one. It must name the statute and section for:

- the owner's payment deadline after a proper pay application, and the contractor's deadline to pay
  subcontractors;
- the interest rate on late payment;
- what a withholding notice must contain and when it must be given;
- preliminary notice requirements, who must give them and when;
- the deadline to record a lien after completion or cessation, and to enforce it;
- the retainage cap, private and public;
- whether pay-if-paid and pay-when-paid clauses are enforceable;
- the Little Miller Act threshold for public work.

Each with its source and `confidence: provisional` until a person confirms it against the statute.
The periods that apply to a given project are then recorded in `project_facts` at setup, alongside
the contract's own periods; where the contract is shorter, it governs.
