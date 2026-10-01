---
deliverable: First Pass
aliases: []
filing: report
toc_exempt: true
required_sections:
  - The situation, read back
  - What we read
  - What stood out
  - The pathway
  - A straight fit call
---

# Report structure — First Pass

**Every PM agent.** The first deliverable on every enquiry — produced before any engagement
exists, at no charge, inside **two business days** of receiving the documents.

This file is authoritative on **section order and section contents**. The agent config governs
everything else — filenames, where to save, draft status, evidence rules. Where this file and the
config disagree on structure, this file wins.

Output: `<job no.> - First Pass - YYYY-MM-DD - RevA.docx`, filed to the `filing.report` folder (config.json).

The `.docx` is built per the `deliverable-build` skill — on the firm's letterhead where one is configured.

**Two pages is a ceiling, not a target.** One page is often enough. A thin enquiry produces a
short first pass — do not pad.


## What this document is

The first pass does two opposing jobs at once: it proves the practice is worth paying, without giving
away the thing they would pay for. The advantage it trades on is the one nobody else has — our
agents genuinely read everything, at near-zero cost. So the line is never how much we read. **The
line is how much we conclude.** The first pass reads everything and concludes almost nothing: it
names, it locates, and it stops exactly where the paid work begins.

The sentence that governs every section: *the first pass tells you where it hurts; the Health
Check tells you how much, why, and what to do.* Every observation is a visible
loose thread that only the paid report pulls.


## House presentation rules

These bind every `.docx` built from this structure, above the section order below.

1. **Contents page, then executive summary.** After the title page comes a contents page — a
   `[[TOC]]` marker in the draft, made live by `insert-toc.py` — then the executive summary. It is
   a house element, not a numbered section, and never counts against a page budget.
2. **Prose over tables.** A table earns its place only for a genuine register or matrix — risk and
   action registers, milestone movement, comparison and classification matrices, drawing registers,
   pricing build-ups. Everything else is prose and headed lists.
3. **Start from the controlled structure, never a blank page.** Where the firm keeps a controlled
   template for this deliverable (`config.json → templates.dir`), start from it; otherwise follow
   this file's sections. `check-provenance.py` checks the required sections survived.
4. **Write in the project's terms.** A `{{key}}` in this file stands for the project's terminology
   (`kb_resolve.py --terms`): {{client}}, {{schedule}}, {{change}}, {{payment_application}} and so
   on. Write the deliverable in those words, never the placeholder.

**Build chain.** Follow the `deliverable-build` skill exactly — it carries the script chain and the
`--check` gates.

---

## Title block

Enquiry reference · prospective client · project · documents received [date] · issued [date] ·
prepared by (the firm) · commercial-in-confidence · **"Obligation-free first pass — no
fee, no commitment."**

## 1. The situation, read back

Their problem restated in contract-literate terms, in three to five sentences of prose: the
contract form and whether it is amended (the standard form in `project_facts.contract_form`, or
bespoke), the parties and
their roles, the stage the project has reached, and what they told us worries them — connected to
what the documents actually show. No findings here, and no commentary. The test for this section:
the client reads it and says *"that's exactly it."* Half the value of the first pass is them
seeing that someone actually understood.

## 2. What we read

Opens with the sentence, verbatim: **"We read every page of every document you sent."** It is
written because it is true and because no competitor's free look-over can say it. If it is not
true, the first pass does not go out.

Then the register, one line per document: name · revision · date. Past roughly twelve documents,
group by type with counts — "14 architectural drawings, A-01 to A-14, Rev C, 12 June 2026" is one
line, not fourteen. Where something arrived corrupt, partial or illegible, say so — that too is
proof of reading.

## 3. What stood out

**Three to five observations. Named, located, never analysed.** Each is one or two sentences: the
thing itself, then where it sits — document, clause, page, {{schedule}} line. *"Your {{time_extension}} notice
period is amended down to 5 business days — Special Conditions, item 12, amending cl 34.3."*
*"The {{schedule}} shows no float against the services trade — Rev 4, lines 118–126."* The
observation ends where the consequence begins.

- **Quote numbers, never produce them.** A number that appears in their documents may be named —
  clause references, amended notice periods, dates, a float column showing zero. A number the practice
  would have to calculate — a cost implication, a claim value, a delay quantum — belongs to the
  Health Check and never appears here.
- Choose the three to five a paying client would most want pulled. Where more exist, state the
  count and nothing else: "We noted [n] further items worth attention." The count is a fact, not
  analysis — and it converts.
- Fewer than three genuine observations is a legitimate first pass. Do not pad, and let section 5
  say what a thin list means.
- A sentence that has drifted into *how much* or *what to do* is cut, not softened.

## 4. The pathway

One short paragraph recommending **the engagement that fits** — not a menu recital — followed by
the comparison, one line per pathway:

`Engagement · Fee basis · When it fits`

List the firm's own engagements and fee bases, read from its current fee proposal or fee
schedule — for example a fixed-fee Health Check, contract administration, project management, and
advisory work. Never invent a fee.

Then, for each observation in section 3, one line on what the paid engagement adds to it — the
loose thread made visible: *"O1 — the Health Check tells you what the 5-day regime has already
cost you across the claims made to date, and the notice discipline that stops it."* This is the
only place the paid work is previewed, and it previews the question the paid report answers —
never the answer.

The section closes with the positioning sentence, verbatim: **"The first pass tells you where it
hurts. The Health Check tells you how much, why, and what to do."**

Every fee quoted is read from the firm's current published fee schedule — never invented here.

## 5. A straight fit call

One committed paragraph. Three permitted calls, and no hedging between them:

- **Engage** — which engagement, and the first thing it would do.
- **You don't need us** — with the X specific enough to act on: *"Serve the notice under cl 41.1
  yourself this week; a paid report is not required to tell you that."* It costs nothing, it
  converts like nothing else, and it is the brand promise.
- **Not our work** — and where to go instead.

"It depends" is not a call. Make one.

---

## The paid line — what the first pass never does

These rules sit above every section, and a first pass that breaks one does not go out:

- **No quantification.** No cost implications, claim values, delay figures or computed amounts.
  Numbers are Health Check territory; the quote-never-produce rule in section 3 is the test.
- **No analysis, no recommendations.** The first pass says where it hurts — never how much, never
  why, never what to do about it. The only recommendation it may carry is section 5's call about
  the engagement itself, including "do X yourself."
- **No reliance.** The footer of every page carries, verbatim: *"Preliminary observations based
  on documents provided; not advice and not to be relied upon."* It protects the practice and makes
  the upgrade explicit.
- **No live-dispute positions, ever.** Where the matter is in adjudication, litigation,
  arbitration or a formal notice exchange, section 3 carries no observations on the disputed
  questions — one line instead: "This matter is in [forum]; the practice does not state positions on
  live disputes outside an engagement." Then straight to sections 4 and 5.

## Fixed elements

- Marked `DRAFT — for review` until reviewed under **the review-and-issue procedure**; issued version carries no draft
  marking
- The footer disclaimer line appears on every page, exactly as worded above
- Commercial-in-confidence, prepared for the exclusive use of the prospective client named
- Issued inside two business days of document receipt — the date received and the date issued
  both appear in the title block, so the speed is visible
- The document is free and says so; no fee reference other than published engagement pricing in
  section 4
