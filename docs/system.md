# System Description

SIVACOR operates through a series of Trusted Research Performances (TRPs) that ensure computational reproducibility. TRPs are standardized, verifiable processes that form the foundation of transparent computational research. For more information about TRPs, see the [TRACE Specification](https://transparency-certified.github.io/trace-specification/docs/trov-vocabulary/).

## Hardware capabilities

Every submission runs on its own virtual machine, created when your job starts and
destroyed when it finishes. Your code is the only thing running on it, and nothing is
carried over from one submission to the next.

| Resource | Available to your submission |
|----------|------------------------------|
| Processor | 8 cores (AMD EPYC-Milan Processor) |
| Memory | 30 GiB |
| Disk | 60 GB |

Your analysis is given the whole machine — SIVACOR does not place additional CPU or
memory limits on the container.

:::{warning}

The 60 GB of disk must hold **both** your replication package (including everything your
code writes) **and** the software image it runs in. Those images are large: the MATLAB /
Dynare image alone is about 15 GB. If free space runs low, the run is stopped and you will
see an error saying the submission ran out of disk space.

:::

### Limits

- **Run time.** A run is stopped after **7 days**.
- **Sign of life.** A run that reports no activity for **30 minutes** is marked as failed,
  on the assumption that the machine running it has been lost.
- **Retention.** Submissions are deleted **14 days** after they are submitted.
- **Uploads.** A single archive may be at most 5 GB, and each user may store up to 10 GB.
- **One at a time.** You can have only one submission in progress at a time.

At busy times, your submission may have to wait for a machine to become available before it
starts. See [Monitoring Jobs](step3-monitoring.md).

## TRS: Trusted Research System

SIVACOR has the following TRS [capabilities](https://transparency-certified.github.io/trace-specification/docs/trov-vocabulary/#predefined-values-trs-capability-types):

:::{warning}

Coming: Needs to be parsed from TRS specification upon rebuild. 

:::

## TRP: Container Execution


:::{warning}

Coming: Uses the terms used in the actual specification.

:::

**Purpose**: Execute computational research within an  container environment.

**Process**:

- Uses a container image from a pre-specified list as the execution environment
- Provisions an execution environment
- Runs the container, using the user-provided ZIP file and entry point.
- Captures execution logs and outputs
- May be called multiple times in a chained execution, with each run updating the project space.

**Inputs**:

- Container image reference from the pre-specified list
- Execution parameters: network isolation, name of entry point
- Resource allocation specifications *(coming)*


## TRP: Artifact Filtering

**Purpose**: Process and filter research artifacts according to `.sivacorignore` specifications before publication.

**Process**:

- This is always the last step.
- Parses the `.sivacorignore` file from the user-provided ZIP file
- Applies pattern matching to identify files and directories to exclude
- Filters the output artifacts based on the ignore rules
- Preserves the directory structure of remaining files

**Inputs**:

- Project space from all previous TRPs
- `.sivacorignore` configuration file

