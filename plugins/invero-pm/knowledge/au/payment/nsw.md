---
title: Security of Payment — New South Wales
source: Building and Construction Industry Security of Payment Act 1999 (NSW), consolidated text at https://legislation.nsw.gov.au/view/whole/html/inforce/current/act-1999-046 — not reachable by automation (HTTP 403, 14.09.2026); the section pointers below are practice working-paper record, not yet read against the Act
verified: 2026-08-21
confidence: provisional
licence: own-words
applies_to: [NSW]
governing: claims
tags: [commercial, sopa, payment, claims, nsw]
---

# Security of Payment — New South Wales

The governing Act is the **Building and Construction Industry Security of Payment Act 1999 (NSW)**.

**This file is New South Wales only.** It is one jurisdiction of eight and carries no authority
anywhere else — `README.md` in this folder has the shape common to all of them. Nothing here transfers.

**Victorian day counts do not apply in New South Wales.** The NSW periods are read from the sections named below, recorded in the project's contract calendar and in its `project_facts` at setup, and are **not reproduced in this file** — the folder rule, which holds in every jurisdiction. On a NSW matter the Act governs.

A person who carries out construction work has a statutory right to progress payment. The mechanism:

1. **Payment claim** served by the claimant
2. **Payment schedule** served in response by the respondent, stating the scheduled amount and, if it
   is less than claimed, **why**
3. If no schedule is served in time, or the scheduled amount is not paid, the claimant can proceed —
   including to **adjudication**

## Where each clock lives in the Act

No periods are written here. This list exists so a reader goes to the clause that fixes the period
rather than to another jurisdiction's number.

- **The payment-schedule period — s 14, and subsection (4).** The contract may set a **shorter**
  period than the Act's, and where it does, **the earlier date governs**. Read both; the contract
  can only bring the date forward, never push it out.
- **The due date for payment — s 11.** NSW does not run one payment period. It fixes **different
  periods by class of respondent**, and identifying the class is the first step, before any
  counting:
  - **principal to head contractor** — s 11(1A)
  - **head contractor to subcontractor** — s 11(1B)
  - **exempt residential construction contracts** — s 11(1C)

  Here too the contract may shorten the period but **cannot lengthen it**.
- **Reasons that may be run at adjudication — s 20(2B)**, with s 14(3) requiring the schedule to
  indicate its reasons.
- **When a claim may be served, and how many — s 13(1A)–(1C) and s 13(5).**
- **Endorsement — s 13(2)(c).**
- **Service — s 31**, alongside the contract's notices clause.
- **"Business day" — s 4.**

**These subsection numbers are practice working-paper record**, carried from a claim-assessment
working paper of 30 August 2026 that was independently reviewed on its statutory-date leg. They
have **not** been read against the consolidated Act by this agent — see the gap at the foot of this
file. Confirm the pointer before you rely on it, and never cite a subsection to a client from this
file alone.

## Two independent clocks, not one

The schedule clock and the payment clock run **independently** from the same event. Serving a
payment schedule does not stop or reset the payment clock, and paying does not cure a schedule that
was never served. Diarise both the moment a claim is received, and treat neither as a proxy for the
other. The schedule date is the earlier of the two and is the one that forfeits rights.

## Business days are defined in the Act, and NSW's definition is not Victoria's

NSW defines **"business day" in s 4**, with **its own exclusions** — and that definition, not
habit, is what a count runs on.

**The NSW exclusion is narrower than Victoria's.** Victoria's count carries an end-of-year pause that NSW does not match. A Victorian-trained count made in **late December** therefore returns a
date **later** than the NSW truth — and late is the fatal direction, because the right is lost
before anyone notices the arithmetic was wrong. The error is invisible for eleven months of the
year and then costs the full claimed amount.

Two consequences:

- **Count NSW claims on s 4, never on a Victorian business-day habit or sheet.**
- **The public-holiday calendar is New South Wales's**, not Victoria's. The two diverge, and a
  divergent holiday inside a short period moves the date.

The specific calendar dates s 4 excludes are deliberately **not written here** — go to s 4. An
unverified exclusion window in this file would be exactly the confidently wrong date the folder
rule exists to prevent.

## Reasons at adjudication — s 20(2B)

**A respondent cannot include in its adjudication response any reason for withholding payment that
was not already in the payment schedule.** Not a hedge and not a tendency: it is the rule the
section states, and s 14(3) requires the schedule to indicate its reasons in the first place.

**The schedule's face is the whole record.** What is written on it is what can be argued; what was
understood, discussed, emailed or intended and not written is gone. This is the one limb where the
Victorian practitioner discipline transfers whole — state every reason, in the schedule, at the
time.

## Endorsement, reference dates, and the asymmetry rule

This is where reasoning from Victoria misleads most.

**Endorsement — s 13(2)(c).** NSW requires a payment claim to state that it is made under the Act.
The requirement was reinstated by the 2018 amendments and has been in force since 21 October 2019.
An unendorsed claim is **arguably not a payment claim under the Act**, so the statutory clocks
arguably do not run from it.

**Reference dates — NSW retains them; Victoria abolished them on 15 April 2026.** In NSW,
s 13(1A)–(1C) fix when a claim may be served and s 13(5) allows one claim per reference date. A
premature claim, or a second claim against a reference date already used, is a second validity
point. A Victorian habit formed after April 2026 will not see either of them.

**The asymmetry rule — the practice position on both.** A validity doubt is never a reason to let a
clock run:

1. **Fix the service date and serve the payment schedule regardless**, inside the s 14 period, as
   though the claim were valid.
2. **Carry the defect as a reservation on the face of the schedule** — the endorsement point, the
   reference-date point, or both — stated as a reservation of position, not as a refusal to
   schedule.
3. **Never rest the Principal's position on the claim being invalid.**

The asymmetry is the whole argument: the cost of scheduling a claim that turns out to be invalid is
**nil**, and the cost of not scheduling one that turns out to be valid is **the full claimed amount
with no defence** — see s 14(4) and s 15. An invalidity argument is a second line of defence, never
the first.

## Service, and fixing the service date

Point at **s 31** and at the contract's notices clause together; either can bear on when service
took effect, and the contract's machinery is read alongside the Act's rather than instead of it.

The practitioner discipline is jurisdiction-neutral and applies here unchanged:

- **Convert the received timestamp to local time before stamping it.** A UTC or sender-local
  timestamp can sit on the wrong side of midnight, and every downstream date inherits the error.
- **Record the method, the date and the time of service** at receipt, in the contract calendar —
  not reconstructed later from a mail client.
- A claim served late in the day is served that day; the count does not start when it was read.

## The instrument trap — check the tool before you trust its date

**Before relying on any date the practice's claims workbook computes for a New South Wales claim,
confirm its jurisdiction switch has been applied.** The controlled progress-claims workbook was
found to compute the payment due date on the Victorian period and against a Victorian business-day
sheet; a correction was approved, and **an approved correction is not an applied one** — it has to
be confirmed present in the copy in front of you, and in the stocked copy in the project, before
its output means anything.

If in doubt, **count by hand from the sections named above**. A spreadsheet that returns a date
carries no warning that it used the wrong jurisdiction's calendar, which is what makes this failure
mode quiet and expensive.

## Why a PM must care

**The reasons for withholding must be in the payment schedule.** A respondent who fails to serve a
schedule in time, or who serves one that does not state its reasons, is severely limited in what it
can argue later — s 20(2B) is the section that limits it.

This is the trap for a client-side PM: a contractor's claim arrives, the client disputes part of it
informally, nobody serves a compliant payment schedule inside the statutory period, and the client's
position collapses on a technicality rather than on the merits.

**The dates are hard deadlines, not targets.** They do not extend for holidays, illness, or the fact
that the person who assesses claims was on site.

## Practical rules

- **Establish the class of respondent first.** Principal-to-head-contractor and
  head-contractor-to-subcontractor run on different subsections of s 11. Getting the class wrong
  gets the payment date wrong before any counting starts.
- **Diarise the schedule date the moment a claim is received.** Not the payment date — the schedule
  date. It is earlier and it is the one that forfeits rights.
- **State every reason.** Not the main one. Every one. Under s 20(2B) a reason omitted from the
  schedule cannot be run in the adjudication response.
- **Be specific.** "Work not complete" is weak. "Item 4.2, ceiling to zone B, 60% complete against
  100% claimed, valued at $X" is a reason that survives.
- **Do not rely on an email exchange.** The Act contemplates documents served under it. An informal
  agreement about a disputed amount is not a payment schedule.
- **Retention and security are separate questions** from the progress claim itself, and have their own
  release triggers and timing.

## Where it meets the programme

A payment dispute that reaches adjudication consumes management time at exactly the point a job needs
it least. Most of them are avoidable through process rather than argument: claims assessed on time,
schedules served on time, reasons stated properly.

For a PM the deliverable is a **claim assessment turned around inside the statutory window with
reasons documented per item** — not a view on whether the claim is fair.

> **Open gap — `gap-sop-nsw-periods` (high, opened 14 September 2026).** Every section pointer on
> this page is **provisional**. The consolidated Act at
> `https://legislation.nsw.gov.au/view/whole/html/inforce/current/act-1999-046` returns **HTTP 403**
> to automated requests — confirmed again on 14 September 2026 — so no agent has read the sections;
> they are practice working-paper record, not verified text.
>
> **What would verify it: a person opens that URL** and confirms ss 4, 11(1A)/(1B)/(1C),
> 13(1A)–(1C), 13(2)(c), 13(5), 14(3)–(4), 20(2B) and 31 against this page. The request is routed
> through the commissioning Project Manager to `knowledge-curator-agent`; on confirmation the
> provisional entries here move to `verified` with the date the Act was actually opened.
>
> **The periods themselves stay out of this file** under the folder rule, verified or not. They live
> in the Act and in the contract, and they are recorded for a given job in the contract calendar and
> in that project's `project_facts` at setup. Contracts can set shorter
> periods than the statutory maximum, so the contract governs alongside the Act.
