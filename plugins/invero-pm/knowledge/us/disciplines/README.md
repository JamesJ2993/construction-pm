---
title: Engineering disciplines in US drawing sets — names, sheet designators, and the review files
source: domain-knowledge (discipline designators follow the US National CAD Standard convention)
verified: 2026-10-01
confidence: provisional
licence: own-words
applies_to: [all]
tags: [disciplines, sheet-designators, review-checklist]
---

# Disciplines in US drawing sets

**Provisional.** What would verify it: a person checks the designators against the current US
National CAD Standard, and the curator moves the file to `verified`.

## Sheet designators

US sets usually follow the National CAD Standard's discipline designators: **G** general, **C** civil,
**L** landscape, **S** structural, **A** architectural, **I** interiors, **Q** equipment, **F** (or
**FP**) fire protection, **P** plumbing, **M** mechanical, **E** electrical, **T** telecommunications.
The project's `config.json → drawings.discipline_prefixes` holds the map the scanner uses; adjust it
to the set in hand.

## Names that differ from other packs

| This pack | Elsewhere |
|---|---|
| plumbing | hydraulic (Australia) |
| fire protection | fire services (Australia) |
| MEP | building services |

## Discipline review files

**No US discipline files are written yet** — tracked in `_meta/gaps.jsonl`. Until they are:

- `discipline-review-agent` may read the matching file in another pack (for example
  `../../au/disciplines/fire.md`) **for coordination logic only** — what the consultant issues,
  where trades clash, what a reviewer looks for.
- It must **never** cite another country's standard or code from that file. Every citation in a US
  review comes from the US adopted code and US referenced standards (`../standards/index.json`),
  and the review says plainly that the checklist was borrowed.
