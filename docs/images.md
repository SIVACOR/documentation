---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Available Software

SIVACOR only allows you to run certain well-defined software stacks, packaged as Docker images, from known and trusted sources. The table below shows all available software images with their tags and links to their Docker Hub repositories. If you believe additional images should be added, file a [pull request](https://github.com/SIVACOR/sivacor-repo-choice/issues/new) at the [sivacor-repo-choice](https://github.com/SIVACOR/sivacor-repo-choice/) repository, and contact us.


```{code-cell} python
:tags: ["remove-input","full-width"]

import yaml
import pandas as pd
import requests
from IPython.display import HTML, display
from itables import init_notebook_mode, show
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Initialize interactive tables
init_notebook_mode(all_interactive=True)

# Fetch the YAML data
url = "https://raw.githubusercontent.com/SIVACOR/sivacor-repo-choice/main/allowed_repos.yaml"
response = requests.get(url)
data = yaml.safe_load(response.text)

# Process the data into a pandas DataFrame
rows = []
for image_name, tags in data.items():
    # Extract software name from image name
    if 'stata' in image_name.lower():
        software = 'Stata'
    elif 'dynare' in image_name.lower():
        software = 'MATLAB'
    elif image_name.startswith('rocker/'):
        software = 'R'
    elif '/julia' in image_name.lower():
        # One repository per Julia release line -- julia1.10, julia1.11 -- so
        # without this the fallback below would title-case each into a software
        # of its own ("Julia1.10", "Julia1.11") and the table would gain a row
        # group per line. The line belongs in the Container column.
        software = 'Julia'
    else:
        # Capitalize first letter of each part
        parts = image_name.split('/')[-1].split('-')
        software = ' '.join([part.capitalize() for part in parts])

    # Create the registry link. SIVACOR builds its own Julia images and
    # publishes them to GitHub Container Registry, so a hub.docker.com URL would
    # be a dead link for those.
    if image_name.startswith('ghcr.io/'):
        info_url = 'https://github.com/orgs/SIVACOR/packages'
    else:
        info_url = f"https://hub.docker.com/r/{image_name}"
    info_link = f'<a href="{info_url}" target="_blank">More info</a>'

    # Add a row for each tag
    for tag in tags:
        rows.append({
            'Software': software,
            'Container': image_name,
            'Tag': str(tag),
            # Not "Link to Docker Hub": SIVACOR's own images live on GHCR,
            # so the column holds two registries now.
            'More info': info_link
        })

# Create DataFrame
df = pd.DataFrame(rows)

# Sort by software name for better organization
df = df.sort_values('Software')

# Store software data for use in MyST tabs below
software_groups = df.groupby('Software')
software_data = {}
for software, group_df in software_groups:
    software_data[software] = group_df

# Export data to global namespace for use in MyST tabs
globals().update({f'df_{software.lower().replace(" ", "_")}': group_df[['Container', 'Tag']].copy().rename(columns={'Container': 'Image'}) 
                  for software, group_df in software_data.items()})
```

::::{tab-set}

:::{tab-item} Stata

Stata images are built by the AEA Data Editor, with permission from StataCorp. See the [dataeditors repositories](https://hub.docker.com/u/dataeditors) for more information. Stata containers define Stata versions, with tags identifying the within-version regular updates. Usually, you can use the latest tag for a specific version.


```{code-cell} python
:tags: ["remove-input"]
if 'df_stata' in globals():
    show(df_stata, lengthMenu=[10, 25, 50, -1], classes="display compact", showIndex=False,
         columnDefs=[{"width": "400px", "targets": 0, "className": "dt-left"}, {"width": "150px", "targets": 1, "className": "dt-left"}],
         autoWidth=False)
```

:::

:::{tab-item} R

We use a subset of images from the [rocker project](https://www.rocker-project.org/) for `R`. See the  [rocker repositories](https://hub.docker.com/u/rocker) for more information. An image name is defined by a combination of pre-installed packages. Tags identify different versions of R.

```{code-cell} python
:tags: ["remove-input"]
if 'df_r' in globals():
    show(df_r, lengthMenu=[10, 25, 50, -1], classes="display compact", showIndex=False,
         columnDefs=[{"width": "400px", "targets": 0, "className": "dt-left"}, {"width": "150px", "targets": 1, "className": "dt-left"}],
         autoWidth=False)
```

:::



:::{tab-item} MATLAB

We use images from  [dynare/dynare](https://hub.docker.com/r/dynare/dynare) for MATLAB, because they contain most toolboxes. Only certain versions of MATLAB are supported. You should use these even if you do not use [Dynare](https://www.dynare.org/). Tags identify a particular combination of Dynare and MATLAB versions. 

```{code-cell} python
:tags: ["remove-input"]
if 'df_matlab' in globals():
    show(df_matlab, lengthMenu=[10, 25, 50, -1], classes="display compact", showIndex=False,
         columnDefs=[{"width": "400px", "targets": 0, "className": "dt-left"}, {"width": "150px", "targets": 1, "className": "dt-left"}],
         autoWidth=False)
```

:::

:::{tab-item} Julia

Julia is the one stack whose images SIVACOR builds itself, from the
[official Julia image](https://github.com/docker-library/julia). They are published to the GitHub
Container Registry at [`ghcr.io/sivacor`](https://github.com/orgs/SIVACOR/packages) and the source
is [`SIVACOR/julia`](https://github.com/SIVACOR/julia).

There is one repository per Julia release line — `julia1.10`, `julia1.11` — and a tag per build,
`<julia version>-<build date>`. A tag always names the same image: when a new Julia is released, or
when the underlying Debian is rebuilt for a security fix, a **new** tag is published rather than an
existing one replaced. Pick the line matching the Julia you developed against, and the newest tag
within it.

Unlike the other stacks, these images ship **no packages** — only Julia itself and the package
registry. Installing what your code needs is part of your replication package: add a step that
does it, see [Step 0](#dependencies) and [installing packages and network
isolation](#julia-network).

```{code-cell} python
:tags: ["remove-input"]
if 'df_julia' in globals():
    show(df_julia, lengthMenu=[10, 25, 50, -1], classes="display compact", showIndex=False,
         columnDefs=[{"width": "400px", "targets": 0, "className": "dt-left"}, {"width": "150px", "targets": 1, "className": "dt-left"}],
         autoWidth=False)
```

:::

::::
