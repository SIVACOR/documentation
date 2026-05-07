# Preparing a Compatible Replication Package

### You should not include any data that you are not allowed to share publicly.

While SIVACOR does not publish data or replication packages, and deletes completed jobs after a short period of time, it is not a designated secure computing system.[^data]

[^data]: SIVACOR runs on [JetStream2](https://jetstream-cloud.org/) infrastructure. The [JS2 Acceptable Use and Data Policy](https://docs.jetstream-cloud.org/general/policies/#acceptable-use-of-jetstream2) apply.

### Your replication package should be portable.

Code must run without manual intervention, use a single controller script (e.g., `main.do` or `master.R`), and avoid hard-coded absolute paths. You can only upload the package, not edit it on the site. It should also not have inconsistently used case-sensitive file or directory names. 

:::{tip}

For some guidance on constructing a portable replication package, see [Steps 1-3](https://aeadataeditor.github.io/aea-de-guidance/preparing-replication-package.html#step-1-main-file) at the AEA Data Editor's website. 

:::

### All dependencies must either be included or installed automatically.

If your code uses libraries or packages, you must ensure that they are installed automatically. We strongly encourage packages that use "environments", and packages to manage dependencies.


::::{tab-set}

:::{tab-item} Tips for `R`

Possible approaches include [`renv`](https://rstudio.github.io/renv/) or [`packrat`](https://rstudio.github.io/packrat/). You can also include code at the top of your main R script to install any required packages that are not already installed. All code necessary to manage depenedencies must be part of the replication package, and must run unattended. For instance, if using `renv`, include the `.Rprofile` and ensure that `renv::restore()` is called at the start of your main R script. 

:::

:::{tab-item} Stata

Guidance for portable dependencies for Stata is provided [at Step 3](https://aeadataeditor.github.io/aea-de-guidance/preparing-replication-package.html#step-3-dependencies) of the AEA Data Editor's guidance. See also the World Bank's [`repado`](https://worldbank.github.io/repkit/reference/repado.html).

:::
::::

### Your replication package only uses a single software application.

Each run of SIVACOR only supports a single software application (e.g., Stata, R, Python), as encapsulated by containers. If your replication requires multiple applications, you will need to configure separate runs. However, your package itself can include the code for multiple applications.

::::{note}
:class: dropdown

The single-application requirement means you cannot call one application from another (e.g., call R from Stata). It also is highly inconvenient when iterating between applications frequently. It can, however, be used when a small number of actions are needed in one software application, with the bulk in a main application. For instance, if you use Stata for data preparation, but R for all remaining analysis. 

::::

::::{admonition} Beta functionality: Chaining of runs
:class: dropdown warning

SIVACOR has new functionality that allows to chain multiple runs that use different software containers, without having to re-upload intermediate results. There may be limitations. Please contact us with any questions.

:::: 


### Prepare a ZIP or tar.gz file

Your replication package must be a single ZIP file or tar.gz file.

:::{admonition} Excluding files from final package
:class: dropdown tip

In some cases, you might want to remove files, which are part of your uploaded package, from the final replicated package, because they are subject to redistribution restrictions. 

You can include a file named `.sivacorignore` at the root of your project to exclude files or directories before the final replicated package is created. It follows the same pattern rules as [`.gitignore`](https://git-scm.com/docs/gitignore), so you can use glob patterns, negations, and directory-specific rules.

For example, to exclude a `data/raw/` directory and all `.tmp` files:

```
data/raw/
*.tmp
```

This is useful for stripping large intermediate files, sensitive data, or build artifacts that should not be part of the archived output.

:::


:::{note}

You may find [this checklist](https://aeadataeditor.github.io/aea-de-guidance/preparing-replication-package.html#checklist) on the AEA Data Editor's site useful. 

:::

:::{admonition} Minimal sample code
:class: dropdown tip

- Sample code for Stata (any version), Scenario B: <https://github.com/SIVACOR/sivacor-test-stata>
- Sample code for Stata (any version), Scenario A (`main.do` in a non-root directory): <https://github.com/SIVACOR/sivacor-test-stata/tree/scenario-A>
- Sample code for R (set up for R 4.3.1, tested on R 4.5.1): <https://github.com/SIVACOR/sivacor-test-r>
- Sample code for MATLAB with and without use of Dynare: <https://github.com/SIVACOR/sivacor-test-matlab> (both use the same `dynare/dynare` container).

:::

The next step is to [upload your package to SIVACOR](step1-upload.md).
