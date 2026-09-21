## When a run fails

A failed run still offers the **Run output log** (stdout) and **Run error log** (stderr) for
download — the signed artifacts are offered only on success. Read those logs first; the message
names the file or command at fault. The most common causes, and what to change:

| What you see | What it means | What to do |
|---|---|---|
| `No main.do found` | The main file name does not match anything in the package | Check the exact spelling, case and extension. The file may sit in a subdirectory — that is fine, it is searched for |
| `Multiple main.R files found: ...` | The same file name appears more than once anywhere in the package | Rename or remove the extra copies and upload again — `.sivacorignore` cannot help, it is applied after the run. The message lists every path |
| Out of disk | The package plus the unpacked image exceeded the worker's disk | See [Step 0](#step0-prepare) — a **bigger machine will not help**, its disk is the same. Have the code delete intermediates as it goes (`.sivacorignore` is applied after the run, so it frees nothing during it), or ask for [extra scratch disk](#scratch-disk) |
| Out of memory | The kernel killed the container | Pick a larger [machine size](#worker-size). The container's own log says nothing, because it was killed without warning |
| Stata `r(601)` and similar | Stata could not find a file | Usually an absolute path or a wrong working directory. See the [FAQ]({{SITE_URL}}/docs/faq#stata-errors) |
| `Package Foo not found`, `renv` failures | Dependencies did not install | Isolation is per step: a setup step that installs packages needs **network isolation off**. See the [debugging guide]({{SITE_URL}}/docs/debugging) |
| Image pull failed | The image could not be fetched onto the worker | Re-submit; if it persists, mail support — the image, not the package, is at fault |
| Waiting for a worker, for a long time | No machine free yet | Normal for a few minutes; see the [FAQ]({{SITE_URL}}/docs/faq#monitoring-job-status) |
| Submission abandoned / presumed lost | The worker died mid-run | Not caused by the package. Re-submit; see the [FAQ]({{SITE_URL}}/docs/faq#my-job-failed-with-submission-abandoned) |

## Quick reference

| | |
|---|---|
| Submission site | <https://submit.sivacor.org> (institutional login via Globus) |
| Documentation | <{{SITE_URL}}> |
| Available software images | <{{SITE_URL}}/docs/images> |
| FAQ | <{{SITE_URL}}/docs/faq> |
| Debugging a failed run | <{{SITE_URL}}/docs/debugging> |
| System description | <{{SITE_URL}}/docs/system> |
| Support (also for larger machine sizes and extra scratch disk) | <support@sivacor.org> |
| Feedback | <https://feedback.sivacor.org/> |

### Limits at a glance

- One archive per submission, **ZIP or tar.gz**, at most **{{UPLOAD_MAX_GB}} GB**; **{{USER_QUOTA_GB}} GB** stored per user at any one time.
- **One job at a time** per user.
- Every machine size has the same **{{DISK_GB}} GB** disk, shared between your package and the software image; only the memory and cores change. Extra scratch disk is granted per account on request.
- A submission is **deleted 14 days** after it was submitted, and starting a new run deletes the previous one. Download the Replicated Package first.
- Maximum run time is **7 days**.
- Do not upload data you are not allowed to place on third-party systems; use `.sivacorignore` to keep non-redistributable or bulky files out of the final package.

### Sample packages

- Stata: <https://github.com/SIVACOR/sivacor-test-stata>
- R: <https://github.com/SIVACOR/sivacor-test-r>
- MATLAB / Dynare: <https://github.com/SIVACOR/sivacor-test-matlab>
- Julia: <https://github.com/SIVACOR/sivacor-test-julia>

---

*Generated from the SIVACOR documentation source at <https://github.com/SIVACOR/documentation>
(`docs/step0-prepare.md` through `docs/step4-download.md`) on {{BUILD_DATE}} by
`scripts/build_skill.py`. Edit the source pages, not this file.*
