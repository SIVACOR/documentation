(tutorial-stata-packages)=
# Tutorial: Including Stata Packages

:::{seealso} Derived from [AEA Data Editor guidance](https://aeadataeditor.github.io/aea-de-guidance/preparing-replication-package-step3)
:class: dropdown

Additional sources are  [Self Checking Reproducibility](https://larsvilhuber.github.io/self-checking-reproducibility/12-environments-in-stata.html) and [Julian Reif's Stata Coding Guide](https://julianreif.com/guide/).
:::

## Stata packages

Stata users frequently use user-written packages, which are made available to the Stata community via the [Stata Journal](https://www.stata-journal.com/), [SSC](https://ideas.repec.org/s/boc/bocode.html), or Github. They are typically installed using a small number of variants of the `net install` command (including `ssc install`).

We will first provide guidance on how to install Stata packages into a project, permanently, for the duration of the project until it is turned into a replication package. We then outline an alternate approach, similar to the way that R (CRAN) or Python (PyPi) handle package management.

## Embedding Stata packages into a project

:::{important} All code goes into a master do file.

The modifications below to `sysdir` and `adopath` must be run before any other runs in the same project, as they are intentially not permanent. Either include the lines in your `main.do`, or include a `pathconfig.do` or similar in your various do-files.

```stata
include "$rootdir/pathconfig.do"
```
:::

### **Define the environment** 

An environment will constrain where Stata installs (`sysdir PLUS`) and seeks (`adopath`) for `ado` files.

In your **main file**, after setting a `$rootdir`:



```stata
/* install any packages locally */
di "=== Redirecting where Stata searches for ado files ==="
capture mkdir "$rootdir/ado"
adopath - PERSONAL
adopath - OLDPLACE
adopath - SITE
sysdir set PLUS     "$rootdir/ado/plus"
sysdir set PERSONAL "$rootdir/ado"       // may be needed for some packages
sysdir                                   // display current settings
```

All installed packages will now be installed into the project-specific `$rootdir/ado`, and Stata will look there (and only there) when loading user-contributed packages.

### **Install packages once**

Packages are then installed if not present (f.i., upon first run), but don't reinstall if already present (on subsequent runs).



```stata
*** Add required packages from SSC to this list ***
local ssc_packages ""
    // Example:
    // local ssc_packages "estout boottest"
    //
    display in red "============ Installing packages/commands from SSC ============="
    display in red "== Packages: `ssc_packages'"
    if !missing("`ssc_packages'") {
        foreach pkg in `ssc_packages' {
            capture which `pkg'
            if _rc == 111 {
               dis "Installing `pkg'"
                ssc install `pkg'
            }
            which `pkg'
        }
    }
 ado
```

:::{important} This checks for commands, not package names!
:class: dropdown

If a package contains NO command with the same name as the package, the above check will not detect it, and you may need to install it unconditionally. For instance, the command `eststo` is part of the `estout` package, but cannot be used as a trigger here. You have to mention `estout`.

:::

:::{note} **Some special cases** (usually not necessary)
:class: dropdown

*For some packages, the **package name does not correspond to any command** included.  Example: `moremata` or `grc1leg`. For these packages, the above code does not work. Use this code:


```stata
// examples are moremata, egennmore, blindschemes, etc.
local ssc_unconditional ""
global triggerfile "$rootdir/install_completed.txt"
cap confirm file "$triggerfile"
if _rc != 0 {
/* add unconditionally installed packages */
    display in red "=============== Unconditionally installed packages from SSC ==============="
    display in red "== Packages: `ssc_unconditional'"
    if !missing("`ssc_unconditional'") {
        foreach pkg in `ssc_unconditional' {
            dis "Installing `pkg'"
            cap ssc install `pkg'
        }
    }
     // write out the trigger file
    file open trigger using "$triggerfile", write replace text
    file write trigger "Installation completed on `c(current_date)'" _n
    file close trigger
}
else {
    display in red "Additional packages already installed"
    display in red "== to reset, delete $triggerfile"
}
```


**Packages that are not on SSC**,  including Github and personal websites, cannot (easily) be iterated over, they need custom `net install` commands.  Use this code:


```stata
// If you have packages that need to be unconditionally installed from other sources (not SSC), then list them here.
global triggerfile "$rootdir/install_completed.txt"
cap confirm file "$triggerfile"
if _rc != 0 {
        display in red "Installing additional packages"
    // Example: grc1leg
    net install grc1leg, from("http://www.stata.com/users/vwiggins/")
    // write out the trigger file
    file open trigger using "$triggerfile", write replace text
    file write trigger "Installation completed on `c(current_date)'" _n
    file close trigger
}
else {
    display in red "Additional packages already installed"
    display in red "== to reset, delete $triggerfile"
}
```

In some cases, an **explicit check** might be easy:

```stata
global ebayesloc "$rootdir/ado/plus/e/ebayes.ado"
cap confirm file "$ebayesloc"
if _rc != 0 {
    // Example when net install is not an option
    cap mkdir "$rootdir/ado"
    cap mkdir "$rootdir/ado/plus"
    cap mkdir "$rootdir/ado/plus/e"
    copy http://www.sacarny.com/wp-content/uploads/2015/08/ebayes.ado "$rootdir/ado/plus/e/ebayes.ado"
}
else {
    display in red "Additional packages already installed"
    display in red "== to reset, delete $triggerfile"
}
```
:::

## **Indexing Mata libraries**

When Stata packages include Mata libraries, the (separate) Mata index of such files needs to be updated. This is a very quick operation, and never hurts to include it, after all installs.

```stata
    mata: mata mlib index
```

## **Adding to replication package**

The following files should be included in your replication package:

```bash
code/ado/*
```
