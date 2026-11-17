---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Available Software

SIVACOR only allows you to run certain well-defined software environments from known and trusted sources. The tables below list every **Software Environment** and **Version** you can pick in the submission form, with a link to more information about each. (Technically, each environment is a Docker image and each version one of its tags; you do not need to know anything about Docker to use them.) If you believe additional software should be added, file a [pull request](https://github.com/SIVACOR/sivacor-repo-choice/issues/new) at the [sivacor-repo-choice](https://github.com/SIVACOR/sivacor-repo-choice/) repository, and contact us.


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
globals().update({f'df_{software.lower().replace(" ", "_")}': group_df[['Container', 'Tag']].copy().rename(columns={'Container': 'Software Environment', 'Tag': 'Version'}) 
                  for software, group_df in software_data.items()})
```

::::{tab-set}

:::{tab-item} Stata

Stata environments are built by [SSC NG](https://ssc-ng.net/docker-stata/)[^stataimg], with permission from StataCorp. See the [sscng repositories](https://hub.docker.com/u/sscng) for more information. Each environment corresponds to a Stata version, and its versions identify the regular updates within it. Usually, you can use the latest version available. 

```{important} 
Stata environments contain no user-installed packages (`net install`, `ssc install`, etc.). You must provide an installation script that adds any such packages into a project-specific folder,  see [Step 0](#dependencies). 
```

[^stataimg]: These environments were previously created by Lars Vilhuber, AEA Data Editor, and published at <https://hub.docker.com/r/dataeditors/>. Maintenance was transferred to [SSC-NG](https://ssc-ng.net/) in October 2026.

```{code-cell} python
:tags: ["remove-input"]
if 'df_stata' in globals():
    show(df_stata, lengthMenu=[10, 25, 50, -1], classes="display compact", showIndex=False,
         columnDefs=[{"width": "400px", "targets": 0, "className": "dt-left"}, {"width": "150px", "targets": 1, "className": "dt-left"}],
         autoWidth=False)
```

:::

:::{tab-item} R

We use a subset of the environments built by the [rocker project](https://www.rocker-project.org/) for `R`. See the  [rocker repositories](https://hub.docker.com/u/rocker) for more information. Each environment comes with a different combination of pre-installed packages. Any additional packages must be installed, using an appropriate method,  see [Step 0](#dependencies). Versions identify different releases of R.

```{code-cell} python
:tags: ["remove-input"]
if 'df_r' in globals():
    show(df_r, lengthMenu=[10, 25, 50, -1], classes="display compact", showIndex=False,
         columnDefs=[{"width": "400px", "targets": 0, "className": "dt-left"}, {"width": "150px", "targets": 1, "className": "dt-left"}],
         autoWidth=False)
```

:::



:::{tab-item} MATLAB

We use the environments built by  [dynare/dynare](https://hub.docker.com/r/dynare/dynare) for MATLAB, because they contain most MATLAB toolboxes. Only certain versions of MATLAB are supported. You should use these even if you do not use [Dynare](https://www.dynare.org/). Each version identifies a particular combination of Dynare and MATLAB releases. 

```{warning}
MATLAB environments require network isolation to be turned off (`network_isolation: false`) to run, due to the need for a license server.
```

```{code-cell} python
:tags: ["remove-input"]
if 'df_matlab' in globals():
    show(df_matlab, lengthMenu=[10, 25, 50, -1], classes="display compact", showIndex=False,
         columnDefs=[{"width": "400px", "targets": 0, "className": "dt-left"}, {"width": "150px", "targets": 1, "className": "dt-left"}],
         autoWidth=False)
```

:::

:::{tab-item} Julia

We build the Julia environments and publish them at [`ghcr.io/sivacor`](https://github.com/orgs/SIVACOR/packages).
They differ only minimally from the [official Julia images](https://github.com/docker-library/julia), see  [`SIVACOR/julia`](https://github.com/SIVACOR/julia). 

Environments are named after the major-minor Julia release — `julia1.10`, `julia1.11` — and each build is a version,
`<julia patch version>-<build date>`. Pick the environment matching the Julia you developed against, and the newest version
within it.


```{important}
Julia environments do not include **any packages**, and SIVACOR does not install them for you. If your code needs packages, ship a `Project.toml` (and ideally a `Manifest.toml`) and add a first step that installs them — for example a `setup.jl` running `using Pkg; Pkg.instantiate()`, with network isolation turned off for that step only. See [Step 0](#dependencies).
```

```{code-cell} python
:tags: ["remove-input"]
if 'df_julia' in globals():
    show(df_julia, lengthMenu=[10, 25, 50, -1], classes="display compact", showIndex=False,
         columnDefs=[{"width": "400px", "targets": 0, "className": "dt-left"}, {"width": "150px", "targets": 1, "className": "dt-left"}],
         autoWidth=False)
```

:::

::::
