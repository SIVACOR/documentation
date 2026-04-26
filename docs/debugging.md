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

