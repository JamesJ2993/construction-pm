---
title: Queensland WHS — codes of practice (content not yet written; source dark)
source: https://www.worksafe.qld.gov.au/laws-and-compliance/codes-of-practice
verified: 2026-09-10
confidence: gap
licence: own-words
applies_to: [QLD]
governing: safety
tags: [whs, worksafe, codes-of-practice, qld, dark-source]
---

# Queensland WHS — not yet written, and its source is currently dark

Queensland is a model-law jurisdiction (Work Health and Safety Act 2011 (Qld) — see the
jurisdiction table in `safety/README.md`), but the code-by-code detail equivalent to `safety/nsw.md` and
`safety/vic.md` has not been written. That gap is tracked as `gap-whs-qld` in `_meta/gaps.jsonl`,
open since 22 August 2026.

## The source that would fill it is dark

**`qld-whs-codes`** (WorkSafe Queensland codes of practice,
https://www.worksafe.qld.gov.au/laws-and-compliance/codes-of-practice) has been returning
**HTTP 403** to every fetch **since 25 August 2026**. That since-date is the fact recorded here.
The current duration and status are not tracked in this file — read them from the watcher:
`kb-watch-sources.py --check --country au` and `_meta/sources.json` (`qld-whs-codes`,
`last_checked`).

**A source that failed to fetch is not a source that has not changed.** Any new or revised
Queensland approved code issued since 25 August 2026 is invisible to this pack until a person reads the source. No
finding about Queensland WHS codes may be treated as current while this source stays dark — say so
explicitly rather than reporting silence as "no change".

The gap matters the day a Queensland job lands, and should not be rediscovered cold at that point.

## What would close this

- The fetch-treatment decision **was taken on 21 September 2026** : `qld-whs-codes` is now on **manual watch** in `_meta/sources.json`, the same class
  as `vic-planning`, `sa-whs-codes`, `tas-whs-codes` and `nt-whs-codes`, rather than the 403
  being worked around. `gap-qld-whs-codes-fetch-403` closed on that decision. Its `last_checked`
  stays at 25 August 2026 — the conversion stamps no currency the pack does not have, so
  a person's first read is still outstanding and is tracked as `gap-qld-whs-codes-first-read` in
  `_meta/gaps.jsonl`.
- Once the source is reachable (by fix or by manual read), the actual content file: governing
  statute confirmation, approved-code status, and the codes a fitout would engage — the same shape
  as `safety/nsw.md`.
