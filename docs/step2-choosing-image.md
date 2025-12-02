# Choosing Docker Image and Running Jobs

If the upload was successful, scroll down.

![Upload page continued](images/sivacor-image-choice.png)

Choose first a Docker image from the curated list. Variuos `R` and `Stata` images are available. You can also select an image tag, but generally, the latest image should work. 

:::{tip}

If you need a different image, please contact us.

:::

Finally, identify the name of the main file. This is the file that will be executed by SIVACOR. For `R`, this is typically an `R` script (`.R` file). For `Stata`, this is typically a `do` file (`.do` file). 

:::{warning}

Please be sure to use the proper case (`main.do` is not the same as `Main.do`) and include the extension.

:::

Then click on the `Run with...` button.

![Submit job](images/sivacor-image-choice-ready.png)
