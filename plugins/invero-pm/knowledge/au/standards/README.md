---
title: How Australian Standards are handled here
source: https://www.standards.org.au/access-standards/license-standards
verified: 2026-08-21
confidence: verified
licence: own-words
applies_to: [all]
tags: [standards, licensing, copyright]
---

# Australian Standards — the rule

**No clause text. Ever. Not a sentence, not a figure, not a table.**

Standards Australia licenses reproduction of any extract from an Australian Standard. An extract
includes a sentence, a paragraph, a diagram, a figure or a clause. That is narrower than most people
assume, and it is why this branch of the knowledge base stores pointers and paraphrase rather than
content.

Contrast with the NCC, which is CC BY 4.0 and *can* be reproduced with attribution. The two are
handled differently on purpose, and `kb-lint.py lint` (the knowledge-base skill) enforces the difference:

- files under `standards/` must be licensed `own-words`
- any long quoted run in this branch is flagged as suspected reproduced clause text

## What is stored instead

`index.json` holds, per standard:

| Field | What it is |
|---|---|
| `number`, `title`, `year` | Bibliographic facts. Not protected expression. |
| `discipline` | Which consultant owns it |
| `governs` | What the standard is about, in one line |
| `ncc_hook` | Which NCC clause calls it up — the reason it applies at all |
| `requires_in_own_words` | What it requires, described rather than quoted |
| `pm_trigger` | What makes it relevant on a job — the thing that should make a PM go and look |
| `ncc_2025_schedule_2` | What NCC 2025 Schedule 2 actually calls up for that standard — see Currency below |

`pm_trigger` is the field that earns its keep. Knowing AS 1428.1 exists is worthless; knowing that a
change to a shopfront threshold or a queuing rail sends you to it is the actual working knowledge.

## Getting the exact wording

The paraphrase is for triage — deciding whether a standard applies and whether something needs
checking. **It is not a substitute for the clause when a compliance position is being taken.**

Where the firm holds licensed copies of standards, and exact wording is needed, the answer is to open the licensed copy, not to reconstruct it from here.

If a paraphrase in the index turns out to be wrong or dated, correct the index and record what
settled it. Do not paste the clause in.

## Currency

Standards get revised, and the NCC references a *specific edition* of each standard in Schedule 2.
A newer edition existing does not mean it applies — the edition called up by the governing NCC
edition does. Check Schedule 2 before assuming the latest version governs.

The index now carries that check written down. Each standard has an `ncc_2025_schedule_2` key
recording whether NCC 2025 Schedule 2 lists it, every edition it lists with the clauses that call
that edition up, and what was searched for where it is not listed. The key has its own provenance
block at the top of the file — `ncc_schedule_2_provenance` — because it was verified against the
NCC PDFs on a different day, and under a different licence, from the rest of the file. The block's
CC BY attribution covers the NCC-derived clause identifiers and nothing else; every paraphrase in
the file remains own-words.

Four cautions follow from what that key holds.

**`year` is not the referenced edition.** The `year` field records the standard's own edition as the
index has always carried it. Where Schedule 2 calls up a different one, the entry carries an
`edition_note` saying so. The note is the current position; `year` has deliberately not been
overwritten, because correcting it is a separate decision recorded as its own gap.

**One standard can have more than one referenced edition at once.** Schedule 2 lists some standards
several times, each edition against a different set of clauses. AS 1428.1 is listed three times — a
current edition for the general access provisions, an earlier one retained for certain Part I2
clauses, and a Supplement. Reading only the newest is the error this key exists to prevent; which
edition governs turns on the clause being applied.

**A state table can call up an edition the national table does not, or a standard it does not list
at all.** The jurisdiction entries sit under their own keys and are never merged into the national
one. Two examples verified in this branch: AS/NZS 3000 is not in the national table anywhere, and
reaches the Code only through the NSW table; AS 1851 is likewise absent nationally but is referenced
in the Victorian table against a Volume Three clause, which makes it a Code reference in Victoria
and not only a maintenance standard. Establish the jurisdiction before answering from the national
column.

**Absent means absent from the tables that were read.** Jurisdictions whose tables have not been
opened read `not-read`, not `not-listed`. The two are different answers and the file keeps them
apart.
