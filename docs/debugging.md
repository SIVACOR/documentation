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

Most of the containers used on SIVACOR use a date-based snapshot of CRAN (hosted on PPM). If you installed R on your computer, and then **later** installed package which you captured with `renv`, then you may get inconsistencies. To fix this, you can try this:

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
### `using SomePackage` fails, or my setup step did

The Julia images ship no packages. If your code needs them, one of your steps has to install them —
see [Step 0](#dependencies). A missing setup step shows up as Julia's own
`ArgumentError: Package Foo not found in current path`, from your analysis step rather than from
SIVACOR.

If you *have* a setup step and it is the one that failed, the error is about your *declaration*,
not your analysis code.

**Read `stderr`, not `stdout`.** Julia's package manager writes everything — what it installed,
what it could not install — to `stderr`. Your `stdout` will contain only your own output, so an
installation failure looks like an empty file if you check there first. Both are in the job's
output files; each step's output is under its own `===== Stage N Output =====` heading, numbered in
the order you added the steps.

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

Note also that network isolation is per step — see [Step 2](#julia-network). Code that downloads
data at run time fails in an isolated step even though your setup step installed its packages
fine.
