% Here we use `grid` to add a basic grid structure to the HTML,
% but the formatting column sizes are defined manually in css/footer.css
% see the `grid-template-columns` line.
:::::{grid} 3 3 5 5
:class: outer-grid col-screen

<!-- Project description -->

::::{div}

# SIVACOR 
```


::::

<!-- Spacer between project description and links columns -->

::::{div}
::::

<!-- Link columns -->

% This a _second_ grid embedded within the first one, to create nicer
% responsive design experience. This grid will have a single column on narrow screens,
% and fan out into three columns on wide screens. However, it always remains within
% its parent grid column.
::::{grid} 1 1 3 3

:::{div}

This material is based upon work supported by the National Science Foundation
        under Grants No. 

- [OAC-2209628](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2209628)
- [OAC-2209629](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2209629)
- [OAC-2209630](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2209630)

:::

:::{div}

![](/img/UoI_wordmark.png)
![](/img/Cornell_wordmark.svg)

:::

::::

:::::

