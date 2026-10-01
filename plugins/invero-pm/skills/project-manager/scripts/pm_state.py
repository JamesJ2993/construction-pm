r"""Shared state library for the PM agent.

All state for a project lives in its registered state folder (see project.py). Every write is
atomic (tmp + os.replace), every path goes through guard.check(), and mutating runs snapshot
state.json to history\ first. Nothing in this module writes outside the state folder.

Path constants (STATE_PATH, CONFIG_PATH, ACTIVITY_LOG, ...) resolve against the active project on
access, so `pm_state.STATE_PATH` works from a short inline script:

    import sys; sys.path.insert(0, r"<scripts dir>")
    import pm_state
    state = pm_state.load_state()
    pm_state.flip_gate(state, "register_signoff", "approved", note="Rev C approved")
    pm_state.save_state(state)
"""

from __future__ import annotations

import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import guard
import project
from guard import ScopeError  # noqa: F401  (re-exported for callers)

SCHEMA_VERSION = 2

_FILES = {
    "STATE_PATH": "state.json",
    "CONFIG_PATH": "config.json",
    "EMAILS_PATH": "emails.json",
    "ACTIVITY_LOG": "activity-log.jsonl",
    "APPROVALS_LOG": "approvals.jsonl",
    "HISTORY_DIR": "history",
    "REPORTS_DIR": "reports",
    "ANSWERS_INBOX": "answers-inbox.jsonl",
    "ANSWERS_PROCESSED": "answers-processed.jsonl",
    "CHAT_LOG": "chat.jsonl",
    "NOTES_PATH": "project-notes.md",
    "LESSONS_PATH": "lessons.md",
}

STEP_STATUSES = (
    "pending", "briefed", "producing", "in_review",
    "awaiting_signoff", "signed_off", "blocked", "n/a",
)
DOC_STATUSES = ("current", "stale", "missing", "not_required")


def _p(name: str) -> Path:
    return project.current().state_dir / _FILES[name]


def __getattr__(name: str):
    if name == "PM_DIR":
        return project.current().state_dir
    if name in _FILES:
        return _p(name)
    raise AttributeError(f"module 'pm_state' has no attribute {name!r}")


def key() -> str:
    """The active project's id - its key in state.json."""
    return project.current().id


def owner() -> str:
    return project.current().owner


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


_ISO_DT = re.compile(r"(\d{4})-(\d{2})-(\d{2})T(\d{2}:\d{2})(?::\d{2})?(?:[+-]\d{2}:\d{2}|Z)?")
_ISO_D = re.compile(r"(?<!\d)(\d{4})-(\d{2})-(\d{2})(?!\d)")
_ORDER = {
    "YYYY-MM-DD": r"\1-\2-\3",
    "DD.MM.YYYY": r"\3.\2.\1",
    "DD/MM/YYYY": r"\3/\2/\1",
    "MM/DD/YYYY": r"\2/\3/\1",
}


def display_dates(text) -> str:
    """Rewrite ISO dates in text into the project's display format. Internal state stays ISO."""
    s = str(text if text is not None else "")
    pattern = _ORDER.get(project.current().date_format, _ORDER["YYYY-MM-DD"])
    s = _ISO_DT.sub(pattern + r" \4", s)
    return _ISO_D.sub(pattern, s)


def ensure_dirs() -> None:
    history = guard.check(_p("HISTORY_DIR"), "write")
    history.mkdir(parents=True, exist_ok=True)


def _read_text(path: Path) -> str | None:
    """Guarded read. None if the file is absent."""
    p = guard.check(path, "read")
    return p.read_text(encoding="utf-8") if p.exists() else None


def _atomic_write(path: Path, text: str) -> None:
    guard.check(path, "write")
    ensure_dirs()
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def load_json(path: Path, default=None):
    raw = _read_text(path)
    return default if raw is None else json.loads(raw)


def save_json(path: Path, data) -> None:
    _atomic_write(path, json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False, default=str))


def load_config() -> dict:
    cfg = load_json(_p("CONFIG_PATH"))
    if cfg is None:
        raise SystemExit(f"config.json not found at {_p('CONFIG_PATH')} - run init_project.py")
    return cfg


def load_state() -> dict:
    state = load_json(_p("STATE_PATH"))
    if state is None:
        state = {"schema_version": SCHEMA_VERSION, "generated_at": None, "projects": {}}
    if state.get("schema_version", 1) < SCHEMA_VERSION:
        raise SystemExit(
            f"{_p('STATE_PATH')} is schema {state.get('schema_version', 1)}; this PM expects "
            f"{SCHEMA_VERSION}. Migrate it before running.")
    state.setdefault("projects", {})
    return state


def project_state(state: dict) -> dict | None:
    """The active project's entry in state.json, or None before the first scan."""
    return state["projects"].get(key())


def snapshot_state() -> Path | None:
    r"""Copy current state.json into history\ before a mutating run."""
    src = _p("STATE_PATH")
    if not src.exists():
        return None
    ensure_dirs()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = guard.check(_p("HISTORY_DIR") / f"state-{stamp}.json", "write")
    shutil.copy2(guard.check(src, "read"), dest)
    return dest


def save_state(state: dict, snapshot: bool = True) -> None:
    if snapshot:
        snapshot_state()
    state["generated_at"] = now_iso()
    state["schema_version"] = SCHEMA_VERSION
    save_json(_p("STATE_PATH"), state)


def append_jsonl(path: Path, record: dict) -> None:
    guard.check(path, "write")
    ensure_dirs()
    record = {"ts": now_iso(), **record}
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")


def log_activity(action: str, detail: str = "", **extra) -> None:
    append_jsonl(_p("ACTIVITY_LOG"), {"action": action, "detail": detail, "project": key(), **extra})


def log_approval(gate: str, decision: str, by: str | None = None,
                 artifact: str | None = None, note: str = "") -> None:
    append_jsonl(_p("APPROVALS_LOG"), {
        "project": key(), "gate": gate, "decision": decision,
        "by": by or f"{owner()} (in chat)", "artifact": artifact, "note": note,
    })


def _read_jsonl(path: Path) -> list[dict]:
    raw = _read_text(path)
    if raw is None:
        return []
    out = []
    for line in raw.splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def tail_jsonl(path: Path, n: int = 50) -> list[dict]:
    """Last n records, newest first."""
    return list(reversed(_read_jsonl(path)[-n:]))


def post_chat(role: str, text: str) -> None:
    """role: 'owner' (sent from the dashboard) or 'pm' (agent replies shown on the dashboard)."""
    append_jsonl(_p("CHAT_LOG"), {"role": role, "text": text})


def chat_history(n: int = 50) -> list[dict]:
    """Last n chat messages, oldest first."""
    return _read_jsonl(_p("CHAT_LOG"))[-n:]


def pending_answers() -> list[dict]:
    """Unprocessed answers sent from the dashboard (does not consume them)."""
    return _read_jsonl(_p("ANSWERS_INBOX"))


def consume_answers() -> list[dict]:
    """Return all inbox answers and archive them to answers-processed.jsonl."""
    answers = pending_answers()
    if not answers:
        return []
    processed = guard.check(_p("ANSWERS_PROCESSED"), "write")
    with processed.open("a", encoding="utf-8") as f:
        for a in answers:
            f.write(json.dumps({**a, "processed": now_iso()}, ensure_ascii=False) + "\n")
    _atomic_write(_p("ANSWERS_INBOX"), "")
    return answers


def make_waiting(item_id: str, wtype: str, text: str, needed_from: str,
                 raised: str | None = None, due: str | None = None) -> dict:
    """wtype: statutory | approval | missing_input | question | external | email

    A statutory item is a deadline set by law or by the contract - a payment schedule, a payment
    or lien notice, a time-bar. Give it `due` (ISO date). It sorts above everything else on the
    dashboard and survives rescans until resolved, because a missed statutory date cannot be
    recovered.
    """
    item = {
        "id": item_id, "type": wtype, "text": text,
        "needed_from": needed_from, "raised": raised or now_iso()[:10],
    }
    if due:
        item["due"] = due
    elif wtype == "statutory":
        raise ValueError("a statutory waiting-on item needs a due date")
    return item


def set_step(entry: dict, step: str, status: str, detail: str | None = None) -> None:
    assert status in STEP_STATUSES, f"bad status {status}"
    pipeline = entry.setdefault("pipeline", {})
    s = pipeline.setdefault(step, {})
    s["status"] = status
    s["detail"] = detail
    s["updated"] = now_iso()


def resolve(state: dict, item_id: str, answer: str, resolution: str) -> None:
    """Close a waiting-on item on the owner's answer. The next scan will not re-raise it."""
    entry = project_state(state)
    if entry is None:
        raise SystemExit("no project state yet - run scan_state.py first")
    entry.setdefault("resolved", {})[item_id] = {"answer": answer, "resolution": resolution, "ts": now_iso()}
    entry["waiting_on"] = [w for w in entry.get("waiting_on", []) if w["id"] != item_id]
    log_activity("resolved", resolution, item=item_id)


def flip_gate(state: dict, gate: str, decision: str,
              note: str = "", artifact: str | None = None) -> dict:
    """Record the owner's approval or rejection and update the pipeline and waiting-on list."""
    entry = project_state(state)
    if entry is None:
        raise SystemExit("no project state yet - run scan_state.py first")
    log_approval(gate, decision, artifact=artifact, note=note)
    if decision == "approved":
        set_step(entry, gate, "signed_off", note or f"signed off by {owner()}")
        entry["waiting_on"] = [w for w in entry.get("waiting_on", []) if w.get("gate") != gate]
    else:
        set_step(entry, gate, "briefed", f"rejected: {note}" if note else "rejected - rework")
    log_activity("gate", f"{gate} {decision}", note=note)
    return entry
