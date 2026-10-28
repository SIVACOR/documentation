(tutorial-removing-data)=
# Tutorial: Removing Data with `.sivacorignore`


The `.sivacorignore` file follows the same pattern rules as [`.gitignore`](https://git-scm.com/docs/gitignore), so you can use [glob patterns](https://en.wikipedia.org/wiki/Glob_%28programming%29), negations, and directory-specific rules.

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

