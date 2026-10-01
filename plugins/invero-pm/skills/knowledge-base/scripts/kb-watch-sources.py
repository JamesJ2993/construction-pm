r"""Currency watcher for a knowledge pack - the sensor half of the learning loop.

Fetches each source in a pack's _meta/sources.json, reduces the page to text, hashes it, and
reports which sources moved since last time. It keeps a text snapshot per source so --diff can show
what actually changed rather than merely that something did.

    python kb-watch-sources.py --country au --check             fetch all, report changes
    python kb-watch-sources.py --country au --check --only abcb-news
    python kb-watch-sources.py --country au --diff abcb-news    what actually changed
    python kb-watch-sources.py --country us --list              sources and last check
    python kb-watch-sources.py --country au --check --dry-run   fetch, compare, write nothing
    python kb-watch-sources.py --country au --manual <id> --note "..."   record a person's check

THIS SCRIPT MAKES NETWORK REQUESTS - one HTTP GET per source, to the public URLs in the pack's
sources.json. It runs only when the owner asks for a currency scan; nothing schedules it.

Watch state (hashes, last-checked dates) is written to the owner's overlay copy of sources.json,
never to the shipped pack. Snapshots go to the PM home's cache folder.

WHAT THIS DOES NOT DO: decide whether a change matters. Detection is mechanical; interpretation
needs a model reading the diff - industry-watch-agent's job. A failed fetch is NOT "no change":
failures are reported separately and the stored hash is left alone.

Standard library only.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import date, datetime
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import kbpaths

COUNTRY = ""  # set in main()


def sources_path(for_write: bool = False) -> Path:
    """The overlay copy when it exists (or when writing), else the shipped one."""
    if for_write:
        return kbpaths.writable(COUNTRY, "_meta/sources.json")
    found = kbpaths.find(COUNTRY, "_meta/sources.json")
    if found is None:
        raise SystemExit(f"the {COUNTRY} pack has no _meta/sources.json")
    return found


def changelog_path() -> Path:
    return kbpaths.writable(COUNTRY, "_meta/changelog.jsonl")


def snapshots_dir() -> Path:
    # Snapshots are working state, not knowledge: inside a pack they would be linted as knowledge.
    return kbpaths.cache_dir() / "source-snapshots" / COUNTRY

UA = "Mozilla/5.0 (compatible; invero-pm currency watcher; local use)"
TIMEOUT = 25

SKIP_TAGS = {"script", "style", "noscript", "svg", "head"}

# A page that returns 200 but yields almost no text is a JavaScript-rendered
# shell. Hashing it "succeeds" forever while detecting nothing - the hash lands
# on e3b0c442... , the SHA-256 of the empty string, and the source is silently
# blind. Treated as a failure, because that is what it is.
MIN_TEXT = 500


class TextExtractor(HTMLParser):
    """Reduce HTML to visible text. Stdlib only - there is no bs4 here."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            t = data.strip()
            if t:
                self.parts.append(t)

    def text(self) -> str:
        return "\n".join(self.parts)


# Volatile fragments that change on every load and would make every source look
# changed forever: timestamps, cache-busting ids, csrf tokens, view counts.
NOISE = [
    (re.compile(r"\b\d{1,2}:\d{2}(:\d{2})?\s*(am|pm)?\b", re.I), ""),
    (re.compile(r"\b[0-9a-f]{16,}\b", re.I), ""),
    (re.compile(r"\bnonce[-=][\w-]+", re.I), ""),
    (re.compile(r"\s+"), " "),
]


def normalise(text: str) -> str:
    for pat, rep in NOISE:
        text = pat.sub(rep, text)
    return text.strip()


# Snapshots are stored one item per line so a diff points at the item that
# changed rather than reprinting the page. Nav text has few full stops, so
# splitting on sentences alone leaves everything on one line and every diff
# shows the whole page.
SPLIT_BEFORE = re.compile(
    r"(?=\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{4}\b)"
    r"|(?=\b\d{4}-\d{2}-\d{2}\b)"
    r"|(?=\b(?:AS|AS/NZS)\s+\d{3,5}(?:\.\d+)*\b)", re.I)


def to_lines(norm: str) -> str:
    """One item per line, so a diff is readable."""
    text = norm.replace(". ", ".\n")
    out = []
    for line in text.split("\n"):
        parts = [p.strip() for p in SPLIT_BEFORE.split(line) if p and p.strip()]
        out.extend(parts or ([line.strip()] if line.strip() else []))
    return "\n".join(out)


def fetch(url: str) -> tuple[str | None, str | None]:
    """Return (text, error). One of the two is always None."""
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "text/html,application/xhtml+xml"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            raw = r.read()
        enc = "utf-8"
        html = raw.decode(enc, errors="replace")
        p = TextExtractor()
        p.feed(html)
        return p.text(), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return None, f"unreachable: {e.reason}"
    except (OSError, ValueError) as e:
        return None, f"{type(e).__name__}: {e}"


def load_sources() -> dict:
    return json.loads(sources_path().read_text(encoding="utf-8"))


def save_sources(data: dict) -> None:
    p = sources_path(for_write=True)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(p)


def snap_path(sid: str) -> Path:
    return snapshots_dir() / f"{sid}.txt"


def prev_path(sid: str) -> Path:
    return snapshots_dir() / f"{sid}.prev.txt"


def read_snapshot(sid: str, previous: bool = False) -> str | None:
    p = prev_path(sid) if previous else snap_path(sid)
    return p.read_text(encoding="utf-8") if p.exists() else None


def write_snapshot(sid: str, text: str, keep_previous: bool = False) -> None:
    r"""Store the current snapshot.

    keep_previous rolls the existing one to <id>.prev.txt first. Without it,
    --check would overwrite the only copy of the old text the moment it detected
    a change, leaving --diff nothing to compare - useless in exactly the case it
    exists for.
    """
    snapshots_dir().mkdir(parents=True, exist_ok=True)
    cur = snap_path(sid)
    if keep_previous and cur.exists():
        prev_path(sid).write_text(
            cur.read_text(encoding="utf-8"), encoding="utf-8")
    cur.write_text(text, encoding="utf-8")


def _log(rec: dict) -> None:
    p = changelog_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def log_activity(kind: str, detail: str) -> None:
    _log({"ts": datetime.now().astimezone().isoformat(timespec="seconds")[:10],
          "action": kind, "target": "_meta/sources.json", "detail": detail,
          "by": "kb-watch-sources"})


def log_change(sid: str, name: str, detail: str, url: str) -> None:
    _log({"ts": datetime.now().astimezone().isoformat(timespec="seconds")[:10],
          "action": "source-changed", "target": f"_meta/sources.json#{sid}",
          "detail": detail, "source": url, "by": "kb-watch-sources"})


def cmd_check(only: str | None, dry_run: bool) -> int:
    data = load_sources()
    today = datetime.now().astimezone().isoformat(timespec="seconds")[:10]
    changed, unchanged, failed, first = [], [], [], []

    manual = []
    for src in data["sources"]:
        sid = src["id"]
        if only and sid != only:
            continue
        if src.get("watch") == "manual":
            manual.append((sid, src.get("last_checked"), src.get("cadence", "monthly")))
            continue
        text, err = fetch(src["url"])
        if err:
            failed.append((sid, err, src.get("last_checked")))
            continue

        norm = normalise(text)
        if len(norm) < MIN_TEXT:
            failed.append((sid, f"only {len(norm)} chars of text - JavaScript-rendered, "
                                f"cannot be watched this way", src.get("last_checked")))
            continue

        digest = hashlib.sha256(norm.encode("utf-8")).hexdigest()
        prev = src.get("content_hash")

        if not prev:                       # never fetched: empty hash or None
            first.append(sid)
        elif digest != prev:
            changed.append(sid)
        else:
            unchanged.append(sid)

        if not dry_run:
            moved = bool(prev) and digest != prev
            write_snapshot(sid, to_lines(norm), keep_previous=moved)
            src["content_hash"] = digest
            src["last_checked"] = today
            if moved:
                log_change(sid, src["name"], f"{src['name']} changed since last check",
                           src["url"])

    if not dry_run:
        save_sources(data)
        log_activity(
            "learn",
            f"currency check: {len(changed)} changed, {len(unchanged)} unchanged, "
            f"{len(first)} baselined, {len(failed)} failed")

    print(f"currency check  {today}{'  (dry run, nothing written)' if dry_run else ''}")
    if first:
        print(f"\n  baselined (first fetch, nothing to compare):")
        for s in first:
            print(f"    {s}")
    if changed:
        print(f"\n  CHANGED - read the diff before deciding it matters:")
        for s in changed:
            print(f"    {s}    python kb-watch-sources.py --country {COUNTRY} --diff {s}")
    if unchanged:
        print(f"\n  unchanged: {', '.join(unchanged)}")
    if failed:
        print(f"\n  FAILED - a failed fetch is not 'no change':")
        for s, err, last in failed:
            print(f"    {s:<26} {err}   (last read: {last or 'never'})")

    if manual:
        print("\n  manual - not fetchable, checked by a person:")
        for sid, last, cadence in manual:
            if not last:
                state = "NEVER CHECKED"
            else:
                try:
                    age = (date.today() - date.fromisoformat(last)).days
                    limit = {"weekly": 8, "monthly": 35}.get(cadence, 35)
                    state = f"last {last}" + (f"  OVERDUE by {age - limit}d" if age > limit else "")
                except ValueError:
                    state = f"last {last}"
            print(f"    {sid:<26} {state}")
            print(f"    {'':<26} record: python kb-watch-sources.py --country {COUNTRY} --manual {sid}")

    if not changed and not first and not failed:
        print("\n  nothing moved.")
    return 0


def cmd_manual(sid: str, note: str) -> int:
    """Record that a person checked a source a fetch cannot reach.

    Unmonitorable is not the same as unmonitored. Without this the source
    silently rots while the dashboard shows the others looking healthy.
    """
    data = load_sources()
    src = next((s for s in data["sources"] if s["id"] == sid), None)
    if src is None:
        print(f"no source {sid!r}")
        return 1
    if src.get("watch") != "manual":
        print(f"{sid} is fetched automatically - use --check, not --manual")
        return 1
    today = datetime.now().astimezone().isoformat(timespec="seconds")[:10]
    src["last_checked"] = today
    save_sources(data)
    log_change(sid, src["name"], note or f"{src['name']} checked manually", src["url"])
    log_activity("learn", f"manual source check: {sid}" + (f" - {note}" if note else ""))
    print(f"recorded manual check of {sid} on {today}")
    if note:
        print(f"  {note}")
    return 0


def cmd_diff(sid: str) -> int:
    r"""Show what changed.

    Prefers the rolled-aside previous snapshot against the current one, which is
    exactly the change --check reported. Falls back to re-fetching and comparing
    against the stored snapshot when there is no previous - useful for spotting
    drift since the last check.
    """
    data = load_sources()
    src = next((s for s in data["sources"] if s["id"] == sid), None)
    if src is None:
        print(f"no source {sid!r}. Known: {', '.join(s['id'] for s in data['sources'])}")
        return 1

    old = read_snapshot(sid, previous=True)
    if old is not None:
        new = read_snapshot(sid)
        label_old, label_new = f"{sid} (before last check)", f"{sid} (after)"
    else:
        stored = read_snapshot(sid)
        if stored is None:
            print(f"no snapshot for {sid} yet - run --check first")
            return 1
        text, err = fetch(src["url"])
        if err:
            print(f"fetch failed: {err}")
            return 1
        old, new = stored, to_lines(normalise(text))
        label_old, label_new = f"{sid} (stored)", f"{sid} (now)"

    diff = list(difflib.unified_diff(old.splitlines(), new.splitlines(),
                                     fromfile=label_old, tofile=label_new,
                                     lineterm="", n=1))
    if not diff:
        print(f"{sid}: identical to the stored snapshot")
        return 0

    added = [l for l in diff if l.startswith("+") and not l.startswith("+++")]
    removed = [l for l in diff if l.startswith("-") and not l.startswith("---")]
    print(f"{sid}  {src['url']}")
    print(f"  {len(added)} added, {len(removed)} removed\n")
    for line in diff[:200]:
        print(f"  {line}")
    if len(diff) > 200:
        print(f"  ... {len(diff) - 200} more lines")
    return 0


def cmd_list() -> int:
    data = load_sources()
    print(f"{len(data['sources'])} monitored sources\n")
    for s in data["sources"]:
        state = "never checked" if not s.get("last_checked") else f"last {s['last_checked']}"
        print(f"  {s['id']:<26} {state:<18} {'/'.join(s.get('applies_to', []))}")
        print(f"      {s['catches']}")
    if data.get("not_monitored"):
        print("\n  deliberately not monitored:")
        for n in data["not_monitored"]:
            print(f"    {n['what']} - {n['why']}")
    return 0


def main() -> int:
    global COUNTRY
    ap = argparse.ArgumentParser(description="Currency watcher for a knowledge pack")
    ap.add_argument("--country", required=True, help="lowercase country code, e.g. au, us")
    ap.add_argument("--check", action="store_true", help="fetch all sources and report changes")
    ap.add_argument("--diff", metavar="ID", help="show what changed for one source")
    ap.add_argument("--list", action="store_true", help="list monitored sources")
    ap.add_argument("--only", metavar="ID", help="restrict --check to one source")
    ap.add_argument("--dry-run", action="store_true", help="fetch and compare, write nothing")
    ap.add_argument("--manual", metavar="ID", help="record a human check of an unfetchable source")
    ap.add_argument("--note", default="", help="what the manual check found")
    a = ap.parse_args()
    COUNTRY = a.country.lower()
    if not kbpaths.pack_roots(COUNTRY):
        print(f"no {COUNTRY} pack in {kbpaths.overlay_root()} or {kbpaths.SHIPPED}")
        return 1

    if a.manual:
        return cmd_manual(a.manual, a.note)
    if a.diff:
        return cmd_diff(a.diff)
    if a.list:
        return cmd_list()
    if a.check:
        return cmd_check(a.only, a.dry_run)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
