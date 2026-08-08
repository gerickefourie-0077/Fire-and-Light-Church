#!/usr/bin/env python3
"""Local preview server that matches how Cloudflare serves this site.

The site's links are extensionless (`/contact`), because Workers Static Assets
strips `.html`. Python's plain `http.server` would 404 on those, so this maps
`/contact` -> `contact.html` and `/` -> `index.html`, giving local preview the
same URLs as production.

    python3 serve.py [port]        # default 8812
"""

import http.server
import os
import socketserver
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8812
ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def translate_path(self, path):
        local = super().translate_path(path)

        # Directory request -> its index.html
        if os.path.isdir(local):
            index = os.path.join(local, "index.html")
            if os.path.isfile(index):
                return index

        # Extensionless request -> the .html file behind it
        if not os.path.exists(local) and not os.path.splitext(local)[1]:
            candidate = local + ".html"
            if os.path.isfile(candidate):
                return candidate

        return local

    def end_headers(self):
        # Mirror the production cache policy from _headers, so a stale local
        # copy never masks a change the way an edge copy would.
        if self.path.endswith((".css", ".js")) or "." not in self.path.rsplit("/", 1)[-1]:
            self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("  %s\n" % (fmt % args))


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Fire & Light preview -> http://localhost:{PORT}  (Ctrl-C to stop)")
        httpd.serve_forever()
