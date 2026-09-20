---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Preparing a Compatible Replication Package

## Use a single software application per step

Each step of a SIVACOR submission only supports a single software application (e.g., Stata, R, Python). If your replication package requires multiple applications, you will need to configure separate steps. However, your package itself can include the code for multiple applications, and you can chain them together in a highly simplified workflow system at submission, see [instructions in Step 2](#chained-runs-steps).

::::{admonition} Additional information
:class: dropdown seealso

The single-application requirement means you cannot call one application from another (e.g., call R from Stata). If your code iterates frequently between applications, for instance in a loop, it is also not recommended to use this system. It can, however, be used when a small number of actions are needed in one software application, with the bulk in a main application. For instance, if you use Stata for data preparation, but R for all remaining analysis. 

::::

## Do not include any data that you are not allowed to upload to third-party systems

While SIVACOR does not publish data or replication packages, and deletes completed jobs after a short period of time, it is not a designated secure computing system.[^data] You should not upload *controlled* data, and all uploads should be compatible with any data use agreement you signed. 

[^data]: SIVACOR runs on [JetStream2](https://jetstream-cloud.org/) infrastructure. The [JS2 Acceptable Use and Data Policy](https://docs.jetstream-cloud.org/general/policies/#acceptable-use-of-jetstream2) apply. SIVACOR's privacy policy can be found at <https://submit.sivacor.org/privacy>.

If you have data that you are allowed to upload, but not publish, see "[Excluding files](#excluding-files-from-final-package)" on how to exclude files from the final replication package.



(excluding-files-from-final-package)=
## Excluding files from final package

The final digitally signed replication package contains all data as originally uploaded. If you need to remove files because you do not have redistribution rights, or large intermediate files, include a file named `.sivacorignore` (note the leading dot!) at the root of your project to exclude files or directories before package is finalized. This will be logged as part of the [TRO](https://transparency-certified.github.io/trace-specification/docs/elements.html#transparency-certified-research-objects-tro). 

:::{admonition} Example file and usage
:class: dropdown hint

The `.sivacorignore` file follows the same pattern rules as [`.gitignore`](https://git-scm.com/docs/gitignore), so you can use [glob patterns](https://en.wikipedia.org/wiki/Glob_%28programming%29), negations, and directory-specific rules.

For example, to exclude a `data/raw/` directory and all `.tmp` files, the `.sivacorignore` file would look like this:

```
data/raw/
*.tmp
```

Your replication package then should look somewhat like this:

```
data/raw/
  file1.csv
code/
  main.R
  ...
.sivacorignore
```

before it is run, and might look like this

```
code/
  main.R
output/
  figure.png
  ...
.sivacorignore
```

after the run (note removal of `data/raw`).

:::



## Your replication package should be portable.

Code must run **without manual intervention**, use a **single controller script** (e.g., `main.do` or `master.R`) per step, and **omit hard-coded absolute paths**. File and directory paths are  **case-sensitive**, and should use **OS-neutral path separators** (`/`, not `\`). 

:::{seealso}

For some guidance on constructing a portable replication package, see [Steps 1-3](https://aeadataeditor.github.io/aea-de-guidance/preparing-replication-package.html#step-1-main-file) at the AEA Data Editor's website. 

:::

(dependencies)=
## All dependencies must either be included or installed automatically.

If your code uses libraries or packages, you must ensure that they are **installed automatically** (for Stata, we suggest you include them). We strongly encourage packages that use "environments", and packages to manage dependencies.

::::::{seealso} Details
:class: dropdown

:::::{tab-set}

::::{tab-item} R

Possible approaches include [`renv`](https://rstudio.github.io/renv/) or [`packrat`](https://rstudio.github.io/packrat/).[^groundhog] You can also include code at the top of your main R script to install any required packages that are not already installed. All code necessary to manage depenedencies must be part of the replication package, and must run unattended. For instance, if using `renv`, include the `.Rprofile` and ensure that `renv::restore()` is called at the start of your main R script. 

[^groundhog]: [`groundhog`](https://cran.r-project.org/web/packages/groundhog/index.html) is another option for managing R package dependencies. However, on Linux, it always recompiles from source, which can take a very long time, and may fail, depending on the system libraries required on the `rocker` images used here.


:::{warning}

Do not define a `CRAN` archive (e.g., `https://cloud.r-project.org`) in your replication package. It is generally much more efficient to leverage the `CRAN` mirror defined naturally within the `rocker` images. 

:::

::::

::::{tab-item} Stata

Guidance for portable dependencies for Stata is provided [at Step 3](https://aeadataeditor.github.io/aea-de-guidance/preparing-replication-package.html#step-3-dependencies) of the AEA Data Editor's guidance. See also the World Bank's [`repado`](https://worldbank.github.io/repkit/reference/repado.html).

Note that even when you include Stata packages, you should provide the script that originally installed them, to demonstrate provenance.

::::

::::{tab-item} Julia

Include a `Project.toml` and `Manifest.toml`. 

Declare your dependencies in a `Project.toml`. 
The `Manifest.toml`, if present, will ensure that the code will install and use the same versions. Without it,  `Project.toml` will install latest versions of the dependencies.

Both can be generated by "activating" your project, and then interactively adding your dependencies:

```julia
julia --project=.
julia> ]           # enter the package REPL
(YourProject) pkg> add DataFrames CSV GLM
```

When running, include a `setup.jl` as your first workflow step (suggested), or include it in your main file:

```{code} julia
:filename: setup.jl
using Pkg
Pkg.instantiate()
```


Alternatively, use a `install.jl` to programmatically install your dependencies.

```julia
julia --project=.
julia> include("install.jl")
```

where

```{code} julia
:filename: install.jl
# Install project dependencies
using Pkg
Pkg.add("DataFrames")
Pkg.add("CSV")
Pkg.add("GLM")
```

Include `Project.toml` and `Manifest.toml`, as well as `setup.jl`  or `install.jl` if present,  next to your main file, or at the top of your package. 


::::
:::::
::::::

:::{admonition} Minimal sample code
:class: dropdown seealso

- Sample code for Stata (any version), Scenario B: <https://github.com/SIVACOR/sivacor-test-stata>
- Sample code for Stata (any version), Scenario A (`main.do` in a non-root directory): <https://github.com/SIVACOR/sivacor-test-stata/tree/scenario-A>
- Sample code for R (set up for R 4.3.1, tested on R 4.5.1): <https://github.com/SIVACOR/sivacor-test-r>
- Sample code for MATLAB with and without use of Dynare: <https://github.com/SIVACOR/sivacor-test-matlab> (both use the same `dynare/dynare` container).
- Sample code for Julia (any version): <https://github.com/SIVACOR/sivacor-test-julia>


:::


(size-considerations)=
## Package must be able to fit on the SIVACOR workers

```{code-cell} python
:tags: ["remove-input", "remove-output"]

# ==============================================================
import csv
import math
from pathlib import Path

import requests
import yaml
from IPython.display import HTML

DATA = Path("_data")

# Everything is GiB (powers of 1024), as `df` on a worker reports it.
nodes = list(csv.DictReader((DATA / "jetstream2-nodes.csv").open()))
node = next(n for n in nodes if n["default"] == "true")
DISK_GIB = float(node["disk_fs_gib"])
OVERHEAD_GIB = float(node["overhead_gib"])
FOOTPRINT_FACTOR = float(node["footprint_factor"])  # on-disk / compressed, see _data/README.md
BASE_FREE_GIB = DISK_GIB - OVERHEAD_GIB

images = list(csv.DictReader((DATA / "container-images.csv").open()))

repos_url = "https://raw.githubusercontent.com/SIVACOR/sivacor-repo-choice/main/allowed_repos.yaml"
allowed = yaml.safe_load(requests.get(repos_url).text)


def hub_compressed_gib(image, tag):
    info = requests.get(f"https://hub.docker.com/v2/repositories/{image}/tags/{tag}/").json()
    size = next((i["size"] for i in info["images"] if i["architecture"] == "amd64"), info["full_size"])
    return size / 1024**3


rows = []
for img in images:
    name = img["image"]
    if not allowed.get(name):  # not (or no longer) on the allow-list: skip, don't fail the build
        continue
    tag = str(allowed[name][0])
    compressed = float(img["compressed_gib"]) if img["compressed_gib"] else hub_compressed_gib(name, tag)
    on_disk = compressed * FOOTPRINT_FACTOR
    rows.append((img["software"], f"{name}:{tag}", compressed, on_disk, BASE_FREE_GIB - on_disk))

free = [r[4] for r in rows]
dynare = next((r for r in rows if r[1].startswith("dynare/")), None)

# Placeholders for the prose ({eval} shows a bare string).
disk_gib = f"{DISK_GIB:.0f}"
overhead_gib = f"{OVERHEAD_GIB:.1f}"
base_free_gib = f"{BASE_FREE_GIB:.0f}"
footprint_factor = f"{FOOTPRINT_FACTOR:g}"
free_min, free_max = f"{math.floor(min(free))}", f"{math.floor(max(free))}"
dynare_on_disk = f"{math.floor(dynare[3])}" if dynare else "n/a"  # "over ..."
dynare_free = f"{math.ceil(dynare[4])}" if dynare else "n/a"  # "less than ..."

# MyST does not render `text/markdown` outputs, so build HTML.
L, R = 'style="text-align:left"', 'style="text-align:right"'
table = (
    "<table>\n<thead><tr>"
    f"<th {L}>Software</th><th {L}>Image</th><th {R}>Download size</th>"
    f"<th {R}>Space it occupies*</th><th {R}>Free space for your package*</th>"
    "</tr></thead>\n<tbody>\n"
)
for software, image_tag, compressed, on_disk, free_gib in rows:
    table += (
        f"<tr><td {L}>{software}</td><td {L}><code>{image_tag}</code></td>"
        f"<td {R}>{compressed:.1f} GiB</td><td {R}>{on_disk:.1f} GiB</td>"
        f"<td {R}>{free_gib:.1f} GiB</td></tr>\n"
    )
table += "</tbody>\n</table>"
size_table = HTML(table)
# ==============================================================
```

The size available to run your code depends on the **software** being used, and how you **manage files** within your replication package. A complete run of your code needs room:

- the operating system
- the statistical software you use
- multiple copies of your replication package:
  - the ZIP file you upload
  - the workspace it is extracted into
- anything your code writes

Current SIVACOR nodes have  between **{eval}`free_min` and {eval}`free_max` GiB** free, depending on the software being used.

::::{admonition} Additional information
:class: dropdown tip

This instance of SIVACOR launches a virtual machine for each run. The machine's filesystem is **{eval}`disk_gib` GiB**, of which about **{eval}`overhead_gib` GiB** is the operating system, Docker and the SIVACOR harness. Roughly **{eval}`base_free_gib` GiB** are available before the analysis software is added. Software sizes differ a great deal, and the software is unpacked onto the same disk your package lives on. 


The table below lists what is left for your package after each one. See
[Available Software](images.md) for the full, curated list.

```{code-cell} python
:tags: ["remove-input"]

size_table
```

\* Estimated from the compressed download size.[^downloadsize] 

[^downloadsize]: The container is kept **both** compressed and
unpacked on the worker's disk, so it occupies roughly **{eval}`footprint_factor`x** what it downloads.

:::{important}

**If your analysis uses MATLAB/Dynare, pay particular attention to the  `dynare` entry.** Images provided by the Dynare project are large, typically over {eval}`dynare_on_disk` GiB. This leaves less than {eval}`dynare_free` GiB for the package and everything it writes. If you run into problems, see how to request 
[extra scratch disk](step2-choosing-image.md#scratch-disk).

:::

::::

For more information on the system itself, see [Hardware capabilities](system.md#hardware-capabilities).


A run is stopped if the worker runs out of disk space,  see the
[FAQ](faq.md#my-job-failed-saying-it-ran-out-of-disk-space). 

If your package cannot be made to fit the free space in the table above, you may be able to ask for
[extra scratch disk](step2-choosing-image.md#scratch-disk).


## Prepare a ZIP or tar.gz file

Your replication package must be a single ZIP file or tar.gz file.

:::{note}

You may find [this checklist](https://aeadataeditor.github.io/aea-de-guidance/preparing-replication-package.html#checklist) on the AEA Data Editor's site useful. 

:::


The next step is to [upload your package to SIVACOR](step1-upload.md).

## ℹ️ FAQ

See the [FAQ](faq.md#preparing-a-package).