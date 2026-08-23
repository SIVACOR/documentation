# Choosing Software and Running Jobs

If the upload was successful, scroll down.

![Upload page continued](images/sivacor-image-choice-chained.png)

## Choose software and version

Choose first the software and version from the curated list (see [container images](images.md)). You can also select an image tag (sub version), but generally, the latest version should work. 

:::{tip}

If you need a different image, please contact us.

:::

## Identify the main file

Finally, identify the name of the main file. This is the file that will be executed by SIVACOR. For `R`, this is typically an `R` script (`.R` file). For `Stata`, this is typically a `do` file (`.do` file). 

:::{warning}

Please be sure to use the proper case (`main.do` is not the same as `Main.do`) and include the extension.

:::

(advanced-settings)=
## Advanced settings

Below the steps is an **Advanced** panel, folded by default. Most submissions never need to open
it: everything inside has a sensible default, and the summary line shows what those defaults
currently come to — so you can read the settings without unfolding anything.

![The Advanced panel, opened](images/sivacor-advanced-panel.png)

It holds three settings, each applying to the whole submission rather than to one step:

- **Worker Size** — the machine your submission runs on ([below](#worker-size));
- **Extra Scratch Disk** — a temporary disk on top of the machine's own
  ([below](#scratch-disk));
- **Environment Secrets** — values passed to your code as environment variables. They are sent
  with the submission and never stored in your browser, and they never appear in a downloaded
  `Workflow definition`.

The panel opens itself in two cases, because leaving it shut would hide something you need to
see: when a scratch-disk request cannot be granted, and when you import a workflow file that
sets any of these.

(worker-size)=
## Choose the machine size

Under **Advanced**, **Worker Size** sets the machine your submission runs on. It applies to the
whole submission — every step runs on the same machine, one submission at a time — so there is one
setting, not one per step.

| Size | Cores | Available to your analysis | Disk | Relative cost |
|---|---|---|---|---|
| 30 GiB | 8 | ≈28 GiB | 60 GB | 1× |
| 60 GiB | 16 | ≈58 GiB | 60 GB | 2× |
| 125 GiB | 32 | ≈123 GiB | 60 GB | 4× — by request |
| 250 GiB | 64 | ≈248 GiB | 60 GB | 8× — by request |

**New submissions default to the smallest size.** Most analyses need far less memory than they are
given, so start there and move up only if you need to — the form tells you what your last run
actually used, as a share of what it was allowed, which is usually the fastest way to decide.

:::{important}

Three things about this table are easy to get wrong, and all three cost real time:

- **Disk does not grow with the size.** Every size has the same 60 GB, shared between your package
  and the software image. If you have run out of *disk*, a bigger machine will not help — ask for
  [extra scratch disk](#scratch-disk) instead, and see
  [size considerations](step0-prepare.md#size-considerations).
- **Cores are not chosen separately.** They move with the memory; the numbers above are the whole
  ladder.
- **The usable figure is approximate and is always lower than the size's name.** A small amount is
  held back so the machine itself cannot be starved by your analysis. The exact limit for a run is
  reported in its performance data, and the job log names it if a run exceeds it.

:::

### Sizes marked "by request"

The two largest sizes are visible but not selectable by default. They cost four and eight times the
smallest, so they are granted on request rather than by a click: email
[support@sivacor.org](mailto:support@sivacor.org) and say what you are running and why it needs the
memory. Once you have access, the size becomes selectable and behaves like any other.

If an imported workflow file asks for a size you do not have access to, the import is refused and
tells you which sizes you can use.

(scratch-disk)=
## Extra scratch disk

In the same **Advanced** panel, under the machine size, **Extra Scratch Disk** asks for a temporary
disk *in addition to* the machine's own 60 GB. It is for the small number of packages whose data,
outputs and software image cannot fit that 60 GB together — the case where a run fails saying it ran
out of disk space, and where a larger machine size would not have helped.

**It is off unless you ask, and granted per account.** The field is empty on every new submission —
it is deliberately not remembered from your last one — and for most accounts it is visible but not
selectable, labelled *(by request)*. To ask for it, email
[support@sivacor.org](mailto:support@sivacor.org) and say roughly how much space your package needs.

Once your account has an allowance:

- type the number of gigabytes you want for **this** submission, up to your allowance;
- the form shows what it rounds up to — requests are rounded **up** to the nearest 10 GB, so you
  never get less than you asked for;
- your analysis sees one filesystem, the usual working directory, with that much more room in it;
- the disk is created for your submission and **destroyed when the run finishes**. Nothing on it
  survives; anything you want to keep has to be in the package that gets uploaded back, exactly as
  without it.

:::{important}

- **This is disk, not memory.** If a run was stopped for using too much *memory*, extra scratch disk
  changes nothing — pick a larger [machine size](#worker-size) instead.
- **Ask for what you need, not for your whole allowance.** The space comes from a shared pool, and
  while your submission holds a large amount of it, other submissions asking for space may have to
  wait. The form tells you what your last run's workspace actually peaked at, which is usually the
  right basis for the number.
- **An allowance is per account, and yours is not carried in a workflow file.** A `disk_gb` line in a
  file someone shares with you is *their* allowance; if it exceeds yours, the import is refused and
  names your own limit.

:::

(chained-runs-steps)=
## Optional chained runs (steps)

You can chain multiple runs together, by selecting the `+ ADD STEP` button. The runs will be run in separate containers. Each run inherits the workspace modified by the previous run, so the output of one run will be made available as input to the next run.

![Chaining runs](images/sivacor-image-choice-chained-2.png)

:::{admonition} Advanced configuration of steps
:class: tip dropdown

If you need to repeatedly run similar jobs on SIVACOR, you can describe the steps in a file
and import it instead of filling in the form. Expand **Optional: Import workflow definition**
at the top of the submission form, then choose or drag in a `YAML` or `JSON` file (any file
name, up to 256 KB). The file is checked before anything is filled in, and you will be told
which step is at fault if something is wrong — for example if an image or tag is not one of
the [curated images](images.md).

Importing replaces whatever is currently in the form, so you can always review and adjust
the steps before running.

A finished run offers the matching `Workflow definition` download, so the easiest way to get
a valid file is to run once, download it, and reuse it afterwards.

Expected configuration:

```yaml
stages:
  - image_name: dataeditors/stata15
    image_tag: "2023-01-27"
    main_file: main_step1.do
    network_isolation: true
  - image_name: rocker/tidyverse
    image_tag: "4.6.1"
    main_file: main_step2.R
    network_isolation: false
env_secrets:
  - key: API_TOKEN
    value: s3cret
```

`image_name`, `image_tag` and `main_file` are required for every step;
`network_isolation`, `env_secrets` and `resources` are optional. A file with no `resources`
block leaves the [machine size](#worker-size) as chosen on the form:

```yaml
resources:
  memory_gb: 60
stages:
  - image_name: rocker/tidyverse
    image_tag: "4.6.1"
    main_file: main.R
```

`memory_gb` must be one of the sizes in the table above. A file naming a size that is no longer
offered is refused rather than quietly run on a different machine, and the message names the sizes
that are available.

`resources` may also carry `disk_gb`, for [extra scratch disk](#scratch-disk) — but only if your own
account has an allowance for it. A downloaded `Workflow definition` carries the figure the run was
granted, so a file that came from somebody else may ask for more than you can have; the import is
then refused and names your limit. A run that used no extra disk has no `disk_gb` line at all.

:::{warning}

Secrets imported from a file are placed in the form and sent with the submission, but they
are never stored in your browser, and they are never included in a downloaded
`Workflow definition`. If you share a workflow file that you wrote by hand, remember to
remove any `env_secrets` from it first.

:::


## Submitting jobs

Then click on the `Run Replication Workflow` button.

![Submit job](images/sivacor-image-run-chained.png)

The button is grey until an upload has finished, and says so underneath — while a file is still
going up, and again if you delete the uploaded file. Everything else on the form is checked when
you click: if a step is missing an image, a tag or a main file, the page tells you which one
rather than leaving the button dead.
