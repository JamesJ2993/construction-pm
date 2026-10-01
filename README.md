# construction-pm

Claude Code plugins for construction and fit-out project management.

| Plugin | What it does |
|---|---|
| [invero-pm](plugins/invero-pm/README.md) | A PM agent and its team of specialist agents for construction and fit-out projects in any country. It watches a project folder (drawing issues, registers, documentation health, programme and cost), briefs specialists for claims, tenders, scope, health checks, site reports and code compliance, runs a live local dashboard and takes every deliverable through independent review and your sign-off. Adapts to the project's building code, payment law and terms (Australia in depth, US starter pack, template for others) |

## Install

In Claude Code:

```
/plugin marketplace add JamesJ2993/construction-pm
/plugin install invero-pm@construction-pm
```

Then install the Python dependencies (also listed in `plugins/invero-pm/requirements.txt`):

```
pip install pymupdf openpyxl python-docx pillow
```

Then ask Claude to "set up the PM on <your project folder>", and tell it the country and region the project is in.

Example prompts, and a full account of what the plugin reads, writes, runs and sends, are in the
[plugin README](plugins/invero-pm/README.md).

## Setup and support

The plugin is free to use under the MIT licence.

Paid setup, customisation and support are available for construction and fit-out firms through
[Invero Projects](https://inveroprojects.com.au).

| Service | What it covers |
|---|---|
| Setup | Registering your projects, matching the config to your folder structure and drawing stages, and a first scan walked through with your PM |
| Customisation | Your checklists, register format, report layout, cost plan labels and sign-off gates built into the config and skills |
| Support | Fixes, updates as Claude Code changes, and help when a scan or stage doesn't behave |

### Booking and payment

Email james@inveroprojects.com.au to book. Include the number of projects and how your project
folders are set out.

Each engagement is quoted per firm.

Work is invoiced on acceptance of the quote.

### Free help

For free help, open a GitHub issue. Responses are best effort with no committed turnaround.

Don't attach client drawings or documents to an issue. Issues are public.

## Developing

If you work from a clone, add it as a local marketplace:

```
claude plugin marketplace add <path to clone>
```

Claude Code runs a cached copy of each plugin and only refreshes it when the version changes. After
editing, run:

```
python refresh.py invero-pm
```

It bumps the patch version in `plugin.json` and in `.claude-plugin/marketplace.json`, then updates
the installed copy. Restart Claude Code or run `/reload-plugins` to pick up the change.

`python package.py invero-pm` builds `dist/invero-pm-<version>.zip` for uploading to
claude.ai (Customize → Plugins → Upload plugin).

## Licence

MIT. See [LICENSE](LICENSE).
