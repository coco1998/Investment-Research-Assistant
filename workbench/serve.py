#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import http.server
import json
import os
import socketserver
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PORT = int(os.getenv("IRA_WORKBENCH_PORT", "8765"))
BIND = os.getenv("IRA_WORKBENCH_BIND", "127.0.0.1")
os.chdir(HERE)


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _refresh(self):
        try:
            result = subprocess.run(
                [sys.executable, str(HERE / "refresh_data.py")],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                timeout=120,
            )
            payload = {
                "ok": result.returncode == 0,
                "out": (result.stdout or "")[-1200:],
                "err": (result.stderr or "")[-1200:],
            }
        except Exception as exc:
            payload = {"ok": False, "err": str(exc)}
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(200 if payload["ok"] else 500)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.split("?")[0] == "/api/refresh":
            return self._refresh()
        return super().do_GET()

    def do_POST(self):
        if self.path.split("?")[0] == "/api/refresh":
            return self._refresh()
        self.send_error(404)

    def end_headers(self):
        if self.path.split("?")[0].endswith((".js", ".html")):
            self.send_header("Cache-Control", "no-store")
        super().end_headers()


class Server(socketserver.TCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    subprocess.run([sys.executable, str(HERE / "refresh_data.py")], cwd=str(ROOT))
    url = f"http://localhost:{PORT}/index.html?t={int(time.time() * 1000)}"
    try:
        server = Server((BIND, PORT), Handler)
    except OSError:
        webbrowser.open(url)
        sys.exit(0)
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    print(f"Investment Research Assistant workbench: {url}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
