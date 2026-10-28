# Developer notes

Notes for maintainers of this site. This folder is excluded from the build
(see `project.exclude` in `myst.yml`).

## Local build environment

Everything needed to build the site locally (Python packages, Node.js, and the
`jupyter-book`/`mystmd` CLIs) lives in the project's `.venv`, which is
git-ignored. Nothing is installed system-wide, and deleting `.venv` removes it
all.

Node.js is installed into the venv with [nodeenv](https://github.com/ekalinin/nodeenv).
The Node major version and the npm packages are read from
`.github/workflows/deploy.yml`, so the local environment follows CI.

### One-time setup

From the repository root:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt nodeenv

# Latest Node release of the major version CI uses
major=$(sed -n 's/.*node-version: *\([0-9]*\).*/\1/p' .github/workflows/deploy.yml | head -1)
version=$(.venv/bin/nodeenv --list 2>&1 | tr -s ' \t' '\n' | grep "^${major}\." | sort -V | tail -1)
.venv/bin/nodeenv -p -n "$version"

# Same npm packages as CI; `-g` installs into .venv once it is activated
source .venv/bin/activate
npm install -g $(sed -n 's/^ *npm install -g \(.*\)$/\1/p' .github/workflows/deploy.yml | xargs)
```

`nodeenv -p` adds Node to the existing venv's `activate` script, so `node`,
`npm`, `myst` and `jupyter-book` all resolve to `.venv/bin` after activation.

### Building

```bash
source .venv/bin/activate
jupyter-book build --execute --html   # HTML site, as in CI
myst build --pdf                      # PDF; also needs Typst on the PATH
```

Output goes to `_build/` (git-ignored). To preview with live reload, run
`jupyter-book start --execute`.

### Updating

Re-run the `npm install -g` line to pick up new `jupyter-book`/`mystmd`
releases. If CI moves to a new Node major version, delete `.venv` and redo the
setup.
