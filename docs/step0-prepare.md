---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Preparing a Compatible Replication Package

### You should not include any data that you are not allowed to upload to third-party systems

While SIVACOR does not publish data or replication packages, and deletes completed jobs after a short period of time, it is not a designated secure computing system.[^data] You should not upload *controlled* data, and all uploads should be compatible with any data use agreement you signed. 

[^data]: SIVACOR runs on [JetStream2](https://jetstream-cloud.org/) infrastructure. The [JS2 Acceptable Use and Data Policy](https://docs.jetstream-cloud.org/general/policies/#acceptable-use-of-jetstream2) apply.

If you have data that you are allowed to upload, but not publish, see [the next point](#excluding-files-from-final-package) on how to exclude files from the final replication package.



(excluding-files-from-final-package)=
### Excluding files from final package

The final digitally signed replication package contains all data as originally included. If you need to remove files because you do not have redistribution rights, or large intermediate files, you can include a file named `.sivacorignore` (note the leading dot!) at the root of your project to exclude files or directories before the final replicated package is created. It follows the same pattern rules as [`.gitignore`](https://git-scm.com/docs/gitignore), so you can use [glob patterns](https://en.wikipedia.org/wiki/Glob_%28programming%29), negations, and directory-specific rules.


:::{admonition} Example file and usage
:class: dropdown tip

For example, to exclude a `data/raw/` directory and all `.tmp` files, the `.sivacorignore` file would look like this:

```
data/raw/
*.tmp
```

Your replication package then should somewhat like this:

```
data/raw/
  file1.csv
code/
  main.R
  ...
.sivacorignore
```

:::



### Your replication package should be portable.

Code must run **without manual intervention**, use a **single controller script** (e.g., `main.do` or `master.R`), and **avoid hard-coded absolute paths**. You can only upload the package, not edit it on the site. It should also not have inconsistently used **case-sensitive** file or directory names. 

:::{tip}

For some guidance on constructing a portable replication package, see [Steps 1-3](https://aeadataeditor.github.io/aea-de-guidance/preparing-replication-package.html#step-1-main-file) at the AEA Data Editor's website. 

:::

### All dependencies must either be included or installed automatically.

If your code uses libraries or packages, you must ensure that they are **installed automatically** (for Stata, we suggest you include them). We strongly encourage packages that use "environments", and packages to manage dependencies.


::::{tab-set}

:::{tab-item} Tips for `R`

Possible approaches include [`renv`](https://rstudio.github.io/renv/) or [`packrat`](https://rstudio.github.io/packrat/). You can also include code at the top of your main R script to install any required packages that are not already installed. All code necessary to manage depenedencies must be part of the replication package, and must run unattended. For instance, if using `renv`, include the `.Rprofile` and ensure that `renv::restore()` is called at the start of your main R script. 

:::

:::{tab-item} Stata

Guidance for portable dependencies for Stata is provided [at Step 3](https://aeadataeditor.github.io/aea-de-guidance/preparing-replication-package.html#step-3-dependencies) of the AEA Data Editor's guidance. See also the World Bank's [`repado`](https://worldbank.github.io/repkit/reference/repado.html).

:::
::::

:::{admonition} Minimal sample code
:class: dropdown tip

- Sample code for Stata (any version), Scenario B: <https://github.com/SIVACOR/sivacor-test-stata>
- Sample code for Stata (any version), Scenario A (`main.do` in a non-root directory): <https://github.com/SIVACOR/sivacor-test-stata/tree/scenario-A>
- Sample code for R (set up for R 4.3.1, tested on R 4.5.1): <https://github.com/SIVACOR/sivacor-test-r>
- Sample code for MATLAB with and without use of Dynare: <https://github.com/SIVACOR/sivacor-test-matlab> (both use the same `dynare/dynare` container).

:::


### Your replication package only uses a single software application per step

Each step of a SIVACOR submission only supports a single software application (e.g., Stata, R, Python), as encapsulated by containers. If your replication requires multiple applications, you will need to configure separate runs. However, your package itself can include the code for multiple applications, and you can chain them together in a highly simplified workflow system at submission, see [instructions in Step 2](#chained-runs-steps).

::::{admonition} Additional information
:class: dropdown tip

The single-application requirement means you cannot call one application from another (e.g., call R from Stata). It also is highly inconvenient when iterating between applications frequently. It can, however, be used when a small number of actions are needed in one software application, with the bulk in a main application. For instance, if you use Stata for data preparation, but R for all remaining analysis. 

::::

### Size considerations

The size available to run your code depends on the software being used, and how you manage files within your replication package. A complete run of your code needs room for more than one copy of itself:
the archive you upload, the workspace it is extracted into, and anything your code writes all need to be accommodated.

The machine's filesystem is **58 GiB**, of which about **12.7 GiB** is the operating system, Docker
and the SIVACOR harness — so roughly **45 GiB** is available before the analysis software is added.
Software sizes differ a great deal, and the software is unpacked onto the same disk your package lives
on. The table below lists what is left for your package after each one. See
[Available Software](images.md) for the full, curated list.

```{code-cell} python
:tags: ["remove-input"]

import yaml
import requests
from IPython.display import HTML, display

# Everything here is GiB (powers of 1024), which is what `df` on a worker reports.
# Mixing decimal GB with `df` figures was how an earlier version of this table came
# out optimistic in two places at once.
DISK_GIB = 58.0      # the filesystem's own figure on a worker
OVERHEAD_GIB = 12.7  # operating system + Docker + the SIVACOR harness

# Docker Hub reports the *compressed* layer total. What that costs on the worker's
# disk is much more than the unpacked size, because the workers' Docker keeps the
# compressed blobs in its content store *and* materialises a snapshot per layer --
# so a file rewritten by a later layer is stored three times over.
#
# Measured 2026-08-22 on a VM built exactly like a worker, as the free-space delta
# across a cold pull (and confirmed by `docker system df`):
#
#   dynare/dynare:6.1-R2024a   6.16 GiB compressed -> 21.00 GiB on disk  (3.41x)
#   rocker/r-ver:4.6.1         0.34 GiB compressed ->  1.26 GiB on disk  (3.69x)
#
# 3.5 is the measured middle. The previous value, 3, was described here as "a
# deliberately conservative ceiling" but was in fact an under-estimate: it told
# researchers they had more room than they do.
FOOTPRINT_FACTOR = 3.5

# A handful of representative images, not the full curated list (see images.md for that).
SAMPLE_IMAGES = [
    ("rocker/verse", "R"),
    ("rocker/geospatial", "R"),
    ("dynare/dynare", "MATLAB"),
    ("dataeditors/stata19_5-mp-i-python", "Stata"),
    ("dataeditors/stata19-mp", "Stata"),
]

repos_url = "https://raw.githubusercontent.com/SIVACOR/sivacor-repo-choice/main/allowed_repos.yaml"
allowed = yaml.safe_load(requests.get(repos_url).text)

rows = []
for image_name, software in SAMPLE_IMAGES:
    tag = str(allowed[image_name][0])  # first entry is the most recently added tag
    tag_info = requests.get(
        f"https://hub.docker.com/v2/repositories/{image_name}/tags/{tag}/"
    ).json()
    size_bytes = next(
        (img["size"] for img in tag_info["images"] if img["architecture"] == "amd64"),
        tag_info["full_size"],
    )
    compressed_gib = size_bytes / 1024**3
    on_disk_gib = compressed_gib * FOOTPRINT_FACTOR
    rows.append(
        (
            software,
            f"{image_name}:{tag}",
            compressed_gib,
            on_disk_gib,
            DISK_GIB - OVERHEAD_GIB - on_disk_gib,
        )
    )

# MyST does not render `text/markdown` outputs, so emit HTML directly.
L, R = 'style="text-align:left"', 'style="text-align:right"'
table = (
    "<table>\n<thead><tr>"
    f"<th {L}>Software</th><th {L}>Image</th>"
    f"<th {R}>Download size</th>"
    f"<th {R}>Space it occupies*</th>"
    f"<th {R}>Free space for your package*</th>"
    "</tr></thead>\n<tbody>\n"
)
for software, image_tag, compressed_gib, on_disk_gib, free_gib in rows:
    table += (
        f"<tr><td {L}>{software}</td><td {L}><code>{image_tag}</code></td>"
        f"<td {R}>{compressed_gib:.1f} GiB</td>"
        f"<td {R}>{on_disk_gib:.1f} GiB</td>"
        f"<td {R}>{free_gib:.1f} GiB</td></tr>\n"
    )
table += "</tbody>\n</table>"

display(HTML(table))
```

\* Estimated from the compressed download size. The software is kept **both** compressed and
unpacked on the worker's disk, so it occupies roughly **3.5x** what it downloads — measured on a
worker, and the reason these figures are lower than the download sizes suggest. Individual tags differ.

:::{important}

**If your analysis uses MATLAB/Dynare, read the `dynare` row before anything else.** That image alone
occupies over 21 GiB, which leaves under 24 GiB for your package and everything it writes — by far the
tightest combination on the platform, and the one that has actually run out of disk in practice. A
large package plus Dynare frequently will not fit, and
[extra scratch disk](step2-choosing-image.md#scratch-disk) is the way through it.

:::

For more information on the system itself, see [Hardware capabilities](system.md#hardware-capabilities).


If free space runs low, the run is stopped and you will see an error saying the submission
ran out of disk space — see the
[FAQ](faq.md#my-job-failed-saying-it-ran-out-of-disk-space) for what to do about it.

If your package cannot be made to fit the free space in the table above, you can ask for
[extra scratch disk](step2-choosing-image.md#scratch-disk) instead of shrinking it: a temporary disk
on top of the machine's own, granted per account on request.


### Prepare a ZIP or tar.gz file

Your replication package must be a single ZIP file or tar.gz file.

:::{note}

You may find [this checklist](https://aeadataeditor.github.io/aea-de-guidance/preparing-replication-package.html#checklist) on the AEA Data Editor's site useful. 

:::


The next step is to [upload your package to SIVACOR](step1-upload.md).
