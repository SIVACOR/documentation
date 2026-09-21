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
