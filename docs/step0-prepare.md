# Preparing a Compatible Replication Package

### You should not include any data that you are not allowed to upload to third-party systems

While SIVACOR does not publish data or replication packages, and deletes completed jobs after a short period of time, it is not a designated secure computing system.[^data] You should not upload *controlled* data, and all uploads should be compatible with any data use agreement you signed. 

[^data]: SIVACOR runs on [JetStream2](https://jetstream-cloud.org/) infrastructure. The [JS2 Acceptable Use and Data Policy](https://docs.jetstream-cloud.org/general/policies/#acceptable-use-of-jetstream2) apply.

If you have data that you are allowed to upload, but not publish, see [the next point](#excluding-files-from-final-package) on how to exclude files from the final replication package.



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

Each step of a SIVACOR submission only supports a single software application (e.g., Stata, R, Python), as encapsulated by containers. If your replication requires multiple applications, you will need to configure separate runs. However, your package itself can include the code for multiple applications, and you can chain them together in a highly simplified workflow system at submission, see [instructions in Step 2](step2-choosing-image.md#chained-runs-steps).

::::{note}
:class: dropdown tip

The single-application requirement means you cannot call one application from another (e.g., call R from Stata). It also is highly inconvenient when iterating between applications frequently. It can, however, be used when a small number of actions are needed in one software application, with the bulk in a main application. For instance, if you use Stata for data preparation, but R for all remaining analysis. 

::::





### Prepare a ZIP or tar.gz file

Your replication package must be a single ZIP file or tar.gz file.

:::{note}

You may find [this checklist](https://aeadataeditor.github.io/aea-de-guidance/preparing-replication-package.html#checklist) on the AEA Data Editor's site useful. 

:::


The next step is to [upload your package to SIVACOR](step1-upload.md).
