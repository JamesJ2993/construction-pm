---
title: Building codes in the United States — model codes, adoption, and which edition governs
source: International Code Council, code adoption information (https://www.iccsafe.org/about/overview/international-code-adoptions/); NFPA, NEC adoption information (https://www.nfpa.org)
verified: 2026-10-01
confidence: provisional
licence: own-words
applies_to: [all]
tags: [codes, ibc, irc, iecc, nfpa, adoption, editions]
---

# Building codes in the United States

**There is no national building code.** The International Code Council (ICC) publishes model codes
— the I-Codes — and each state, and often each county or city, decides whether to adopt them,
which edition, and with what amendments. A model code has no force anywhere until a jurisdiction
adopts it. The question is never "what does the IBC say" but "what does the code **this authority
having jurisdiction (AHJ) adopted** say".

**Provisional.** Written from general knowledge of the US system, not read against each source for
this pack. What would verify it: a person confirms the statements below against the ICC and NFPA
adoption pages and the curator moves the file to `verified` with the date. The state-by-state
adoption for a given project is **never** taken from this file — it is built per state (below).

## The model codes a commercial fitout meets

| Code | Covers |
|---|---|
| International Building Code (IBC) | Commercial and multi-family buildings: occupancy, construction type, egress, fire protection, accessibility (by reference to ICC A117.1), structural |
| International Existing Building Code (IEBC) | Alterations, repairs, additions and change of occupancy in existing buildings — **the code most tenant fitouts actually run under** |
| International Fire Code (IFC) | Fire prevention, fire protection systems, hazardous materials; enforced by the fire marshal |
| International Mechanical / Plumbing / Fuel Gas Codes (IMC, IPC, IFGC) | MEP systems — some states use the Uniform codes (UMC, UPC) instead |
| International Energy Conservation Code (IECC) | Energy; many jurisdictions allow ASHRAE 90.1 as the commercial compliance path |
| International Residential Code (IRC) | One- and two-family dwellings and townhouses — not commercial work |
| NFPA 70, National Electrical Code (NEC) | Electrical — adopted separately from the I-Codes, often on a different edition |
| NFPA 101, Life Safety Code | Used instead of or alongside the IBC in some jurisdictions and by federal healthcare regulators |

The ICC publishes on a three-year cycle (2018, 2021, 2024 …) and the NEC likewise (2020, 2023,
2026 …). **Adoption lags publication** — commonly by one or two cycles — so a project in one state
can be under IBC 2018 while the next state is on 2024.

## Which edition governs a project

1. **Find the AHJ.** Usually the city or county building department; for some state-owned or
   state-regulated buildings, a state agency.
2. **Find what that AHJ had adopted when the permit application was submitted**, including state
   amendments and local amendments. Some states adopt statewide and pre-empt local codes; others set
   a minimum and let localities go further; a few leave it almost entirely to localities.
3. **Record it** as `project_facts.building_code` — the edition, the state code name where it has
   one, and the local amendments — before any clause is cited. A clause cited against the wrong
   edition reads as authoritative and is wrong.

State codes often carry their own name. Several states publish a state building code that is the
IBC with state amendments under the state's own title; the IBC section numbers usually survive but
the content can differ. Cite the adopted code by its adopted name.

## Accessibility is two regimes, not one

- **The building code** — the IBC's accessibility chapter and ICC A117.1, enforced by the building
  official at plan review and inspection.
- **The Americans with Disabilities Act (ADA)** — the 2010 ADA Standards for Accessible Design, a
  federal civil-rights law enforced by the Department of Justice and through private lawsuits, **not
  by the building official**. A permit and a certificate of occupancy do not establish ADA
  compliance. Some states add their own accessibility code on top.

## Built per state, on first use

This pack carries no state adoption detail. When a project is registered in a state with no file
at `codes/<state>.md`, the PM commissions the knowledge curator (with the owner's OK) to write one:
the adopting body, the I-Code and NEC editions in force, the state code's name, whether localities
may amend, and where the adoption is published — each with its source and `confidence:
provisional` until a person confirms it.
