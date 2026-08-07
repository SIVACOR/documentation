# SIVACOR

Scalable Infrastructure for Validation of Computational Social Science Research (SIVACOR) is a pilot site for automated verification of computational social science research. 

The project aims to build a scalable framework that enables users to confirm and demonstrate reproducible analysis. We build on the metadata schema developed within the [TRACE project](https://transparency-certified.github.io/) to build a system that generates a [Trusted Research Object (TRO)](https://transparency-certified.github.io/trace-specification/docs/elements.html#transparency-certified-research-objects-tro).  Researchers use  SIVACOR  to execute their analysis, generating a certified record of successful execution. The certificate assures researchers that their models are likely to run when executed by others, and can use the generated certificate to demonstrate this fact when submitting articles to a journal. 

## Who is this for

Our target audience are social science researchers who ultimately need to publish in a journal that has a data and code verification process in place, but generally do not have the technical expertise to work in containerized environments or larger computational pipelines.


:::{warning}

Contact your journal's data editor to verify if they will accept SIVACOR-certified replication packages.

:::

## How does it work

SIVACOR allows researchers to work in their preferred environments until the last moment, without needing to fully understand Docker or similar technologies. The system  provides a web interface where users can upload a ZIP file containing their code and data, and select from a set of curated computational environments (Docker images). The SIVACOR backend will then automatically create a containerized environment, execute the analysis, and generate a TRO that includes the code, data, execution environment details, and results. This TRO can then be provided to journal editors, replacing the often tedious and manual process of verifying the reproducibility of the submitted research.

:::{note}

SIVACOR is currently in a pilot phase. As such, the system is limited

- to specific curated Docker images (see [Images](images.md) for details)
- to running each submission on a machine with 8 cores and 30 GiB of RAM (an AMD EPYC-Milan Processor), with 60 GB of disk shared between your files and the software image
- to a maximum run time of 7 days

Results are deleted 14 days after submission. See [System Description](system.md) for details.

:::



