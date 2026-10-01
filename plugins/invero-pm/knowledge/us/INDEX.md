# United States — starter knowledge pack

A **starter** pack. It carries the national picture — how codes are adopted, how payment, liens
and bonds work, OSHA and State Plans, the contract families, permitting — and the US terms the
agents write in. It carries **no state-by-state legal detail**: building codes, prompt payment and
lien deadlines, State Plans and permits are all set by the state or the locality, and each state's
file is written on first use by the knowledge curator, with the owner's OK, marked `provisional`
until a person confirms it. The layout and frontmatter contract are in [../README.md](../README.md).

**Every file here is `provisional`.** Read the confidence line before relying on anything, and say
so in any finding that rests on it.

| Branch | File | What |
|---|---|---|
| codes | [README.md](codes/README.md) | No national code: model I-Codes, adoption by state and locality, which edition governs, ADA vs the building code |
| payment | [README.md](payment/README.md) | Pay applications, prompt payment acts, mechanics' liens, retainage, Miller Act bonds — and what each state file must name |
| safety | [README.md](safety/README.md) | OSHA Part 1926, State Plans, and the multi-employer citation policy that makes "observe, never direct" matter |
| contracts | [README.md](contracts/README.md) | AIA, ConsensusDocs, DBIA, EJCDC — who certifies under each |
| permitting | [README.md](permitting/README.md) | Zoning, building and trade permits, fire and health review, inspections, certificate of occupancy |
| standards | [README.md](standards/README.md), `index.json` | Commonly met referenced standards — pointers and paraphrase only |
| disciplines | [README.md](disciplines/README.md) | Sheet designators and names; review checklists are a gap |

Validate with `kb-lint.py lint --country us`. Open holes: `kb-gaps.py --country us`.

## State files

None ship. `kb_resolve.py` reports which state files a project needs and which are missing; the PM
raises the missing ones with the owner and commissions the curator to write them into the owner's
overlay (`~/.claude/pm-agent/knowledge/us/`).
