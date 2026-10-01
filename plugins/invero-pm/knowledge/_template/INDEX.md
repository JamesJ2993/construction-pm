# <Country> — knowledge pack

Copy this folder to `~/.claude/pm-agent/knowledge/<country code>/` and fill it. Layout, frontmatter
and lint rules: [../README.md](../README.md).

Fill in this order — the agents depend on them in this order:

1. `defaults.json` and `terminology.json`
2. `codes/` — the building code and how its edition is fixed for a project
3. `payment/` — the statutory payment regime, one file per region where it varies. Name the section
   that fixes each period; never write the day counts
4. `safety/`, `permitting/`, `contracts/`, `standards/index.json`
5. `disciplines/` as review work needs them

Record every hole in `_meta/gaps.jsonl` rather than leaving it silently absent.
