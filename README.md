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
