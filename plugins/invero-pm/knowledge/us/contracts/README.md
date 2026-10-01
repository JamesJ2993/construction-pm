---
title: Contract forms in US construction — AIA, ConsensusDocs, DBIA, EJCDC
source: AIA Contract Documents (https://www.aiacontracts.com); ConsensusDocs (https://www.consensusdocs.org); DBIA (https://dbia.org); EJCDC (https://www.ejcdc.org)
verified: 2026-10-01
confidence: provisional
licence: own-words
applies_to: [all]
tags: [contracts, aia, a201, consensusdocs]
---

# Contract forms in US construction

**Overview only.** This file tells a project manager which family of documents they are probably
holding and what it calls the parties, so the agents use the contract's own words. It does not say
what any clause means. Read the executed agreement and its supplementary conditions.

**Provisional.** Written from general knowledge. What would verify it: a person confirms each
document's current edition with its publisher, and the curator moves the file to `verified`.

| Family | Documents a PM meets | Contract administrator |
|---|---|---|
| **AIA** (most common in building work) | A101 owner–contractor agreement (stipulated sum), A102 (cost of the work plus fee, with a GMP), **A201 General Conditions**, G702/G703 pay application, G701 change order, G714 construction change directive, G704 certificate of substantial completion | The Architect |
| **ConsensusDocs** | 200 owner–contractor agreement (lump sum), 500 series for construction management at risk | The Owner or its representative |
| **DBIA** | Design-build agreements and general conditions | The Owner |
| **EJCDC** | Engineering and civil/infrastructure work | The Engineer |

## What changes between them, for a PM

- **Who certifies.** Under AIA A201 the Architect certifies payment, evaluates claims in the first
  instance and determines substantial completion. Other families give those jobs to the owner's
  representative. Use the contract's term in every report.
- **Claims and notices.** Each family sets its own notice periods for claims and time extensions,
  and supplementary conditions routinely change them. Record the executed contract's periods in
  `project_facts` at setup; never carry them from another job.
- **Changes.** AIA distinguishes a **change order** (agreed price and time) from a **construction
  change directive** (the owner directs the change before price and time are agreed) and a minor
  change in the work. Register them separately.
- **The printed form is the starting point.** Most owners amend heavily. The supplementary
  conditions are the contract.
