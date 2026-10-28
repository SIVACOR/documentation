---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Assessing Eligibility 

Not every replication package can be run on SIVACOR. This page helps you make that assessment before going forward. 

## Use a single software application per step

Each step of a SIVACOR submission only supports a single software application (Stata, R, MATLAB/Dynare or Julia — see [container images](images.md)). If your replication package requires multiple applications, you will need to configure separate steps. However, your package itself can include the code for multiple applications, and you can chain them together in a highly simplified workflow system at submission, see [instructions in Step 2](#chained-runs-steps).

::::{admonition} Additional information
:class: dropdown seealso

The single-application requirement means you cannot call one application from another (e.g., call R from Stata). If your code iterates frequently between applications, for instance in a loop, it is also not recommended to use this system. It can, however, be used when a small number of actions are needed in one software application, with the bulk in a main application. For instance, if you use Stata for data preparation, but R for all remaining analysis. 

::::

(do-not-include-data-not-allowed)=
## Do not include any data that you are not allowed to upload to third-party systems

While SIVACOR does not publish data or replication packages, and deletes completed jobs after a short period of time, it is not a designated secure computing system.[^data] You should not upload *controlled* data, and all uploads should be compatible with any data use agreement you signed. 

[^data]: SIVACOR runs on [Jetstream2](https://jetstream-cloud.org/) infrastructure. The [JS2 Acceptable Use and Data Policy](https://docs.jetstream-cloud.org/general/policies/#acceptable-use-of-jetstream2) apply. SIVACOR's privacy policy can be found at <https://submit.sivacor.org/privacy>.

If you have data that you are allowed to upload, but not publish, see [next section](temporary-data) and "[Excluding files](#excluding-files-from-final-package)" on how to exclude files from the final replication package.



(temporary-data)=
## Do include data that you can upload but not publish

By default, the final digitally signed replication package (TRO) contains all data as originally uploaded. You should not make manual modifications afterwards, as that will break the integrity of the package (see [Checking Integrity of Your Replication Package](checking-integrity-of-tro)). But you can configure SIVACOR to transparently remove the files for which you do not have redistribution rights. This will be logged as part of the [TRO](https://transparency-certified.github.io/trace-specification/docs/elements.html#transparency-certified-research-objects-tro).





(size-considerations-prep)=
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
disk_gb = node["disk_gb"]
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

- the **operating system**
- the **statistical software** you use
- multiple copies of your **replication package**:
  - the **ZIP file** you upload
  - the **workspace** it is extracted into
- anything your **code writes**

Current SIVACOR nodes have  between **{eval}`free_min` and {eval}`free_max` GiB** free, depending on the software being used.

::::{admonition} Additional planning information
:class: dropdown tip

This instance of SIVACOR launches a virtual machine for each run. Its disk is advertised as {eval}`disk_gb` GB; once formatted the filesystem measures **{eval}`disk_gib` GiB**, which is the figure every number below is in. Of that, about **{eval}`overhead_gib` GiB** is the operating system, Docker and the SIVACOR harness. Roughly **{eval}`base_free_gib` GiB** are available before the analysis software is added. Software sizes differ a great deal, and the software is unpacked onto the same disk your package lives on.


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



The next step is to [prepare your package](step0-prepare.md).

:::{div}
:class: no-checklist
## ℹ️ FAQ
:::

See the [FAQ](faq.md#preparing-a-package).
