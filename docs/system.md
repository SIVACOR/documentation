---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# System Description

```{code-cell} python
:tags: ["remove-input", "remove-output"]

import csv
from pathlib import Path

from IPython.display import HTML

nodes = list(csv.DictReader(Path("_data/jetstream2-nodes.csv").open()))
node = next(n for n in nodes if n["default"] == "true")
disk_gb = node["disk_gb"]
memory_reserve_gib = str(int(node["memory_gib"]) - int(node["memory_available_gib"]))
upload_max_gb = node["upload_max_gb"]
user_quota_gb = node["user_quota_gb"]

L, R = 'style="text-align:left"', 'style="text-align:right"'
table = (
    "<table>\n<thead><tr>"
    f"<th {L}>Size</th><th {L}>Processor</th><th {R}>Available to your analysis</th>"
    f"<th {L}>Disk</th></tr></thead>\n<tbody>\n"
)
for n in nodes:
    disk = f"{n['disk_gb']} GB" + (" (by request)" if n["by_request"] == "true" else "")
    table += (
        f"<tr><td {L}>{n['memory_gib']} GiB</td><td {L}>{n['cores']} cores ({n['processor']})</td>"
        f"<td {R}>≈{n['memory_available_gib']} GiB</td><td {L}>{disk}</td></tr>\n"
    )
table += "</tbody>\n</table>"
size_table = HTML(table)
```

SIVACOR operates through a series of Trusted Research Performances (TRPs) that ensure computational reproducibility. TRPs are standardized, verifiable processes that form the foundation of transparent computational research. For more information about TRPs, see the [TRACE Specification](https://transparency-certified.github.io/trace-specification/docs/trov-vocabulary/).

## Hardware capabilities

Every submission runs on its own virtual machine, created when your job starts and
destroyed when it finishes. Your code is the only thing running on it, and nothing is
carried over from one submission to the next.

**You choose the size** when you submit — see [choosing the machine
size](step2-choosing-image.md#worker-size). New submissions default to the smallest.

```{code-cell} python
:tags: ["remove-input"]

size_table
```

Your analysis gets all of the cores, and all of the memory except a small reserve —
about {eval}`memory_reserve_gib` GiB is held back so that the machine itself, and the agent supervising your
run, cannot be starved by the analysis. That reserve is why each "available" figure is
lower than the size's name, and it is an approximation: the exact limit is reported in
your run's performance data.

An analysis that tries to exceed the limit is stopped, and the job log says so and names
the figure. It is not silently slowed down or swapped to disk.

**Disk is the same at every size.** A larger machine buys memory and cores, never space.

The {eval}`disk_gb` GB of disk is shared between your replication package and the software image it runs
in — see [Package must be able to run on the SIVACOR workers](step0-prepare.md#size-considerations) when preparing your
package.

A submission may additionally be given a **temporary scratch disk**, of a size it asks for, on top of
the machine's own {eval}`disk_gb` GB. It is granted per account on request, created for the one submission and
destroyed with the machine — see [extra scratch disk](step2-choosing-image.md#scratch-disk). Nothing
about the record of your run changes: the files are in the usual working directory and are hashed
into the TRO like any other.

### Limits

- **Run time.** A run is stopped after **7 days**.
- **Sign of life.** A run that reports no activity for **30 minutes** is marked as failed,
  on the assumption that the machine running it has been lost.
- **Retention.** Submissions are deleted **14 days** after they are submitted.
- **Uploads.** A single archive may be at most {eval}`upload_max_gb` GB, and each user may store up to {eval}`user_quota_gb` GB.
- **One at a time.** You can have only one submission in progress at a time.

At busy times, your submission may have to wait for a machine to become available before it
starts. See [Monitoring Jobs](step3-monitoring.md).

## TRS: Trusted Research System

SIVACOR has the following TRS [capabilities](https://transparency-certified.github.io/trace-specification/docs/trov-vocabulary/#predefined-values-trs-capability-types):

:::{warning}

Coming: Needs to be parsed from TRS specification upon rebuild. 

:::

## TRP: Container Execution


:::{warning}

Coming: Uses the terms used in the actual specification.

:::

**Purpose**: Execute computational research within an  container environment.

**Process**:

- Uses a container image from a pre-specified list as the execution environment
- Provisions an execution environment
- Runs the container, using the user-provided ZIP file and entry point.
- Captures execution logs and outputs
- May be called multiple times in a chained execution, with each run updating the project space.

**Inputs**:

- Container image reference from the pre-specified list
- Execution parameters: network isolation, name of entry point
- Resource allocation: the machine size the submission asked for, and any extra scratch disk it was
  granted — one of each per submission


## TRP: Artifact Filtering

**Purpose**: Process and filter research artifacts according to `.sivacorignore` specifications before publication.

**Process**:

- This is always the last step.
- Parses the `.sivacorignore` file from the user-provided ZIP file
- Applies pattern matching to identify files and directories to exclude
- Filters the output artifacts based on the ignore rules
- Preserves the directory structure of remaining files

**Inputs**:

- Project space from all previous TRPs
- `.sivacorignore` configuration file

