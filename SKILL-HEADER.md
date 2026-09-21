---
name: sivacor-submission
description: Guide a researcher through submitting a replication package to SIVACOR (https://submit.sivacor.org) for automated, certified verification — preparing a portable ZIP/tar.gz with all dependencies, uploading it, choosing the software image and main file, monitoring the run, and downloading the signed Replicated Package. Use when someone mentions SIVACOR, TRACE certification, or a Trusted Research Object (TRO), or asks how to get a Stata, R, MATLAB/Dynare or Julia replication package verified before submitting to a journal.
---

# Submitting a replication package to SIVACOR

SIVACOR (Scalable Infrastructure for Validation of Computational Social Science Research) runs a
researcher's replication package unattended in a curated container, and returns a digitally signed
**Replicated Package** — the original materials, the outputs the code produced, and the TRACE files
(TRO Declaration, TRS Signature, Trusted Timestamp) that prove the run happened on SIVACOR. The
signed package can be handed to a journal's data editor in place of a manual verification.

This file is generated automatically from the user guide at {{SITE_URL}} (built {{BUILD_DATE}}) and
is the whole submission workflow in one place. The website has the same text with screenshots,
plus an [FAQ]({{SITE_URL}}/docs/faq), a [debugging guide]({{SITE_URL}}/docs/debugging) and the
[list of available software images]({{SITE_URL}}/docs/images).

## What SIVACOR will and will not run

Read this before advising anything. SIVACOR recognises **four** families of container image, and
infers how to run the main file from the image, **never from the file's extension**:

| Software | Images | How the main file is run |
|---|---|---|
| R | `rocker/*` | `R --no-save --no-restore -f MAIN_FILE` |
| Stata | `dataeditors/stata*` | `stata-mp -b do MAIN_FILE` |
| MATLAB / Dynare | `dynare/dynare` | `matlab -batch MAIN_FILE` (the `.m` is stripped for you) |
| Julia | `ghcr.io/sivacor/julia*` | `julia --startup-file=no --project=@. MAIN_FILE` |

**There is no Python image, and no way to run a `.py` file as a main file.** The Stata
`*-i-python` images embed Python for use *from* Stata; they are still run by Stata. Anything
outside the four families above is refused at submission. Do not invent images, tags or stacks —
only the curated list at {{SITE_URL}}/docs/images is accepted, and the form refuses the rest.

## How to use this skill

When helping a researcher, work through the five steps below in order. Most problems come from
Step 0: the package must be portable, run without any human interaction, install its own
dependencies, use a single software application per step, and fit the disk. Check those before
anything else.

The steps are:

0. Preparing a compatible replication package
1. Uploading the package to SIVACOR
2. Choosing software and running jobs
3. Monitoring job status
4. Downloading results

### Checking a package before it is submitted

If the package is available locally, inspect it rather than asking the researcher to self-report.
A run takes minutes and only one may be in flight at a time, so each of these is worth more than a
failed attempt:

- **Absolute paths and working-directory changes.** Search for `setwd(`, `cd "/`, `C:\`,
  `/Users/`, `/home/`, `global root` and similar. Paths must be relative and use `/`.
- **The main file exists, exactly once, with that exact case.** SIVACOR searches the whole package
  for the name you give it. Zero matches and more than one match both fail the run — see
  "[Identify the main file](#step2-choosing-image)".
- **Dependencies bootstrap themselves.** `renv::restore()`, a `Pkg.instantiate()` setup stage, or
  `ssc install`/`net install` lines for Stata. Nothing may wait for a human.
- **No `CRAN` mirror is pinned** in R packages — the `rocker` images already define one.
- **Interactive calls.** `View()`, `browser()`, `readline()`, `pause`, `input(`, `keyboard` all
  hang a container that has no terminal.
- **Size.** Compare the unpacked package plus everything the code writes against the free-space
  figure for the chosen image in "[Package must be able to fit](#step0-prepare)". The image is
  unpacked onto the same disk.
- **Files that must not be redistributed**, which belong in `.sivacorignore`.

Then offer a workflow definition file the researcher can import instead of filling in the form —
the `stages:` YAML documented under "[Optional chained runs](#chained-runs-steps)".

The text uses [MyST](https://mystmd.org) Markdown: blocks fenced by `:::{hint}`, `:::{warning}`,
`:::{important}` and similar are call-outs. A `::::{tab-set}` holds one `::::{tab-item} R`-style
block per software stack; **they are alternatives, not steps** — read only the one matching the
package in front of you, and do not carry advice from one tab into another.
