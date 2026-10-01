# Australia — knowledge pack

What the agents know about building in Australia, and how much to trust it. The pack layout and the
frontmatter contract are described in [../README.md](../README.md).

**Every file carries provenance** — `source`, `verified`, `confidence`, `licence`. Check the
confidence before relying on a claim:

| Confidence | Means |
|---|---|
| `verified` | Checked against the cited source on the verified date |
| `high` | Standard practice, stated without a specific citation |
| `provisional` | Written from knowledge or a secondary source and **not yet checked** — flag before relying on it |
| `gap` | A known hole. The file records what is missing and why. |

Validate with `kb-lint.py lint --country au`. Open holes: `kb-gaps.py --country au`.
Currency: `kb-watch-sources.py --country au --check`. All three are in the knowledge-base skill.

## The licensing line

**NCC/BCA is CC BY 4.0** — clause text, tables and figures may be reproduced with attribution.
**AS/NZS standards are not** — Standards Australia licenses any extract, down to a single sentence or
figure. The `standards/` branch therefore holds pointers and paraphrase only, and the linter fails the
build if reproduced clause text appears there.

## Contents

### codes/ncc — the building code
| File | What |
|---|---|
| [ncc-2025-structure.md](codes/ncc/ncc-2025-structure.md) | Volumes, sections, clause numbering, compliance pathways |
| [adoption-and-editions.md](codes/ncc/adoption-and-editions.md) | Which edition governs a job, and why it is the approval-date edition |
| [retail-fitout-hotspots.md](codes/ncc/retail-fitout-hotspots.md) | **Start here for a drawing review.** The clauses that actually bite, by section |
| [state-variations.md](codes/ncc/state-variations.md) | **Check before citing anything.** Which Parts each of NSW, VIC, QLD, WA and SA varies. NSW varies all nine Parts of Section J. |

### permitting — planning and building approvals
| File | What |
|---|---|
| [README.md](permitting/README.md) | **Read first.** Which planning instrument governs each of the eight jurisdictions, and which of them are written. An unwritten jurisdiction has no answer here and never inherits the NSW one |
| [vic/approval-pathways.md](permitting/vic/approval-pathways.md) | Two instruments, two authorities — the planning permit under the PE Act 1987 and the building permit under the Building Act 1993. The Victorian separate approvals, each a programme predecessor |
| [nsw/approval-pathways.md](permitting/nsw/approval-pathways.md) | Exempt, CDC and DA; the separate approvals people forget; the DBP fitout carve-out |

### standards
| File | What |
|---|---|
| [README.md](standards/README.md) | Why this branch holds no clause text |
| `index.json` | Australian Standards a fitout engages: number, title, what it governs, NCC hook, the **PM trigger** that should send you to it, and the **NCC 2025 Schedule 2 mapping** |

### disciplines
| File | Status |
|---|---|
| [structural.md](disciplines/structural.md) | Written |
| [mechanical.md](disciplines/mechanical.md) | Written |
| [electrical.md](disciplines/electrical.md) | Written |
| [hydraulic.md](disciplines/hydraulic.md) | Written |
| [fire.md](disciplines/fire.md) | Written |
| vertical transport, facade, acoustic, civil, ESD | **Gaps** — recorded in `_meta/gaps.jsonl` with why each was deferred |

Each written file follows the same shape: what the consultant issues, where it bites on a fitout, a
review checklist, common coordination clashes, and the tenancy interface.

### safety — work health and safety
| File | What |
|---|---|
| [README.md](safety/README.md) | **Read first.** Victoria never adopted the model WHS laws |
| [nsw.md](safety/nsw.md) | **Approved codes became mandatory on 01.07.2026** under WHS Act s 26A. The 16 codes a fitout engages |
| [vic.md](safety/vic.md) | The OHS Act 2004 framework and compliance codes |
| [qld.md](safety/qld.md) | **Gap stub, not content.** The source is on manual watch; a person's first read is tracked as `gap-qld-whs-codes-first-read` |

### payment — security of payment
| File | What |
|---|---|
| [README.md](payment/README.md) | The shape common to every jurisdiction. No day counts, anywhere — the periods live in the Act and the contract, and each file names the section that fixes them |
| [vic.md](payment/vic.md) | The 15 April 2026 amendments. **Provisional** until read against the amended Act |
| [nsw.md](payment/nsw.md) | Which section fixes each NSW clock; s 11 runs different periods by respondent class; s 4 business days are narrower than Victoria's; s 20(2B) bars reasons not in the schedule. **Section pointers provisional** — `gap-sop-nsw-periods` |
| [qld.md](payment/qld.md) | Which section fixes each QLD clock; QLD retains reference dates (s 67); no schedule means the full claimed amount is owed (s 77); standard and complex payment claims run different adjudication periods. Verified 22 September 2026 against the Act |

### contracts
| File | What |
|---|---|
| [README.md](contracts/README.md) | The standard forms in use and what each calls the parties. Overview only — `gap-contract-forms` |

### practice
| File | What |
|---|---|
| [cost-planning.md](practice/cost-planning.md) | Preliminaries benchmark, the org-structure traps, and why a compressed programme *reduces* prelims |

### sector/retail-fitout
| File | What |
|---|---|
| [base-building-interface.md](sector/retail-fitout/base-building-interface.md) | Where landlord work stops and tenant work starts — the source of most fitout disputes |

## _meta

| File | What |
|---|---|
| `sources.json` | The sources the currency watcher polls, across all eight jurisdictions, plus what is deliberately not monitored and why |
| `gaps.jsonl` | Known holes, each with what it needs and why it was deferred |
| `changelog.jsonl` | Every change to the pack, with its reason |

## What this does not cover yet

Named honestly rather than left to be discovered:

- **What each state variation actually says** — high priority. Which Parts are varied is recorded;
  the clause-level text of each variation is not, and must not be inferred from the fact that a
  variation exists.
- Five of the ten disciplines.
- **Planning pathways** outside Victoria and New South Wales.
- **Security of payment and WHS** for WA, SA, TAS, NT and the ACT.
- Contract forms below overview level.
