#!/usr/bin/env python3
"""Stamp the build's commit hash and date under the "Made with MyST" link.

Every built page gets a small "Version (abc1234) (2026-10-13)" line in the
footer of the left sidebar, next to the theme's "Made with MyST" link, so a
reader can tell which revision of the docs they are looking at. The hash links
to the commit on GitHub.

The sidebar footer is rendered by the book-theme's React app, which offers no
hook for extra content (see ``inject_banner.py``), so this is another post-build
step: a small script is injected into every page's ``<head>`` and, once the page
has hydrated, appends the line after ``.myst-made-with-myst``. It re-adds the
line if the theme re-renders the sidebar.

Usage::

    python scripts/inject_version.py [--html-dir _build/html] [--commit SHA]

The commit defaults to ``HEAD`` of the checkout; its date is the committer date.
Re-running over an already-injected tree is a no-op. Like the banner, this is
invisible under ``myst start`` and in the PDF export.
"""

from __future__ import annotations

import argparse
import json
import subprocess

from pathlib import Path

from inject_banner import inject

MARKER = "sivacor-version-style"

REPO_URL = "https://github.com/SIVACOR/documentation"

VERSION_CSS = """
#sivacor-version {
  margin-top: 0.25rem;
  text-align: center;
  font-size: 0.7rem;
  line-height: 1.2;
  opacity: 0.7;
}
#sivacor-version a {
  color: inherit;
  text-decoration: none;
}
#sivacor-version a:hover {
  text-decoration: underline;
}
"""

VERSION_JS = """
(function () {
  var cfg = __CFG__;

  function ensure() {
    if (document.getElementById("sivacor-version")) return;
    var anchor = document.querySelector(".myst-made-with-myst");
    if (!anchor || !anchor.parentNode) return;

    var line = document.createElement("div");
    line.id = "sivacor-version";
    line.appendChild(document.createTextNode("Version ("));
    var link = document.createElement("a");
    link.href = cfg.url;
    link.target = "_blank";
    link.rel = "noreferrer";
    link.textContent = cfg.short;
    line.appendChild(link);
    line.appendChild(document.createTextNode(") (" + cfg.date + ")"));
    anchor.parentNode.insertBefore(line, anchor.nextSibling);
  }

  // Mount only after hydration (see inject_banner.py), and keep watching: the
  // theme may re-render the sidebar footer on client-side navigation.
  function start() {
    ensure();
    new MutationObserver(ensure).observe(document.body, {
      childList: true,
      subtree: true,
    });
  }

  if (document.readyState === "complete") start();
  else window.addEventListener("load", start);
})();
"""


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def build_snippet(sha: str, short: str, date: str) -> str:
    """Render the <style> + <script> pair injected into every page's <head>."""
    payload = {"short": short, "date": date, "url": f"{REPO_URL}/commit/{sha}"}
    # `<` escaped so the payload can never terminate the <script> element.
    as_json = json.dumps(payload, sort_keys=True).replace("<", "\\u003c")
    return (
        f'<style id="{MARKER}">{VERSION_CSS}</style>'
        f"<script>{VERSION_JS.replace('__CFG__', as_json)}</script>"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--html-dir", type=Path, default=Path("_build/html"))
    parser.add_argument("--commit", default="HEAD", help="commit to stamp (default: HEAD)")
    args = parser.parse_args()

    sha = git("rev-parse", args.commit)
    short = git("rev-parse", "--short", args.commit)
    date = git("log", "-1", "--format=%cs", args.commit)

    touched = inject(args.html_dir, build_snippet(sha, short, date), marker=MARKER)
    print(f"Injected version {short} ({date}) into {touched} page(s) under {args.html_dir}")


if __name__ == "__main__":
    main()
