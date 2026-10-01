---
title: Planning approvals — which instrument governs where, and which jurisdictions are written
source: Each jurisdiction's legislation register; see the table for the page opened against each row
verified: 2026-09-15
confidence: verified
licence: own-words
applies_to: [all]
tags: [planning, jurisdictions, approvals, index]
---

# Planning approvals — which instrument governs where

**Read this before opening any jurisdiction file in this branch.** Planning is the most
jurisdiction-specific subject in the base. There is no national planning law, no model planning
Act, and no jurisdiction whose pathway names transfer to another. New South Wales has exempt
development, complying development certificates and development applications; Victoria has
planning permits, building permits and VicSmart; the words do not mean the same things and do not
map onto each other.

**A jurisdiction with no file in this branch has no answer in this base.** It does not inherit
the New South Wales answer, and the absence of a file is a gap, never a default. That is the
failure this README exists to prevent — the same failure `safety/README.md` prevents for safety
statutes, where Victoria is the exception that catches people out.

## Where the project manager sits

Nothing in this branch is a determination that a permit is or is not required for a particular site. **The firm's legal-requirements procedure governs, where it has one** (`config.json → procedures.legal`): the pathway position on any specific job is established by a person, with the responsible authority and, where relevant, the building surveyor
or certifier. These files tell a project manager what to ask and whom to ask. They do not answer.

## The jurisdiction table

| Jurisdiction | Governing planning instrument | Status in this base |
|---|---|---|
| **Victoria** | **Planning and Environment Act 1987 (Vic)** — planning permit from the responsible authority (usually the council), decided against the municipal planning scheme. Separately, the **Building Act 1993 (Vic)** and **Building Regulations 2018** — building permit from the relevant building surveyor. Two instruments, two authorities. | **Written** — `vic/approval-pathways.md` |
| **New South Wales** | The pathway instruments are exempt development, the complying development certificate and the development application, recorded in `nsw/approval-pathways.md`. **The governing Act is not verified in this base**: legislation.nsw.gov.au returned HTTP 403 to automated fetch at 08:07 on 15 September 2026 — the same block recorded against `gap-sop-nsw-periods`. A person opening the NSW legislation register would settle it. | **Written** — `nsw/approval-pathways.md` |
| **Queensland** | **Planning Act 2016 (Qld)** | **Not written** — `gap-qld-planning` |
| **Western Australia** | **Planning and Development Act 2005 (WA)** | **Not written** — no gap raised; see below |
| **South Australia** | **Not established in this base.** Both plan.sa.gov.au and legislation.sa.gov.au returned HTTP 403 to automated fetch on 15 September 2026. A person opening the South Australian legislation register would settle it. | **Not written** — no gap raised; see below |
| **Tasmania** | **Land Use Planning and Approvals Act 1993 (Tas)** | **Not written** — no gap raised; see below |
| **Northern Territory** | **Planning Act 1999 (NT)** | **Not written** — no gap raised; see below |
| **Australian Capital Territory** | **Planning Act 2023 (ACT)** | **Not written** — no gap raised; see below |

Each named Act above was confirmed against that jurisdiction's own legislation register on
15 September 2026: Queensland at legislation.qld.gov.au (act-2016-025, current in force),
Western Australia at legislation.wa.gov.au, Tasmania at legislation.tas.gov.au (act-1993-070,
current in force), the Northern Territory at legislation.nt.gov.au and the Australian Capital
Territory at legislation.act.gov.au (a/2023-18). **Naming the Act is not the same as knowing the
pathway.** These rows exist so that an unwritten jurisdiction reads as unwritten and points at
the right statute, not so that anyone reasons from the Act's title to an approval route.

## Why only Queensland carries a gap

`gap-qld-planning` is open because Queensland is the jurisdiction most likely to appear next in
this practice's work. The remaining five are recorded here rather than as five separate gap
entries: five near-identical gaps would crowd the gap list without telling anyone anything this
table does not. **If a project lands in any of them, that reasoning is wrong the day it lands** —
raise the gap then, and do not read this paragraph as a decision that the jurisdiction does not
matter.

## What "written" means here

A written file records the pathway, the triggers a fitout project manager checks for, the
separate approvals that are programme predecessors, and what the project manager does about it.
It carries its own provenance and its own limits. It does not carry statutory day counts or fees
unless the source was opened on the verified date, and it never carries a determination for a
specific site.
