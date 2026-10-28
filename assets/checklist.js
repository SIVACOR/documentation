// Tick-able checklist of a page's ## section headings.
//
// Inlined into every built page by scripts/inject_checklist.py (the book-theme
// has no hook for custom JS); its styles are in assets/site.css. The script tag
// carries the site paths of the pages that get a checklist as JSON in
// `data-pages`, taken from site.options.checklist_pages in myst.yml.
(function () {
  var PAGES = JSON.parse(document.currentScript.dataset.pages);
  var ID = "sivacor-checklist";

  function pagePath() {
    return window.location.pathname.replace(/\/+$/, "") || "/";
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
    return (span ? span.textContent : h.textContent).replace(/\u00b6\s*$/, "").trim();
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
  // a hydration mismatch and make React throw the server markup away.
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
    // MyST drops classes on headings, so a page opts a heading out by
    // wrapping it in a {div} with :class: no-checklist.
    var headings = Array.prototype.slice
      .call(article.querySelectorAll("h2[id]"))
      .filter(function (h) {
        return !h.closest(".no-checklist");
      });
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
