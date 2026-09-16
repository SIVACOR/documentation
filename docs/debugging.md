# Debugging hints

## Stata

### Unknown commands

Some commands that exist in the Windows or MacOS version of Stata, and do exist in the graphical Linux version, do not exist in the command line version. If you get such an error (and it is NOT related to the missing installation of an SSC or Stata Journal package), use the following:

```stata
net install cli-compat, all replace from("https://raw.githubusercontent.com/aeadataeditor/cli-compat-stata/master")
```

Do not use that code on your own machine, unless you know what you are doing!

## R

### Renv wants packages that do not exist (yet)

Most of the containers used on SIVACOR use a date-based snapshot of CRAN (hosted on PPM). If you installed R on your computer, and then **later** installed packaeg which you captured with `renv`, then you may get inconsistencies. To fix this, you can try this:

```r
# 1. Read the lockfile into an R list
lock <- renv::lockfile_read("renv.lock")

# 2. Extract the package names
pkgs <- names(lock$Packages)

# 3. Install the packages (ignoring the versions in the lockfile)
renv::install(pkgs)
```

### Libraries missing

If some of the R packages require additional system libraries, we currently have no way of supporting that on SIVACOR.


## Julia

(julia-resolve-failed)=
### The job failed before my code ran

A Julia submission resolves its dependencies in a stage of its own, before your main file is
executed. If that stage fails, nothing of yours has run yet and the error is about your
*declaration*, not your code.

**Read `stderr`, not `stdout`.** Julia's package manager writes everything — what it installed,
what it could not resolve — to `stderr`. Your `stdout` will contain only your own output, so a
resolution failure looks like an empty file if you check there first. Both are in the job's
output files, under a `===== Stage N Dependency Resolution =====` heading.

Four things cause this, and the message names which:

- **A package that is not registered.** `ERROR: expected package `Foo [abc12345]` to be
  registered` means exactly what it says — check the spelling and the UUID in your `Project.toml`
  against the [General registry](https://github.com/JuliaRegistries/General).
- **Version bounds nothing can satisfy**, usually a `[compat]` section pinning two packages to
  versions that disagree. Resolving locally with the same Julia version will reproduce it.
- **A package whose build step failed**, often because it needs a system library the image does
  not have. The package's own output says which.
- **A `Manifest.toml` that no longer matches its `Project.toml`.** Regenerate it with
  `julia --project=. -e 'using Pkg; Pkg.resolve()'` and commit both.

### My package works locally but not on SIVACOR

Check the Julia version. The image you selected pins a specific release, and a `Manifest.toml`
generated on a different one may not resolve. Selecting the image matching your local Julia is
usually the fastest fix.

Note also that dependency resolution has the internet and your analysis may not — see
[Step 2](#julia-network). Code
that downloads data at run time fails under network isolation even though the packages installed
fine.
