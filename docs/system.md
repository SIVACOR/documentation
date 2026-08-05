# System Description

SIVACOR operates through a series of Trusted Research Performances (TRPs) that ensure computational reproducibility. TRPs are standardized, verifiable processes that form the foundation of transparent computational research. For more information about TRPs, see the [TRACE Specification](https://transparency-certified.github.io/trace-specification/docs/trov-vocabulary/).

## Hardware capabilities

:::{warning}

Coming.

:::


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

