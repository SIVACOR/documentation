#!/usr/bin/env python3
"""Assemble the step-by-step user guide into a single ``SKILL.md``.

The five ``docs/step*.md`` pages are the whole submission workflow, from
preparing a package to downloading the signed result. Concatenated into one
Markdown file with an Agent-Skills frontmatter, they make a skill that an AI
coding assistant (or a person) can load to walk a researcher through SIVACOR
without browsing the site. ``SKILL-HEADER.md`` supplies the frontmatter and
framing, ``SKILL-FOOTER.md`` the quick reference; both live at the repository
root, next to ``footer.md``, and are excluded from the MyST build. They may use
``{{SITE_URL}}``, ``{{BUILD_DATE}}`` and any column of
``docs/_data/jetstream2-nodes.csv`` upper-cased (``{{DISK_GB}}``,
``{{UPLOAD_MAX_GB}}``, ...), taken from the default size.

Usage::

    python scripts/build_skill.py [--out _build/html/SKILL.md] [--site-url URL]

The default output lands inside the built site, so the deploy publishes it at
``<site>/SKILL.md``. The source pages are MyST, and stay MyST: colon fences
(``:::{tip}``, tab sets) are readable as-is and are left alone. What does get
rewritten is whatever only makes sense on the rendered site:

* the ``kernelspec`` frontmatter of executable pages is dropped;
* ``{code-cell}`` blocks are *executed* (they are plain Python reading
  ``docs/_data/*.csv`` and, for step 0, Docker Hub) so that ``{eval}``
  placeholders get their values and displayed HTML tables become Markdown
  tables; cells tagged ``remove-output`` leave nothing behind;
* screenshots are dropped;
* ``(label)=`` targets become ``<a id>`` anchors so ``#label`` links keep
  working inside the single file;
* links between the step pages become in-file anchors, and links to any other
  page become absolute URLs on the site;
* headings are demoted one level so the header's title is the only ``h1``.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import os
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
CODE_CELL = re.compile(r"^```\{code-cell\}[^\n]*\n(?P<body>.*?)^```[ \t]*$\n?", re.DOTALL | re.MULTILINE)
CELL_OPTION = re.compile(r"^:[a-z_-]+:[^\n]*\n")
EVAL = re.compile(r"\{eval\}`([^`]+)`")
TABLE_ROW = re.compile(r"<tr>(.*?)</tr>", re.DOTALL)
TABLE_CELL = re.compile(r"<t[hd]([^>]*)>(.*?)</t[hd]>", re.DOTALL)
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


def html_table_to_md(markup: str) -> str:
    rows = []
    for row in TABLE_ROW.findall(markup):
        cells = TABLE_CELL.findall(row)
        rows.append(
            (
                ["right" in attrs for attrs, _ in cells],
                [html.unescape(re.sub(r"<[^>]+>", "", body)).strip() for _, body in cells],
            )
        )
    if not rows:
        return ""
    aligns, header = rows[0]
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---:" if a else "---" for a in aligns) + "|"]
    out += ["| " + " | ".join(cells) + " |" for _, cells in rows[1:]]
    return "\n".join(out) + "\n"


def run_cells(text: str) -> tuple[str, dict]:
    """Execute each code cell in a shared namespace; replace it with its rendered output.

    Cells run with ``docs/`` as the working directory, as they do under MyST.
    """
    ns: dict = {}
    cwd = os.getcwd()
    os.chdir(DOCS)
    try:

        def replace(m: re.Match) -> str:
            body = m.group("body")
            tags = ""
            while opt := CELL_OPTION.match(body):
                tags += opt.group(0)
                body = body[opt.end():]
            exec(body, ns)  # noqa: S102 -- our own docs' cells
            if "remove-output" in tags:
                return ""
            last = body.strip().splitlines()[-1]
            value = ns.get(last)
            markup = getattr(value, "data", None) if value is not None else None
            if not isinstance(markup, str):
                raise ValueError(f"cannot render output of cell ending in {last!r}")
            return html_table_to_md(markup)

        return CODE_CELL.sub(replace, text), ns
    finally:
        os.chdir(cwd)


def convert(text: str, stem: str, site_url: str) -> str:
    text = FRONTMATTER.sub("", text, count=1)

    text, ns = run_cells(text)
    text = EVAL.sub(lambda m: str(eval(m.group(1), ns)), text)  # noqa: S307

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


def node_values() -> dict[str, str]:
    """``{{DISK_GB}}``-style placeholders, from the default row of the nodes table."""
    with (DOCS / "_data" / "jetstream2-nodes.csv").open(encoding="utf-8") as f:
        node = next(n for n in csv.DictReader(f) if n["default"] == "true")
    return {"{{" + k.upper() + "}}": v for k, v in node.items()}


def fill(template: str, site_url: str) -> str:
    values = {
        "{{SITE_URL}}": site_url.rstrip("/"),
        "{{BUILD_DATE}}": dt.date.today().isoformat(),
        **node_values(),
    }
    for key, value in values.items():
        template = template.replace(key, value)
    return template


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
