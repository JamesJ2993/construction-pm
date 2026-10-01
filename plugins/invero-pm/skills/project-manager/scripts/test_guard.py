r"""Scope guard tests.

Run: python test_guard.py [--project ID]

Two suites:
  1. Fixture - builds a throwaway project and PM home in a temp folder and tries to break out of
     it: sibling projects, parents, traversal, writing the project folder, and a registration
     planted inside the PM's own writable folder.
  2. Live - if a project is registered and its registration carries "scope_tests", runs those
     against the real boundary. Each is {"path", "mode", "allow", "why"}.

The refusals matter more than the permissions. A guard that has only been shown to allow things
has not been tested at all.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import guard
import project


def run(cases, label: str) -> list:
    failures = []
    print(f"\n{label}")
    for path, mode, want, why in cases:
        got = guard.allowed(path, mode)
        ok = got == want
        print(f"  {'pass' if ok else 'FAIL'}  {'allow ' if want else 'REFUSE'} {mode:5} {why}")
        if not ok:
            failures.append((label, why, path))
    allowed_n = sum(1 for c in cases if c[2])
    print(f"  {len(cases)} cases: {allowed_n} allow, {len(cases) - allowed_n} refuse")
    return failures


def fixture_suite() -> list:
    failures = []
    saved_env = {k: os.environ.get(k) for k in ("PM_AGENT_HOME", "PM_PROJECT")}
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        home, jobs = t / "pm-home", t / "jobs"
        root, sibling = jobs / "alpha", jobs / "beta"
        state = root / ".claude" / "pm-agent"
        for d in (home / "projects", root / "Drawings", state, sibling / "Drawings"):
            d.mkdir(parents=True)
        os.environ["PM_AGENT_HOME"] = str(home)
        os.environ.pop("PM_PROJECT", None)
        (home / "projects" / "alpha.json").write_text(json.dumps(
            {"id": "alpha", "name": "Alpha", "root": str(root), "state_dir": str(state)}))
        project.reset()
        project.select()

        cases = [
            (root, "read", True, "the project root"),
            (root / "Drawings" / "set.pdf", "read", True, "its drawings"),
            (state / "state.json", "read", True, "its state"),
            (state / "state.json", "write", True, "state folder is writable"),
            (state / "history" / "x.json", "write", True, "and its history"),

            (root, "write", False, "cannot write the project root"),
            (root / "Drawings" / "set.pdf", "write", False, "project folders are inputs - read only"),
            (root / ".claude" / "settings.json", "write", False, "only the state folder, not its parent"),
            (sibling, "read", False, "a sibling project"),
            (sibling / "Drawings", "read", False, "a sibling project's drawings"),
            (jobs, "read", False, "the parent folder"),
            (root / ".." / "beta", "read", False, "traversal out of the root"),
            (home / "projects" / "alpha.json", "write", False, "its own registration"),
            (Path(tmp), "read", False, "the drive above"),
        ]
        failures += run(cases, "Fixture boundary")

        try:
            guard.check(sibling, "read")
            print("  FAIL  check() returned instead of raising ScopeError")
            failures.append(("fixture", "check-raises", sibling))
        except guard.ScopeError:
            print("  pass  check() raises ScopeError on an out-of-scope path")

        # A registration the PM could rewrite must be refused outright.
        planted = state / "planted.json"
        planted.write_text(json.dumps(
            {"id": "planted", "name": "Planted", "root": str(jobs), "state_dir": str(state)}))
        try:
            project.load(planted)
            print("  FAIL  loaded a registration from inside its own writable folder")
            failures.append(("fixture", "self-writable registration", planted))
        except project.ProjectError:
            print("  pass  refuses a registration inside its own writable folder")

    for k, v in saved_env.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    project.reset()
    return failures


def live_suite(project_id: str | None) -> list:
    try:
        proj = project.select(project_id)
    except project.ProjectError as e:
        print(f"\nLive boundary: skipped ({e})")
        return []
    print("\n" + guard.describe())
    cases = [(c["path"], c.get("mode", "read"), bool(c["allow"]), c.get("why", c["path"]))
             for c in proj.scope_tests]
    if not cases:
        print("  no scope_tests in the registration - add some to pin this project's boundary")
        return []
    return run(cases, f"Live boundary - {proj.name}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", help="registered project id for the live suite")
    args = ap.parse_args()
    if guard._OVERRIDE:
        print("!! PM_SCOPE_OFF is set - refusals are disabled, tests are meaningless")
        return 1
    failures = fixture_suite() + live_suite(args.project)
    if failures:
        print(f"\n{len(failures)} FAILURES")
        for label, why, path in failures:
            print(f"  [{label}] {why}: {path}")
        return 1
    print("\nall pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
