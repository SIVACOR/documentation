# Preparing a Compatible Replication Package

### You should not include any data that you are not allowed to share publicly.

While SIVACOR does not publish data or replication packages, and deletes completed jobs after a short period of time, it is not a designated secure computing system. 

### Your replication package should be portable.

Code must run without manual intervention, use a single controller script (e.g., `main.do` or `master.R`), and avoid hard-coded absolute paths. You can only upload the package, not edit it on the site. It should also not have inconsistently used case-sensitive file or directory names. 

### All dependencies must either be included or installed automatically.

If your code uses libraries or packages, you must ensure that they are installed automatically. We strongly encourage packages that use "environments", and packages to manage dependencies, such as `renv` for `R`.

### Prepare a ZIP or tar.gz file

Your replication package must be a single ZIP file or tar.gz file. 


:::{note}

You may find [this checklist](https://aeadataeditor.github.io/aea-de-guidance/preparing-replication-package.html#checklist) on the AEA Data Editor's site useful. 

:::

:::{admonition} Minimal sample code
:class: dropdown tip

- Sample code for Stata (any version), Scenario B: <https://github.com/SIVACOR/sivacor-test-stata>
- Sample code for Stata (any version), Scenario A (`main.do` in a non-root directory): <https://github.com/SIVACOR/sivacor-test-stata/tree/scenario-A>
- Sample code for R (set up for R 4.3.1, tested on R 4.5.1): <https://github.com/SIVACOR/sivacor-test-r>

:::

The next step is to [upload your package to SIVACOR](step1-upload.md).