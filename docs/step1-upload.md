---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Uploading Packages to SIVACOR

```{code-cell} python
:tags: ["remove-input", "remove-output"]

import csv
from pathlib import Path

node = next(n for n in csv.DictReader(Path("_data/jetstream2-nodes.csv").open()) if n["default"] == "true")
upload_max_gb = node["upload_max_gb"]
user_quota_gb = node["user_quota_gb"]
```

## Logging In

The main submission site is <https://submit.sivacor.org>.

![Login page](images/sivacor-login.png)

SIVACOR uses institutional logins via [Globus](https://globus.org/).

::::{tab-set}


:::{tab-item} Globus Login

Click on the "Login with Globus" button. You can search for your institution, or use one of the other login methods. You will be redirected to your institution's login page. After entering your credentials, you will be redirected back to SIVACOR.

![Globus login page](images/sivacor-login-globus.png)

:::
::::

## Uploading a Package

Once logged in, you will see the upload page.

![Upload page](images/sivacor-upload-page.png)

Upload the replication package (`ZIP` or `tar.gz` files). You can either click to choose a
file, or drag it onto the upload area. A single archive may be at most **{eval}`upload_max_gb` GB**, and each
user may store up to **{eval}`user_quota_gb` GB** on SIVACOR at any one time.

![Successful upload](images/sivacor-upload-successful.png)

:::{hint}

If you picked the wrong file, click `Delete Uploaded File` and upload the correct one. The
upload area reappears once the file has been removed.

:::

Until an upload has finished, `Run Replication Workflow` at the bottom of the page stays grey
and says why. It goes grey again if you delete the uploaded file, so a run can never be started
against a file that is half-uploaded or no longer there.

![The run button before anything is uploaded](images/sivacor-run-disabled.png)


## ℹ️ FAQ

See the [FAQ](faq.md#types-of-archives) if you experience difficulty uploading. 