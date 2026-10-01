---
name: concise-register-entries
description: House style for writing and tightening entries in a construction clarifications register, RFI log or defects list — the Description of Issue, Clarification Question and status wording. Use when drafting register items, when adjudicating a register against a new drawing revision, or whenever the user says entries are too long, too wordy, hard to read, or asks to make them concise, punchy or bullet points. Also use before writing a register from scratch, so items come out short first time instead of needing a trimming pass.
compatibility: Any register produced as .xlsx (openpyxl) or reviewed in Excel. Pairs with the clarifications-register and drawing review workflows.
---

# Concise Register Entries

Construction registers get read by people pricing work under time pressure. An entry that takes
three readings to parse gets skimmed, and a skimmed clarification does not get answered. Write
short the first time — trimming afterwards costs several passes and still reads like trimmed prose.

## The rule that matters most

**Keep every piece of evidence. Cut every word that is not evidence.**

Evidence is what the designer has to answer against and what a contractor would price from:

- Dimensions, levels, RLs, gradients, clearances — `175mm over 2310`, `AFFL +3.019`, `19–29mm`
- Sheet numbers, detail numbers, view references — `A6003 Section 2`, `1/A6402`
- Codes and tags — `SF07`, `W03`, `F9-A5`, `SG01`, `PC9`
- Quoted drawing notes, verbatim and in quotation marks

Everything else is compressible: connective prose, restating the issue inside the finding,
explaining why something matters when the fact already shows it, and hedging.

## Structure

### Items raised fresh

One to five bullets. No heading, no preamble. Lead with what is on the drawing, then what is
wrong with it, then the consequence only if it is not obvious.

```
• A6005 King Street Shopfront carries no dimensions on any of its four views.
• The three-bay elevation has no bay widths, head or sill levels, glazing panel sizes, or glass
  and framing specification.
• The only tag is SG03, with no size or fixing; the only level is Shore Line FFL 17.110.
• The detail plan is titled 1/A310X — a sheet that does not exist.
```

### Items carried forward from a previous revision

The original issue text stays as raised. Append the new-revision finding under a dated heading,
split into what was fixed and what is still outstanding — that split is the whole point, because
it tells the reader what they are still owed:

```
• W01 and W02 had identical descriptions but were used as distinct types; W03 was described only
  as "76mm stud".

REV.O REVIEW 26.07.26 — PARTIALLY ADDRESSED
• Fixed: W01 and W02 now differ by finish (P4 both sides vs P4 / SF01-B). W04 and J01–J04 added.
• Outstanding: W03 still reads "76mm STUD" only — no lining, thickness or finish.
• No wall heights or head conditions given for any type.
```

Where a revision made something worse, say so in the heading — `— OPEN (not resolved, and now
worse)` — and where a previously closed item has to be reopened, flag it there too:
`— OPEN — REOPENED, was recorded Closed at Rev A`. A reversal buried in body text gets missed.

## Length

| | Target |
|---|---|
| Typical entry | 300–450 characters |
| Dense commercial items (long-lead, multi-sheet conflicts) | up to 500 |
| Hard cap | **550** |

If an entry will not come under 550 without deleting a specific, it is usually two items. Split it.

Check the finished register rather than trusting the feel of it:

```python
lengths = sorted(((len(d), ref) for ref, d in descriptions.items()), reverse=True)
print('mean', sum(n for n, _ in lengths) // len(lengths), '| longest', lengths[:5])
print('over 550:', [r for n, r in lengths if n > 550] or 'none')
```

## Compression moves that work

- **Delete the restatement.** If the issue line says the schedule row is blank, the finding does
  not need to say "the schedule row is still blank" — `Unchanged.` does it.
- **Collapse lists.** Not "no stud size, no gauge, no centres, no lining type, no lining
  thickness" but "no stud size, gauge or centres, no lining".
- **Merge a fact and its consequence.** "Surrounding joinery is undimensioned, so the run cannot
  be set out."
- **Cross-reference in parentheses**, never as a sentence: `(CL-032)`, not "please refer to item
  CL-032 which covers this".
- **Drop the closing flourish.** "This is a significant commercial risk" adds nothing to a High
  priority item.

## Compression moves that do not work

- Rewording sentences to be tighter while keeping every clause — this yields ~3% and reads worse.
  Cut whole clauses instead.
- Deleting dimensions, sheet references or codes to hit a number. That is the content.
- Merging the Fixed and Outstanding bullets — the reader loses the thing they most need.

## Column discipline

- **Description of Issue** — what is on the drawing and what is wrong, plus the revision finding.
- **Clarification Question** — the ask, phrased so it can be answered directly. Keep it as
  originally raised on carried-over items even if the sheet has since been renumbered; the
  current sheet belongs in a separate column, not rewritten into the question.
- **Response** — leave completely blank. It belongs to the designer. Never park findings there.
- **Status** — Open / Partially Addressed / Closed only.

## Three things that will bite

**Generate the status heading from the Status cell, never type it.** Users change statuses in
Excel. A typed heading silently contradicts the column:

```python
desc = template.replace('{STATUS}', str(entry['status']).upper())
```

**Stick to characters that render everywhere.** Diameter symbols, and other glyphs outside the
common set, drop out or box in some Excel configurations. Write `3200 dia.` not `⌀3200`. Bullets
(`•`), en dashes (`–`) and `×`-free plain `x` are safe.

**Give conditional-format fills both colours.** A rule fill built as `PatternFill("solid", fgColor=...)` renders white in Excel even though the rule is present. Build every rule fill as `PatternFill(fill_type="solid", start_color=rgb, end_color=rgb)`, then read a cell back through Excel (`DisplayFormat.Interior.Color`) rather than trusting openpyxl.

## When asked to shorten an existing register

1. Back up and verify the backup loads before touching anything — see `invero-pm:safe-xlsx-update`.
2. Read the **live** file. The user has probably edited it; condense their text, not your last copy.
3. Rewrite whole entries. Do not word-tweak.
4. Diff every cell afterwards and assert **only the Description column changed**.
5. Report the per-item reduction, not just the total — an average hides entries that barely moved.

## Keeping this skill current

When the user corrects, refines, or adds to what this skill produced — a changed judgement, a house
convention, a trap you fell into — record the lesson before you finish the turn, then say in one line
what you recorded and where. The point is that the next run starts from the corrected behaviour
instead of repeating the mistake.

This skill ships inside the `invero-pm` plugin, and the installed copy is replaced on every
update — never edit it in place. If the user maintains the plugin (their instructions name its
source folder), edit the source copy of this file. Otherwise record the lesson in the PM project's
`lessons.md` when working under the PM, or tell the user it is worth proposing upstream.

Record only what generalises: a rule, a convention, a recurring trap, a standing preference. Do **not**
record one-off project facts, file paths, or anything already obvious from the inputs. Keep each addition
terse and in the existing voice, and edit or replace the relevant line rather than appending a
near-duplicate — a skill that grows on every correction stops being read.

If the correction is genuinely specific to that one project rather than general, say so and leave the
skill unchanged.
