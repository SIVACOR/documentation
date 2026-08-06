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
`network_isolation` and `env_secrets` are optional.

:::{warning}

Secrets imported from a file are placed in the form and sent with the submission, but they
are never stored in your browser, and they are never included in a downloaded
`Workflow definition`. If you share a workflow file that you wrote by hand, remember to
remove any `env_secrets` from it first.

:::


## Submitting jobs

Then click on the `Run Replication Workflow` button.

![Submit job](images/sivacor-image-run-chained.png)
