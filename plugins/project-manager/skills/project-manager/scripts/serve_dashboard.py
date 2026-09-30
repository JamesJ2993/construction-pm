r"""Local PM dashboard server.

Serves the live dashboard at http://127.0.0.1:<dashboard_port> (8765 unless the registration says
otherwise), re-rendered from state.json on every load. Its Send-to-PM buttons and chat panel append
to answers-inbox.jsonl and chat.jsonl in the state folder, where the PM agent reads them.

Usage: python serve_dashboard.py [--project ID]

Localhost only. Writes nothing outside the state folder.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import pm_state
import project
import render_dashboard


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send(self, code: int, body: str, ctype: str = "text/html; charset=utf-8"):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html", "/dashboard.html"):
            try:
                self._send(200, render_dashboard.build_html())
            except Exception as e:
                self._send(500, f"<pre>render error: {e}</pre>")
        elif self.path == "/health":
            self._send(200, "ok", "text/plain")
        elif self.path == "/answers":
            self._send(200, json.dumps(pm_state.pending_answers()), "application/json")
        elif self.path == "/chat":
            self._send(200, json.dumps(pm_state.chat_history()), "application/json")
        elif self.path == "/activity":
            self._send(200, json.dumps(pm_state.tail_jsonl(pm_state.ACTIVITY_LOG, 200)),
                       "application/json")
        else:
            self._send(404, "not found", "text/plain")

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n).decode("utf-8", "replace") if n else ""
        if self.path == "/answer":
            try:
                payload = json.loads(raw)
                records = payload if isinstance(payload, list) else [payload]
                clean = []
                for rec in records:
                    item_id, answer = str(rec["id"]), str(rec["a"]).strip()
                    assert item_id and answer
                    clean.append({"id": item_id, "q": str(rec.get("q", ""))[:500],
                                  "a": answer[:4000], "source": "dashboard"})
                assert clean
            except Exception:
                self._send(400, json.dumps({"ok": False}), "application/json")
                return
            for rec in clean:
                pm_state.append_jsonl(pm_state.ANSWERS_INBOX, rec)
            self._send(200, json.dumps({"ok": True, "count": len(clean)}), "application/json")
        elif self.path == "/chat":
            try:
                rec = json.loads(raw)
                text = str(rec["text"]).strip()
                assert text
            except Exception:
                self._send(400, json.dumps({"ok": False}), "application/json")
                return
            pm_state.post_chat("owner", text[:4000])
            self._send(200, json.dumps({"ok": True}), "application/json")
        elif self.path == "/rescan":
            try:
                subprocess.run([sys.executable, str(Path(__file__).parent / "scan_state.py"),
                                "--project", project.current().id],
                               timeout=600, capture_output=True)
                self._send(200, json.dumps({"ok": True}), "application/json")
            except Exception as e:
                self._send(500, json.dumps({"ok": False, "error": str(e)[:200]}), "application/json")
        else:
            self._send(404, "not found", "text/plain")


class _Server(ThreadingHTTPServer):
    allow_reuse_address = True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", help="registered project id (default: PM_PROJECT, or the only one)")
    args = ap.parse_args()
    proj = project.select(args.project)
    port = proj.dashboard_port
    try:
        srv = _Server(("127.0.0.1", port), Handler)
    except OSError:
        print(f"already running on port {port}")
        return 0
    print(f"PM dashboard for {proj.name}: http://127.0.0.1:{port}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
