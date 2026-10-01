---
title: Construction safety in the United States — OSHA, State Plans, and the multi-employer policy
source: Occupational Safety and Health Act of 1970; 29 CFR Part 1926 (https://www.ecfr.gov/current/title-29/subtitle-B/chapter-XVII/part-1926); OSHA State Plans (https://www.osha.gov/stateplans)
verified: 2026-10-01
confidence: provisional
licence: own-words
applies_to: [all]
governing: safety
tags: [safety, osha, 1926, state-plans, multi-employer]
---

# Construction safety in the United States

**Read this before observing or reporting anything on site.**

## Where the project manager sits

This pack is written for a **consultant project manager acting for the owner** who performs no
construction work and does not direct the contractor's means, methods or safety program. If the
firm using it holds a different role (recorded as `project_facts.role`), read the duty material
accordingly.

## The regime

- The **Occupational Safety and Health Act of 1970** created OSHA. Construction work is governed by
  the construction standards in **29 CFR Part 1926** — among them fall protection (Subpart M),
  scaffolds (Subpart L), excavations (Subpart P), electrical (Subpart K) and stairways and ladders
  (Subpart X) — together with the general duty clause.
- **State Plans.** About two dozen states and territories run their own OSHA-approved State Plans.
  Some cover private-sector construction; others cover only state and local government workers,
  leaving private work with federal OSHA. A State Plan must be at least as effective as federal
  OSHA and can be stricter. **Establish at setup which regime covers the project** and record it as
  `project_facts.safety_regime`.
- Most contracts also require a **site-specific safety plan** from the general contractor.

## The trap for an owner's PM: the multi-employer citation policy

On a multi-employer site OSHA can cite not only the employer whose workers were exposed, but also
the employer that **created** the hazard, the one responsible for **correcting** it, and the
**controlling** employer — the one with general supervisory authority over the site. An owner's
representative who starts directing safety measures risks being treated as exercising control.

So the observe-and-report stance in this plugin is not just style:

- **Observe and report** what was seen, where, when, and against which drawing.
- **Never direct** the contractor's means and methods, never approve a safety system, never word a
  finding as an instruction. Route anything urgent to the contractor through the contract's notice
  channel, and to the owner.

**Provisional.** Written from general knowledge of the federal system. What would verify it: a person
confirms the Part 1926 subpart references against the eCFR and the State Plan list against
osha.gov/stateplans, and the curator moves the file to `verified`.

## Built per state, on first use

When a project is registered in a state with no file at `safety/<state>.md`, the PM commissions the
knowledge curator (with the owner's OK) to record: whether a State Plan covers private construction
there, its name and rule set, and anything it adds to Part 1926 that a fitout would meet.
