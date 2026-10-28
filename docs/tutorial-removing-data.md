(tutorial-removing-data)=
# Tutorial: Removing Data with `.sivacorignore`


The `.sivacorignore` file follows the same pattern rules as [`.gitignore`](https://git-scm.com/docs/gitignore), so you can use [glob patterns](https://en.wikipedia.org/wiki/Glob_%28programming%29), negations, and directory-specific rules.

## A simple example

For example, to exclude a `data/raw/` directory and all `.tmp` files, the `.sivacorignore` file would look like this:

```
data/raw/
*.tmp
```

Your replication package then should look somewhat like this:

```
data/raw/
  file1.csv
code/
  main.R
  ...
.sivacorignore
```

before it is run, and might look like this

```
code/
  main.R
output/
  figure.png
  ...
.sivacorignore
```

after the run (note removal of `data/raw`).

## Removing data that are obtained via API

In general, you should provide a copy of the data that you obtain via API, as the API query might yield different results over time. However, if you cannot, then `.sivacorignore` can be used to exclude the API-obtained data from your replication package.

A more elaborate example is provided in [SIVACOR/sivacor-test-remove-files](https://github.com/SIVACOR/sivacor-test-remove-files), which also demonstrates how to not include the API key in the replication package. See [Environment variables](step2-choosing-image.md#environment-secrets) for details.