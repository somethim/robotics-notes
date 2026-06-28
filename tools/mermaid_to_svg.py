"""
MkDocs hook: render inline ```mermaid blocks to SVG at build time.

Keep diagrams as ```mermaid fences in the markdown. On build, each block is
rendered to an SVG and replaced with an <img>, so the diagram is a real image —
crisp at any zoom and zoomable via the glightbox plugin.

Renderer (auto-detected, in order):
  1. LOCAL — mermaid-cli (`mmdc`) driving a local headless browser. Fully
     offline, no external service. Looked up via $MMDC, then node_modules/.bin/mmdc,
     then PATH. The browser is auto-detected ($PUPPETEER_EXECUTABLE_PATH, else
     chromium / google-chrome / brave on PATH).
  2. FALLBACK — the kroki.io web service (needs network), used only if mmdc is
     not found.

Rendered SVGs are cached on disk (.diagram-cache/, keyed by diagram content), so
unchanged diagrams are not re-rendered and rebuilds stay fast.

Set up local rendering once:
    cd <repo> && PUPPETEER_SKIP_DOWNLOAD=1 bun add -d @mermaid-js/mermaid-cli
    (any system Chromium/Chrome/Brave is used; no Chromium download needed)

Enabled via mkdocs.yml:
    hooks:
      - tools/mermaid_to_svg.py
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request

from mkdocs.structure.files import File

_MERMAID = re.compile(r"```mermaid\s*\n(.*?)```", re.S)
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
_CACHE = os.path.join(_ROOT, ".diagram-cache")
_KROKI = "https://kroki.io/mermaid/svg"
_announced = set()


def _announce(msg):
    if msg not in _announced:
        _announced.add(msg)
        print(f"[mermaid_to_svg] {msg}", file=sys.stderr)


def _find_mmdc():
    env = os.environ.get("MMDC")
    if env and os.path.exists(env):
        return env
    local = os.path.join(_ROOT, "node_modules", ".bin", "mmdc")
    if os.path.exists(local):
        return local
    return shutil.which("mmdc")


def _find_browser():
    env = os.environ.get("PUPPETEER_EXECUTABLE_PATH")
    if env:
        return env
    for b in ("chromium", "chromium-browser", "google-chrome-stable",
              "google-chrome", "brave", "brave-browser"):
        p = shutil.which(b)
        if p:
            return p
    return None


_MMDC = _find_mmdc()
_BROWSER = _find_browser()
_PPTR_CFG = None


def _puppeteer_cfg():
    global _PPTR_CFG
    if _PPTR_CFG:
        return _PPTR_CFG
    os.makedirs(_CACHE, exist_ok=True)
    cfg = os.path.join(_CACHE, "puppeteer.json")
    data = {"args": ["--no-sandbox"]}
    if _BROWSER:
        data["executablePath"] = _BROWSER
    with open(cfg, "w") as fh:
        json.dump(data, fh)
    _PPTR_CFG = cfg
    return cfg


def _render_local(src):
    with tempfile.TemporaryDirectory() as d:
        i = os.path.join(d, "in.mmd")
        o = os.path.join(d, "out.svg")
        with open(i, "w") as fh:
            fh.write(src)
        subprocess.run(
            [_MMDC, "-i", i, "-o", o, "-p", _puppeteer_cfg(), "-b", "white"],
            check=True, capture_output=True,
        )
        with open(o, "rb") as fh:
            return fh.read()


def _render_kroki(src):
    req = urllib.request.Request(
        _KROKI, data=src.encode("utf-8"), method="POST",
        headers={"Content-Type": "text/plain", "User-Agent": "mkdocs-mermaid-hook"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def _render(src):
    os.makedirs(_CACHE, exist_ok=True)
    key = hashlib.sha256(src.encode("utf-8")).hexdigest()[:16]
    path = os.path.join(_CACHE, key + ".svg")
    if not os.path.exists(path):
        if _MMDC:
            _announce(f"local render via mermaid-cli ({_BROWSER or 'puppeteer browser'})")
            svg = _render_local(src)
        else:
            _announce("mermaid-cli not found — falling back to kroki.io (network)")
            svg = _render_kroki(src)
        with open(path, "wb") as fh:
            fh.write(svg)
    with open(path, "rb") as fh:
        return key, fh.read()


def on_page_markdown(markdown, *, page, config, files, **kwargs):
    counter = {"n": 0}

    def replace(match):
        counter["n"] += 1
        src = match.group(1).rstrip() + "\n"
        key, svg = _render(src)
        uri = f"assets/diagrams/{key}.svg"
        if files.get_file_from_path(uri) is None:
            files.append(File.generated(config, uri, content=svg))
        page_dir = os.path.dirname(page.file.src_uri)
        rel = os.path.relpath(uri, page_dir) if page_dir else uri
        title = page.title or "Diagram"
        return f"![{title} — diagram {counter['n']}]({rel})"

    return _MERMAID.sub(replace, markdown)
