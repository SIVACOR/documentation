#!/usr/bin/env python3
"""Add a tick-able checklist of section headings to selected built pages.

On the "Preparing a Compatible Replication Package" page each ``##`` section is
one requirement a package has to meet, so the page reads naturally as a
checklist. The book-theme's own in-page outline is a React component with no
hook for adding checkboxes, and the theme exposes no ``<head>`` slot for custom
JS (see ``inject_banner.py``), so this is another post-build step: a small
script is injected into every page and, on the pages listed in ``PAGES``, builds
a list of checkboxes from the article's ``<h2>`` headings, linked to their
anchors, and remembers ticks in ``localStorage``.

Deriving the list from the rendered headings rather than from the markdown
means there is nothing to keep in sync when sections are added or renamed --
a renamed heading simply comes back unticked.

Usage::

    python scripts/inject_checklist.py [--html-dir _build/html]

Re-running over an already-injected tree is a no-op. Like the banner, this is
invisible under ``myst start`` and in the PDF export.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from inject_banner import inject

MARKER = "sivacor-checklist-style"

# Site paths (no trailing slash, no origin) of the pages that get a checklist.
# The script is injected everywhere so that client-side navigation to one of
# these pages also triggers it.
PAGES = ["/docs/step0-prepare"]

CHECKLIST_CSS = """
#sivacor-checklist {
  margin: 0 0 1.5rem;
  padding: 0.75rem 1rem;
  border: 1px solid #93c5fd;
  border-left-width: 4px;
  border-radius: 4px;
  background: #eff6ff;
}
html.dark #sivacor-checklist {
  border-color: #1d4ed8;
  background: #0f172a;
}
#sivacor-checklist p {
  margin: 0 0 0.5rem;
  font-weight: 600;
}
#sivacor-checklist ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
#sivacor-checklist li {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  margin: 0.25rem 0;
}
#sivacor-checklist input {
  flex: none;
  width: 1rem;
  height: 1rem;
  cursor: pointer;
}
#sivacor-checklist li.done label {
  text-decoration: line-through;
  opacity: 0.6;
}
#sivacor-checklist button {
  margin-top: 0.5rem;
  padding: 0;
  border: 0;
  background: none;
  color: inherit;
  font-size: 0.85rem;
  opacity: 0.7;
  text-decoration: underline;
  cursor: pointer;
}
#sivacor-checklist button:hover {
  opacity: 1;
}
"""

CHECKLIST_JS = """
(function () {
  var PAGES = __PAGES__;
  var ID = "sivacor-checklist";

  function pagePath() {
    return window.location.pathname.replace(/\\/+$/, "") || "/";
  }

  function storageKey() {
    return "sivacor:checklist:" + pagePath();
  }

  function load() {
    try {
      return JSON.parse(window.localStorage.getItem(storageKey())) || {};
    } catch (e) {
      return {};
    }
  }

  function save(state) {
    try {
      window.localStorage.setItem(storageKey(), JSON.stringify(state));
    } catch (e) {
      /* storage blocked: ticks last for the page view only */
    }
  }

  function headingText(h) {
    var span = h.querySelector(".heading-text");
    return (span ? span.textContent : h.textContent).replace(/\\u00b6\\s*$/, "").trim();
  }

  function build(article, headings) {
    var state = load();
    var box = document.createElement("nav");
    box.id = ID;
    box.setAttribute("aria-label", "Checklist");

    var title = document.createElement("p");
    title.textContent = "Checklist";
    box.appendChild(title);

    var list = document.createElement("ul");
    var inputs = [];
    headings.forEach(function (h) {
      var li = document.createElement("li");
      var input = document.createElement("input");
      input.type = "checkbox";
      input.id = ID + "-" + h.id;
      input.checked = !!state[h.id];
      li.classList.toggle("done", input.checked);
      input.addEventListener("change", function () {
        state[h.id] = input.checked;
        li.classList.toggle("done", input.checked);
        save(state);
      });
      var label = document.createElement("label");
      label.htmlFor = input.id;
      var link = document.createElement("a");
      link.href = "#" + h.id;
      link.textContent = headingText(h);
      label.appendChild(link);
      li.appendChild(input);
      li.appendChild(label);
      list.appendChild(li);
      inputs.push({ input: input, li: li, id: h.id });
    });
    box.appendChild(list);

    var reset = document.createElement("button");
    reset.type = "button";
    reset.textContent = "Clear all";
    reset.addEventListener("click", function () {
      state = {};
      save(state);
      inputs.forEach(function (x) {
        x.input.checked = false;
        x.li.classList.remove("done");
      });
    });
    box.appendChild(reset);

    headings[0].parentNode.insertBefore(box, headings[0]);
  }

  // React attaches a fiber to each DOM node as it hydrates it. Until the
  // headings carry one, inserting our node next to them would be reported as
  // a hydration mismatch and make React throw the server markup away, along
  // with our <style>.
  function hydrated(el) {
    return Object.keys(el).some(function (k) {
      return k.indexOf("__reactFiber") === 0;
    });
  }

  var retries = 0;
  function sync() {
    if (PAGES.indexOf(pagePath()) === -1) return;
    var existing = document.getElementById(ID);
    if (existing && existing.isConnected) return;
    var article = document.querySelector("main article");
    if (!article) return;
    var headings = Array.prototype.slice.call(article.querySelectorAll("h2[id]"));
    if (!headings.length) return;
    if (!hydrated(headings[0])) {
      // A clean hydration mutates nothing, so the observer will not fire
      // again: poll (briefly) instead.
      if (retries++ < 100) window.setTimeout(queueSync, 100);
      return;
    }
    retries = 0;
    build(article, headings);
  }

  var pending = false;
  function queueSync() {
    if (pending) return;
    pending = true;
    window.requestAnimationFrame(function () {
      pending = false;
      sync();
    });
  }

  function start() {
    sync();
    // The theme is a hydrated React app with client-side routing: a reader
    // may arrive at the checklist page without a page load, and React drops
    // our node whenever it re-renders the article, so watch for both.
    new MutationObserver(queueSync).observe(document.body, {
      childList: true,
      subtree: true,
    });
  }

  // Mount only after hydration, or the extra node shows up in React's
  // hydration diff.
  if (document.readyState === "complete") start();
  else window.addEventListener("load", start);
})();
"""


def build_snippet(pages: list[str]) -> str:
    as_json = json.dumps(pages).replace("<", "\\u003c")
    script = CHECKLIST_JS.replace("__PAGES__", as_json)
    return f'<style id="{MARKER}">{CHECKLIST_CSS}</style><script>{script}</script>'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--html-dir", type=Path, default=Path("_build/html"))
    args = parser.parse_args()

    touched = inject(args.html_dir, build_snippet(PAGES), marker=MARKER)
    print(
        f"Injected checklist script into {touched} page(s) under {args.html_dir}; "
        f"active on {', '.join(PAGES)}"
    )


if __name__ == "__main__":
    main()
