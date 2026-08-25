#!/usr/bin/env python3
"""포트폴리오 HTML 로컬 미리보기 서버.

kms_uxui_portfolio_draft.html은 claude.ai Artifact용 "본문 조각"이라
<!doctype>·<head>·<meta charset>이 없다(퍼블리시 시점에 플랫폼이 감싸줌).
그대로 정적 서빙하면 한글이 깨져 보이므로, 이 서버가 로컬 미리보기용으로만
doctype + UTF-8 meta + viewport를 씌워서 내려준다. 원본 파일은 건드리지 않는다.

    python3 portfolio/preview_server.py [port]
"""
import http.server
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SHELL = (
    "<!doctype html><html lang=\"ko\"><head><meta charset=\"utf-8\">"
    "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
    "{head}</head><body>{body}</body></html>"
)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):  # noqa: N802 (stdlib naming)
        path = self.path.split("?", 1)[0].lstrip("/") or "kms_uxui_portfolio_draft.html"
        target = ROOT / path
        if target.suffix == ".html" and target.is_file():
            fragment = target.read_text(encoding="utf-8")
            title = ""
            if fragment.lstrip().startswith("<title>"):
                end = fragment.index("</title>") + len("</title>")
                title, fragment = fragment[:end], fragment[end:]
            page = SHELL.format(head=title, body=fragment).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(page)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(page)
            return
        super().do_GET()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8899
    print(f"portfolio preview: http://localhost:{port}/kms_uxui_portfolio_draft.html")
    http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
