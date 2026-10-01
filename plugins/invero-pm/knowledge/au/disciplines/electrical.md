---
title: Electrical services — what they issue and where it bites on a fitout
source: domain-knowledge
verified: 2026-08-21
confidence: high
licence: own-words
applies_to: [all]
tags: [electrical, lighting, discipline, review-checklist]
---

# Electrical

## What the consultant issues

- Power layout, lighting layout, and often a separate data and communications layout
- Switchboard schedule and single line diagram
- Light fitting schedule
- A Section J lighting calculation — often drawn as its own sheet
- Certificate of compliance for the electrical installation at completion

Sheet prefix is normally **E**. Governing standard: AS/NZS 3000 (Wiring Rules), with AS/NZS 3008 for
cable selection and AS/NZS 1680 for lighting adequacy.

## Where it bites on a retail fitout

**Section J is the compliance exposure.** The NCC controls lighting **power density** and **control**,
not adequacy. AS/NZS 1680 addresses adequacy. A design can satisfy one and fail the other, and the
two are usually done by different people.

**NCC 2025 changed lighting control materially.** J7D3–D4 replaced motion detectors with
demand-operated controls. **A retail lighting design carried over from a 2022-era store will not
comply as drawn.** On a rollout programme where the design is deliberately repeated store to store,
this is the change most likely to be missed — the drawing looks identical to the last one that was
approved, and that is exactly the problem.

**Supply capacity.** The lease grants an allowance in amps or kVA. Retail lighting, refrigeration and
a food offer eat it quickly. Confirm the available supply against the connected load before tender,
not after. Upgrading a tenancy supply from a landlord board is slow and often needs the landlord's
own electrical contractor.

**Voltage drop on long submains.** Where the landlord board is remote, the submain grows for voltage
drop rather than current. This is the most common reason an electrical tender price moves after award.

**Emergency and exit lighting.** Covered under Section E, not J. NCC 2025 updated exit sign
requirements (E4D8, Specification 25), and hybrid photoluminescent signs now reference SA TS 5367.
Exit and emergency is easy to under-draw because it is unglamorous, and it is always caught at
occupancy.

## Review checklist

- Is there a Section J lighting calculation on the set, and does its area match the architectural
  area? **Back-solve the printed total.** A quantity error inside a compliance calculation with a
  thin margin flips the result and is not caught downstream.
- Does the lighting control strategy meet J7D3–D4 as amended, or is it motion detection carried over?
- Is the connected load stated, and is it inside the lease supply allowance?
- Is the switchboard location shown, with access clearances that survive the joinery layout?
- Is emergency and exit lighting shown, with coverage — not just symbols?
- Are RCDs provided per AS/NZS 3000 for the circuit types present?
- Is data and communications shown, including the carrier's lead-in? Carrier lead times are long and
  are not the electrician's problem until they are.
- Do light fitting positions match the reflected ceiling plan exactly? A mismatch between the E and A
  sets on the RCP is a finding.

## Common coordination clashes

| Clash | How it shows up |
|---|---|
| Fitting versus diffuser | Electrical lighting layout and mechanical diffuser layout drawn on different ceiling grids |
| Fitting versus sprinkler | Both want the same ceiling tile |
| Switchboard versus joinery | Board shown on a wall the joinery set covers with shelving, losing the required clearance |
| Cable tray versus duct | High-level congestion, only visible in section |
| Section J area versus architectural area | Lighting calculation run on a superseded floor area |

## Interface with the tenancy

The tenant owns everything downstream of the tenancy isolator; the landlord owns the supply to it.
Metering arrangement, check metering, and after-hours HVAC charging all sit at this boundary and are
lease questions as much as engineering ones. Where the set says "by landlord", confirm the landlord
agrees — that phrase on a drawing is a claim, not an agreement.
