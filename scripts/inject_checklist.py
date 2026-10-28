#!/usr/bin/env python3
"""Add a tick-able checklist of section headings to selected built pages.

On the "Preparing a Compatible Replication Package" page each ``##`` section is
one requirement a package has to meet, so the page reads naturally as a
checklist. The book-theme's own in-page outline is a React component with no
hook for adding checkboxes, and the theme exposes no ``<head>`` slot for custom
JS (see ``inject_banner.py``), so this is a post-build step: ``assets/checklist.js``
is inlined into every page and, on the pages listed under
``site.options.checklist_pages`` in ``myst.yml``, builds a list of checkboxes
from the article's ``<h2>`` headings, linked to their anchors, and remembers
ticks in ``localStorage``. A heading inside an element with class
``no-checklist`` (a MyST ``{div}``) is left out.

The styles are not injected: they live in the site stylesheet
(``site.options.style``), which the theme loads itself.

Deriving the list from the rendered headings rather than from the markdown
means there is nothing to keep in sync when sections are added or renamed --
a renamed heading simply comes back unticked.

Usage::

    python scripts/inject_checklist.py [--config myst.yml] [--html-dir _build/html]

Re-running over an already-injected tree is a no-op. Like the banner, this is
invisible under ``myst start`` and in the PDF export.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import sys
from pathlib import Path, PurePosixPath

import yaml

from inject_banner import inject

MARKER = "sivacor-checklist-script"

# Relative to the directory holding myst.yml.
SCRIPT_FILE = Path("assets/checklist.js")


def load_site_options(config: Path) -> dict:
    raw = yaml.safe_load(config.read_text()) or {}
    return (raw.get("site") or {}).get("options") or {}


def page_slug(source: str, folders: bool) -> PurePosixPath:
    """Map a source file (as listed in the toc) to its path within the site.

    With ``folders: true`` MyST keeps the folder structure in the URL;
    otherwise every page sits at the root.
    """
    path = PurePosixPath(source).with_suffix("")
    return path if folders else PurePosixPath(path.name)


def check_built(html_dir: Path, source: str, slug: PurePosixPath) -> None:
    if not (html_dir / slug / "index.html").exists():
        sys.exit(
            f"checklist_pages: {source} has no built page at {html_dir / slug} -- "
            "not in the toc, or a typo?"
        )


def build_snippet(script: str, pages: list[str]) -> str:
    if "</script" in script.lower():
        sys.exit(f"{SCRIPT_FILE} must not contain '</script', it is inlined")
    pages_attr = html.escape(json.dumps(pages), quote=True)
    return f'<script id="{MARKER}" data-pages="{pages_attr}">{script}</script>'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", type=Path, default=Path("myst.yml"))
    parser.add_argument("--html-dir", type=Path, default=Path("_build/html"))
    args = parser.parse_args()

    options = load_site_options(args.config)
    sources = options.get("checklist_pages") or []
    if not sources:
        print(f"{args.config}: no site.options.checklist_pages; no checklist injected.")
        return

    folders = bool(options.get("folders"))
    slugs = [page_slug(source, folders) for source in sources]
    for source, slug in zip(sources, slugs):
        check_built(args.html_dir, source, slug)
    # BASE_URL is the prefix the deploy workflow builds the site under.
    base_url = os.environ.get("BASE_URL", "")
    pages = [f"{base_url}/{slug}" for slug in slugs]

    script = (args.config.parent / SCRIPT_FILE).read_text(encoding="utf-8")
    touched = inject(args.html_dir, build_snippet(script, pages), marker=MARKER)
    print(
        f"Injected checklist script into {touched} page(s) under {args.html_dir}; "
        f"active on {', '.join(pages)}"
    )


if __name__ == "__main__":
    main()
