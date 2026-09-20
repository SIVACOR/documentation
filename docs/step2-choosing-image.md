# Choosing Software and Running Jobs

If the upload was successful, scroll down.

![Upload page continued](images/sivacor-image-choice-chained.png)

## Choose software and version

Choose first the software and version from the curated list (see [container images](images.md)). You can also select an image tag (sub version), but generally, the latest version should work. 

:::{attention}

If you need a different image, please contact us.

:::

## Identify the main file

Finally, identify the name of the main file. This is the file that will be executed by SIVACOR. For `R`, this is typically an `R` script (`.R` file). For `Stata`, this is typically a `do` file (`.do` file). For `Julia`, this is a `.jl` file, and your package must also contain a `Project.toml` — see [Step 0](#dependencies). 

:::{warning}

Please be sure to use the proper case (`main.do` is not the same as `Main.do`) and include the extension.

:::

(julia-network)=
## Julia: dependency resolution happens before your code runs

A Julia submission runs in **two stages**, and this is worth knowing before you choose network
isolation.

1. **Dependency resolution.** SIVACOR reads your `Project.toml`, downloads the packages it names
   and precompiles them. This stage **needs the internet** and always has it, whatever you chose.
   Your own code does not run here — though installing a package can run that package's own build
   script, which is normal for Julia.
2. **Your analysis.** This is where your main file runs, and this is the stage your network
   isolation setting applies to.

So **a Julia submission always reaches the network**, even when you ask for isolation. What the
isolation setting controls — and what the signed Transparent Research Object records — is whether
*your analysis* had network access. The two stages are recorded separately in the TRO for exactly
this reason: the isolation claim is attached to the stage where it is true, and not to the one
where it is not.

The practical consequence: if your code needs to download something at run time, it will still
fail under isolation. Only dependency resolution is exempt.

(chained-runs-steps)=
## Optional chained runs (steps)

You can chain multiple runs together, by selecting the `+ ADD STEP` button. The runs will be run in separate containers. Each run inherits the workspace modified by the previous run, so the output of one run will be made available as input to the next run.

![Chaining runs](images/sivacor-image-choice-chained-2.png)

:::{admonition} Advanced configuration of steps
:class: seealso dropdown

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

:::{danger}

Secrets imported from a file are placed in the form and sent with the submission, but they are never stored in your browser, and they are never included in a downloaded `Workflow definition`. If you share a workflow file that you wrote by hand, remember to remove any `env_secrets` from it first.

:::




(advanced-settings)=
## Advanced settings

Below the steps is an **Advanced** panel. 

![Advanced panel](images/sivacor-advanced-panel.png)

It holds three settings. 

:::{important}

Each setting applies to the **whole** submission.
:::

- [**Worker Size**](#worker-size): the type of machine your submission runs on
- [**Extra Scratch Disk**](#scratch-disk): a temporary disk in addition to the machine's own disk space
- [**Environment Secrets**](#environment-secrets): values passed to your code as environment variables. 


(worker-size)=
## Choose the machine size

Under **Advanced**, **Worker Size** sets the machine your submission runs on. It applies to the
whole submission: every step runs on the same machine.

| Size | Cores | Available to your analysis | Disk | Relative cost |
|---|---|---|---|---|
| 30 GiB | 8 | ≈28 GiB | 60 GB | 1× |
| 60 GiB | 16 | ≈58 GiB | 60 GB | 2× |
| 125 GiB | 32 | ≈123 GiB | 60 GB | 4× — by request |
| 250 GiB | 64 | ≈248 GiB | 60 GB | 8× — by request |

**Submissions default to the smallest size.** Only request more if you know that you need more. The output from a run shows what your last run
actually used, as a share of what it was allowed.

:::{admonition} Where to find run statistics
:class: dropdown hint

![Run statistics](images/sivacor-completed-run-full-highlight.png)
:::

:::{important}

Important points to consider:

- **Disk does not grow with the size.** Every size has the same 60 GB primary disk, shared between your package
  and the software image. If you have run out of *disk*, a bigger machine will not help: ask for
  [extra scratch disk](#scratch-disk) instead. See
  [Step 0](step0-prepare.md#size-considerations).
- **Cores and memory are tied, not chosen separately.** 
- **The usable disk and memory size is always lower than the  name suggests.** A small amount is reserved for the operating system itself. 
- The two **largest sizes are not selectable** by default. They must be requested, see **Requesting additional resources**.
:::


(scratch-disk)=
## Extra scratch disk

**Extra Scratch Disk** asks for a temporary disk *in addition to* the machine's primary 60 GB disk. It is enabled only upon request, see **Requesting additional resources**.

Once your account has a scratch disk allowance:

- enter the number of gigabytes you want for **this** submission, up to your allowance. Requests are rounded **up** to the nearest 10 GB;
- **no changes are needed** for your analysis. Your code sees a single filesystem. 
- the requested number is not preserved from one run to the next - it must be re-entered every time you submit a job.

:::{important}

- **This is disk, not memory.** If a run was stopped for using too much *memory*, pick a larger [machine size](#worker-size) instead.
- **Ask for what you need, not the maximum.** The space comes from a shared pool, and is in competition with any other submissions. If you request a large amount, other submissions asking for space may have to
  wait. 


:::

## Requesting additional resources

To request additional resources, send an email to [support@sivacor.org](mailto:support@sivacor.org). 

:::{admonition} Information requested
:class: dropdown seealso

SIVACOR uses a limited allocation of compute resources. The largest machine sizes cost the project four and eight times the smallest, and additional volumes are similarly limited. We review requests sent to [support@sivacor.org](mailto:support@sivacor.org). Please  say what you are running and why it needs the additional resources. Once your account is authorized to use the larger machine sizes, they become selectable. If authorized to use additional volumes, the field becomes editable.

:::

## Environment variables

You can set environment variables for your job by using the `env_secrets` block in a workflow definition file, or by entering them in the submission form. These variables are available to your code during execution.

![Entering environment variables](images/sivacor-fred-apikey.png)


:::{admonition} Workflow YAML Example
:class: dropdown tip

```yaml
env_secrets:
  - key: API_TOKEN
    value: s3cret
```

:::

## Submitting jobs

Then click on the `Run Replication Workflow` button.

![Submit job](images/sivacor-image-run-chained.png)

:::{hint}
If the  button is greyed out, you may have forgotten to press the `Upload` button. 
:::



## ℹ️ FAQ

See the [FAQ](faq.md#choosing-software-and-running-jobs).
