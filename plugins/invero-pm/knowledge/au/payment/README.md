---
title: Security of Payment — the shape of it, and where each jurisdiction lives
source: state and territory legislation registers, checked 22.08.2026
verified: 2026-08-22
confidence: verified
licence: own-words
applies_to: [all]
governing: claims
tags: [commercial, sopa, payment, claims]
---

# Security of Payment

Every State and Territory has a security of payment regime. They share a shape and differ in the
detail — and **the detail is the timing**, which is the part that matters, because the regime is
unforgiving about dates.

One file per jurisdiction in this folder. **The Act governs, and the firm's own claims procedure where it has one** (`config.json → procedures.claims`): where a procedure and a file here differ, the procedure wins.

## The shape, everywhere

1. A person who carries out construction work has a statutory right to progress payment.
2. The claimant serves a **payment claim**.
3. The respondent serves a **payment schedule** in response, stating the scheduled amount and, if it
   is less than claimed, **why**.
4. If no schedule is served in time, or the scheduled amount is not paid, the claimant can proceed —
   including to **adjudication**.

## Why a project manager must care

**The reasons for withholding must be in the payment schedule.** A respondent who fails to serve a
schedule in time, or serves one that does not state its reasons, is severely limited in what it can
argue later. Reasons invented after the fact generally cannot be run at adjudication.

That is the trap for a client-side PM: a contractor's claim arrives, the client disputes part of it
informally, nobody serves a compliant schedule inside the statutory period, and the client's position
collapses on a technicality rather than on the merits.

**The dates are hard deadlines, not targets.** They do not extend for holidays, illness, or the fact
that the person who assesses claims was on site.

## The rule for every file in this folder

**No day counts here, in any jurisdiction.** Not one. The periods live in the applicable Act and the contract, and a date wrong by a day is worse than no date at all. A
file here names the Act, describes the mechanism, names the traps, and points at the authority.
Each jurisdiction file names the **section of the Act that fixes each period**, so the reader is sent to the clause and never to another
jurisdiction's number.

Contracts can also set shorter periods than the statutory maximum, so the contract governs alongside
the Act. Establish both at project setup and record them in the contract calendar and in the project's `project_facts` (`config.json`).

## Jurisdictions

Every Act named below was checked against the jurisdiction's legislation register on
22 August 2026. **Naming the Act is not knowing the Act** — a file exists for a jurisdiction
only where the mechanism and the traps have been written down.

| Jurisdiction | Governing Act | File |
|---|---|---|
| Victoria | Building and Construction Industry Security of Payment Act 2002 (Vic), as amended from 15 April 2026 | `vic.md` |
| New South Wales | Building and Construction Industry Security of Payment Act 1999 (NSW) | `nsw.md` |
| Queensland | Building Industry Fairness (Security of Payment) Act 2017 (Qld) | `qld.md` |
| Western Australia | Building and Construction Industry (Security of Payment) Act 2021 (WA) | gap |
| South Australia | Building and Construction Industry Security of Payment Act 2009 (SA) | gap |
| Tasmania | Building and Construction Industry Security of Payment Act 2009 (Tas) | gap |
| Australian Capital Territory | Building and Construction Industry (Security of Payment) Act 2009 (ACT) | gap |
| Northern Territory | Construction Contracts (Security of Payments) Act 2004 (NT) | gap |

**The Northern Territory and Western Australia are structurally different.** Their Acts descend
from the West Coast model — built around adjudication of payment disputes under construction
contracts — rather than the East Coast payment-claim / payment-schedule machinery the other six
share. The NT Act is not even titled "security of payment" in the same form. **What a missed
step costs is not the same**, and reasoning from the Victorian or NSW file to a WA or NT project
will produce a confident wrong answer. Establish the Act at project setup and record it as `project_facts.payment_law`.
