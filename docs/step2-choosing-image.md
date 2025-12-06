# Choosing Docker Image and Running Jobs

If the upload was successful, scroll down.

![Upload page continued](images/sivacor-image-choice-chained.png)

Choose first a Docker image from the curated list (see [Images](images.md)). You can also select an image tag, but generally, the latest image should work. 

:::{tip}

If you need a different image, please contact us.

:::

Finally, identify the name of the main file. This is the file that will be executed by SIVACOR. For `R`, this is typically an `R` script (`.R` file). For `Stata`, this is typically a `do` file (`.do` file). 

:::{warning}

Please be sure to use the proper case (`main.do` is not the same as `Main.do`) and include the extension.

:::

::::{admonition} Beta functionality: Chained runs
:class: dropdown warning

You can chain multiple runs together, by selecting the `+ ADD STEP` button. The runs will be run in separate containers, but the output of one run will be made available as input to the next run.

![Chaining runs](images/sivacor-image-choice-chained-2.png)

::::

Then click on the `Run with...` button.

![Submit job](images/sivacor-image-run-chained.png)
