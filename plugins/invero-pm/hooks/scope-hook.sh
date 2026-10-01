#!/usr/bin/env bash
# Run scope_hook.py with the first Python that actually starts. "python3" can be a Windows Store
# stub that exists on PATH but never runs, so each candidate is tried, not just looked up.
# No usable Python: let the call through - the scripts' own guard still holds.
hook="${CLAUDE_PLUGIN_ROOT}/skills/project-manager/scripts/scope_hook.py"
for py in python3 python py; do
  if "$py" -c "" >/dev/null 2>&1; then
    exec "$py" "$hook"
  fi
done
exit 0
