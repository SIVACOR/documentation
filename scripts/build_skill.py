#!/usr/bin/env python3
"""Assemble the step-by-step user guide into a single ``SKILL.md``.

The five ``docs/step*.md`` pages are the whole submission workflow, from
preparing a package to downloading the signed result. Concatenated into one
Markdown file with an Agent-Skills frontmatter, they make a skill that an AI
coding assistant (or a person) can load to walk a researcher through SIVACOR
without browsing the site. ``SKILL-HEADER.md`` supplies the frontmatter and
framing, ``SKILL-FOOTER.md`` the quick reference; both live at the repository
root, next to ``footer.md``, and are excluded from the MyST build.

Usage::

    python scripts/build_skill.py [--out _build/html/SKILL.md] [--site-url URL]

The default output lands inside the built site, so the deploy publishes it at
``<site>/SKILL.md``. The source pages are MyST, and stay MyST: colon fences
(``:::{tip}``, tab sets) are readable as-is and are left alone. What does get
rewritten is whatever only makes sense on the rendered site:

* the ``kernelspec`` frontmatter of executable pages is dropped;
* ``{code-cell}`` blocks (the disk-space table) are replaced by a link to the
  rendered page, since the skill cannot run Python;
* screenshots are dropped;
* ``(label)=`` targets become ``<a id>`` anchors so ``#label`` links keep
  working inside the single file;
* links between the step pages become in-file anchors, and links to any other
  page become absolute URLs on the site;
* headings are demoted one level so the header's title is the only ``h1``.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

# In order. The stem doubles as the in-file anchor for links between steps.
STEP_FILES = [
    "step0-prepare.md",
    "step1-upload.md",
    "step2-choosing-image.md",
    "step3-monitoring.md",
    "step4-download.md",
]
STEP_STEMS = {Path(f).stem for f in STEP_FILES}

HEADER = ROOT / "SKILL-HEADER.md"
FOOTER = ROOT / "SKILL-FOOTER.md"

FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
# ```{code-cell} ... ``` -- MyST executable cell; the fence may carry options.
CODE_CELL = re.compile(r"^```\{code-cell\}[^\n]*\n.*?^```[ \t]*$\n?", re.DOTALL | re.MULTILINE)
LABEL = re.compile(r"^\(([A-Za-z0-9_-]+)\)=\s*$", re.MULTILINE)
CLASS_OPTION = re.compile(r"^:class:[^\n]*\n", re.MULTILINE)
IMAGE_LINE = re.compile(r"^!\[[^\]]*\]\([^)]*\)\s*\n", re.MULTILINE)
# [text](target) where target is a relative .md page, optionally with #fragment.
# Excludes http(s)/mailto and pure-anchor links, which need no rewriting.
MD_LINK = re.compile(r"\[([^\]]*)\]\((?!https?://|mailto:|#)([A-Za-z0-9_./-]+?)\.md(#[A-Za-z0-9_-]+)?\)")
HEADING = re.compile(r"^(#{1,5})(\s)")
FENCE = re.compile(r"^(`{3,}|~{3,})")


def page_url(site_url: str, stem: str, fragment: str) -> str:
    # `folders: true` in myst.yml keeps the docs/ prefix in the site's URLs.
    return f"{site_url.rstrip('/')}/docs/{stem}{fragment}"


def convert(text: str, stem: str, site_url: str) -> str:
    text = FRONTMATTER.sub("", text, count=1)

    pointer = (
        f"*(This section of the website contains a table that is computed at build time; "
        f"see {page_url(site_url, stem, '#size-considerations' if stem == 'step0-prepare' else '')} "
        f"for the current figures.)*\n"
    )
    text = CODE_CELL.sub(pointer, text)

    text = LABEL.sub(r'<a id="\1"></a>', text)
    text = CLASS_OPTION.sub("", text)
    text = IMAGE_LINE.sub("", text)

    def relink(m: re.Match) -> str:
        label, target, fragment = m.group(1), m.group(2), m.group(3) or ""
        target_stem = Path(target).name
        if target_stem in STEP_STEMS:
            return f"[{label}]({fragment or '#' + target_stem})"
        return f"[{label}]({page_url(site_url, target_stem, fragment)})"

    text = MD_LINK.sub(relink, text)
    return demote_headings(text).strip() + "\n"


def demote_headings(text: str) -> str:
    """Add one ``#`` to every heading, leaving ``#`` comments in code blocks alone."""
    out, fence = [], None
    for line in text.split("\n"):
        m = FENCE.match(line)
        if m and fence is None:
            fence = m.group(1)
        elif m and line.startswith(fence):
            fence = None
        elif fence is None:
            line = HEADING.sub(r"#\1\2", line)
        out.append(line)
    return "\n".join(out)


def fill(template: str, site_url: str) -> str:
    return (
        template.replace("{{SITE_URL}}", site_url.rstrip("/"))
        .replace("{{BUILD_DATE}}", dt.date.today().isoformat())
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", type=Path, default=ROOT / "_build" / "html" / "SKILL.md")
    ap.add_argument("--site-url", default="https://docs.sivacor.org")
    args = ap.parse_args()

    parts = [fill(HEADER.read_text(encoding="utf-8"), args.site_url).rstrip() + "\n"]
    for name in STEP_FILES:
        stem = Path(name).stem
        body = convert((DOCS / name).read_text(encoding="utf-8"), stem, args.site_url)
        parts.append(f'\n<a id="{stem}"></a>\n\n{body}')
    parts.append("\n" + fill(FOOTER.read_text(encoding="utf-8"), args.site_url).rstrip() + "\n")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("".join(parts), encoding="utf-8")
    print(f"wrote {args.out} ({args.out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
