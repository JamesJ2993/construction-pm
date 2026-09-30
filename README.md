# construction-pm

Claude Code plugins for construction and fit-out project management.

| Plugin | What it does |
|---|---|
| [project-manager](plugins/project-manager/README.md) | A PM agent that watches a project folder (drawing issues, clarifications registers, documentation health, programme and cost), runs a live local dashboard and takes each stage through independent review and your sign-off |

## Install

In Claude Code:

```
/plugin marketplace add JamesJ2993/construction-pm
/plugin install project-manager@construction-pm
```

Then install the Python dependencies (also listed in `plugins/project-manager/requirements.txt`):

```
pip install pymupdf openpyxl python-docx pillow
```

Then ask Claude to "set up the PM on <your project folder>".

## Setup and support

The plugin is free to use under the MIT licence.

Paid setup, customisation and support are available for construction and fit-out firms through
Invero Projects.

| Service | What it covers |
|---|---|
| Setup | Registering your projects, matching the config to your folder structure and drawing stages, and a first scan walked through with your PM |
| Customisation | Your checklists, register format, report layout, cost plan labels and sign-off gates built into the config and skills |
| Support | Fixes, updates as Claude Code changes, and help when a scan or stage doesn't behave |

Work is quoted per firm. Email james@inveroprojects.com.au with the number of projects and how
your project folders are set out.

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
python refresh.py project-manager
```

It bumps the patch version in `plugin.json` and in `.claude-plugin/marketplace.json`, then updates
the installed copy. Restart Claude Code or run `/reload-plugins` to pick up the change.

`python package.py project-manager` builds `dist/project-manager-<version>.zip` for uploading to
claude.ai (Customize → Plugins → Upload plugin).

## Licence

MIT. See [LICENSE](LICENSE).
