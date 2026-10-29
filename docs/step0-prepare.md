---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Preparing a Compatible Replication Package

## Use a single software application per step

Each step of a SIVACOR submission only supports a single software application (Stata, R, MATLAB/Dynare or Julia — see [container images](images.md)). For each such step, you need a separate controller script, and  configure separate steps, which you chain  together in a highly simplified workflow system at submission, see [instructions in Step 2](#chained-runs-steps). Your package should include the complete code for multiple applications.

::::{admonition} Additional information
:class: dropdown seealso

The single-application requirement means you cannot call one application from another (e.g., call R from Stata). If your code iterates frequently between applications, for instance in a loop, it is also not recommended to use this system. It can, however, be used when a small number of actions are needed in one software application, with the bulk in a main application. For instance, if you use Stata for data preparation, but R for all remaining analysis. 

::::

## Do not include any data that you are not allowed to upload to third-party systems

As [a reminder](do-not-include-data-not-allowed), do not include data that you are not allowed to **process** on SIVACOR. 



(excluding-files-from-final-package)=
## Excluding files from final package

Identify the files that you cannot publish, due to legal, ethical, or practical reasons. Prepare the `.sivacorignore` (note the leading dot!) file. It must be at the root of your project. This will be logged as part of the [TRO](https://transparency-certified.github.io/trace-specification/docs/elements.html#transparency-certified-research-objects-tro), so it will be clear which files were removed. 

:::{important} Pruning happens **after your code has run**.
:class: dropdown

The last step before the package is signed removes the identified files. An
*ignored* file is present while your code runs. This allows you to read restricted
input data during the run, but  keep it out of the package you publish. 

:::

:::{warning} You should limit removal to files that you are not allowed to publish.
:class: dropdown

A data editor or future reader might not accept the package if you remove files that should and could have been included. 

:::

:::{admonition} Example file and usage
:class: dropdown seealso

See the [tutorial on removing data with `.sivacorignore`](tutorial-removing-data) for an example file and usage.

:::



## Your replication package should be portable.

Code must run **without manual intervention**, use a **single controller script** (e.g., `main.do` or `master.R`) per step, and **omit hard-coded absolute paths**. File and directory paths are  **case-sensitive**, and should use **OS-neutral path separators** (`/`, not `\`). 

:::{seealso}

For some guidance on constructing a portable replication package, see [Steps 1-3](https://aeadataeditor.github.io/aea-de-guidance/preparing-replication-package.html#step-1-main-file) at the AEA Data Editor's website. 

:::

(dependencies)=
## All dependencies must either be included or installed automatically.

If your code uses libraries or packages, you must ensure that they are **installed automatically** (for Stata, we suggest you include them). We strongly encourage packages that use "environments", and packages to manage dependencies.

:::::::{seealso} Details
:class: dropdown

::::::{tab-set}

:::::{tab-item} R

Possible approaches include [`renv`](https://rstudio.github.io/renv/) or [`packrat`](https://rstudio.github.io/packrat/).[^groundhog] You can also include code at the top of your main R script to install any required packages that are not already installed. All code necessary to manage dependencies must be part of the replication package, and must run unattended. For instance, if using `renv`, include the `.Rprofile` and ensure that `renv::restore()` is called at the start of your main R script.

:::{warning} Do not use a hard-coded CRAN mirror
:class: dropdown

Do not define a `CRAN` archive (e.g., `https://cloud.r-project.org`) in your replication package. 
While on your computer, R installations may balk when you don't interactively select a CRAN mirror, the `R` containers have a pre-defined CRAN mirror. See [renv documentation](https://rstudio.github.io/renv/articles/renv.html) for details.

:::

::::{note} Example code
:class: dropdown


```r
install.packages("renv")  # only once
renv::init()               # only once per project
renv::snapshot()           # only once per project, after all packages are installed. You should choose to install all packages detected, then snapshotting.
renv::status()             # to check status
```

This will create a file `renv.lock` in the top-level directory of your project.

**Adding to replication package**

The following files should be included in your replication package:

```bash
.Rprofile
renv.lock
renv/activate.R
renv/settings.json
```

:::{warning} Do not include the entire `renv` directory

In particular not the `renv/library` subdirectory, as it is platform-specific (of no use to other platforms), and can be very large.

:::
::::

[^groundhog]: [`groundhog`](https://cran.r-project.org/web/packages/groundhog/index.html) is another option for managing R package dependencies. However, on Linux, it always recompiles from source, which can take a very long time, and may fail, depending on the system libraries required on the `rocker` images used here.



:::::

:::::{tab-item} Stata

See the [Tutorial for Stata Packages](tutorial-stata-packages) for instructions on how you can include Stata packages reproducibly. Other guidance can be found at  [the AEA Data Editor's site](https://aeadataeditor.github.io/aea-de-guidance/preparing-replication-package.html#step-3-dependencies), the World Bank's [`repado`](https://worldbank.github.io/repkit/reference/repado.html), the [Self Checking Reproducibility tutorial](https://larsvilhuber.github.io/self-checking-reproducibility/12-environments-in-stata.html) and [Julian Reif's Stata Coding Guide](https://julianreif.com/guide/).

Note that even when you include Stata packages, you should provide the script that originally installed them, to demonstrate provenance.

:::::

:::::{tab-item} Julia

Include a `Project.toml` and `Manifest.toml`. 

Declare your dependencies in a `Project.toml`. 
The `Manifest.toml`, if present, will ensure that the code will install and use the same versions. Without it,  `Project.toml` will install latest versions of the dependencies.

Both can be generated by "activating" your project, and then interactively adding your dependencies:

```julia
julia --project=.
julia> ]           # enter the package REPL
(YourProject) pkg> add DataFrames CSV GLM
```

When running, include a `setup.jl` as your first workflow step (suggested), or include it in your main file:

```{code} julia
:filename: setup.jl
using Pkg
Pkg.instantiate()
```


Alternatively, use an `install.jl` to programmatically install your dependencies.

```julia
julia --project=.
julia> include("install.jl")
```

where

```{code} julia
:filename: install.jl
# Install project dependencies
using Pkg
Pkg.add("DataFrames")
Pkg.add("CSV")
Pkg.add("GLM")
```

Include `Project.toml` and `Manifest.toml`, as well as `setup.jl`  or `install.jl` if present,  next to your main file, or at the top of your package. 


:::::
::::::
:::::::

:::{admonition} Minimal sample code
:class: dropdown seealso

- Sample code for Stata (any version), Scenario B: <https://github.com/SIVACOR/sivacor-test-stata>
- Sample code for Stata (any version), Scenario A (`main.do` in a non-root directory): <https://github.com/SIVACOR/sivacor-test-stata/tree/scenario-A>
- Sample code for R (set up for R 4.3.1, tested on R 4.5.1): <https://github.com/SIVACOR/sivacor-test-r>
- Sample code for MATLAB with and without use of Dynare: <https://github.com/SIVACOR/sivacor-test-matlab> (both use the same `dynare/dynare` container).
- Sample code for Julia (any version): <https://github.com/SIVACOR/sivacor-test-julia>


:::


(size-considerations)=
## Package fits on the SIVACOR workers

You have [verified that the replication package fits](size-considerations-prep) within the resource constraints of SIVACOR.
A run is stopped if the worker runs out of disk space,  see the
[FAQ](faq.md#my-job-failed-saying-it-ran-out-of-disk-space). 



## Prepare a ZIP or tar.gz file

Your replication package must be a single ZIP file or tar.gz file.

:::{note}

You may find [this checklist](https://aeadataeditor.github.io/aea-de-guidance/preparing-replication-package.html#checklist) on the AEA Data Editor's site useful. 

:::


The next step is to [upload your package to SIVACOR](step1-upload.md).

:::{div}
:class: no-checklist
## ℹ️ FAQ
:::

See the [FAQ](faq.md#preparing-a-package).
