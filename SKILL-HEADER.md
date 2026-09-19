---
name: sivacor-submission
description: Guide a researcher through submitting a replication package to SIVACOR (https://submit.sivacor.org) for automated, certified verification — preparing a portable ZIP/tar.gz with all dependencies, uploading it, choosing the software image and main file, monitoring the run, and downloading the signed Replicated Package. Use when someone mentions SIVACOR, TRACE certification, or a Trusted Research Object (TRO), or asks how to get a Stata, R, MATLAB/Dynare, Julia or Python replication package verified before submitting to a journal.
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

## How to use this skill

When helping a researcher, work through the five steps below in order. Most problems come from
Step 0: the package must be portable, run without any human interaction, install its own
dependencies, use a single software application per step, and fit the disk. Check those before
anything else. Do not invent software images or versions — only the curated list on the website is
accepted, and the submission form refuses anything else.

The steps are:

0. Preparing a compatible replication package
1. Uploading the package to SIVACOR
2. Choosing software and running jobs
3. Monitoring job status
4. Downloading results

The text uses [MyST](https://mystmd.org) Markdown: blocks fenced by `:::{tip}`, `:::{warning}`,
`:::{important}` and similar are call-outs; `:::{tab-item} R` and its siblings are alternatives
for different software, only one of which applies to a given package.
