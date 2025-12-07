---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Available Images

SIVACOR only allows you to run certain well-defined Docker images from known and trusted sources. The table below shows all available images with their tags and links to their Docker Hub repositories.


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
    else:
        # Capitalize first letter of each part
        parts = image_name.split('/')[-1].split('-')
        software = ' '.join([part.capitalize() for part in parts])

    # Create Docker Hub URL and link
    docker_hub_url = f"https://hub.docker.com/r/{image_name}"
    docker_hub_link = f'<a href="{docker_hub_url}" target="_blank">More info</a>'

    # Add a row for each tag
    for tag in tags:
        rows.append({
            'Software': software,
            'Docker Image': image_name,
            'Tag': str(tag),
            'Link to Docker Hub': docker_hub_link
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
globals().update({f'df_{software.lower().replace(" ", "_")}': group_df[['Docker Image', 'Tag']].copy() 
                  for software, group_df in software_data.items()})
```

::::{tab-set}

:::{tab-item} Stata

Stata images are built by the AEA Data Editor, with permission from StataCorp. See the [dataeditors repositories](https://hub.docker.com/u/dataeditors) for more information.


```{code-cell} python
:tags: ["remove-input"]
if 'df_stata' in globals():
    show(df_stata, lengthMenu=[10, 25, 50, -1], classes="display compact", showIndex=False,
         columnDefs=[{"width": "400px", "targets": 0, "className": "dt-left"}, {"width": "150px", "targets": 1, "className": "dt-left"}],
         autoWidth=False)
```

:::

:::{tab-item} R

We use a subset of images from the [rocker project](https://www.rocker-project.org/) for `R`. See the  [rocker repositories](https://hub.docker.com/u/rocker) for more information.

```{code-cell} python
:tags: ["remove-input"]
if 'df_r' in globals():
    show(df_r, lengthMenu=[10, 25, 50, -1], classes="display compact", showIndex=False,
         columnDefs=[{"width": "400px", "targets": 0, "className": "dt-left"}, {"width": "150px", "targets": 1, "className": "dt-left"}],
         autoWidth=False)
```

:::



:::{tab-item} MATLAB

We use images from  [dynare/dynare](https://hub.docker.com/r/dynare/dynare) for MATLAB, because they contain most toolboxes. Only certain versions of MATLAB are supported. You should use these even if you do not use [Dynare](https://www.dynare.org/).

```{code-cell} python
:tags: ["remove-input"]
if 'df_matlab' in globals():
    show(df_matlab, lengthMenu=[10, 25, 50, -1], classes="display compact", showIndex=False,
         columnDefs=[{"width": "400px", "targets": 0, "className": "dt-left"}, {"width": "150px", "targets": 1, "className": "dt-left"}],
         autoWidth=False)
```

:::

::::
