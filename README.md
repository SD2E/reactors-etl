# ETL Components for the SD2 Program Data

This repository holds source code and test materials for developing various ETL components to power data and metdata extraction, transformation, and loading for the DARPA SD2 program. ETL components are developed and operated in TACC's Cloud API platform, which features the Agave and Reactors application runtimes. 

* *[Agave][1]* is platform-as-a-service which is the foundation of several large cyberinfrastructure platforms, including [CyVerse][2] and [DesignSafe][3]. Designed from the ground up to support reproducible and collaborative science, it provides data management and marshalling, full application lifecycle support, identity management and access control, document store functionality, callback-driven programming, and integration with diverse cloud, hpc, and htc resource types. 
* *Reactors* is a REST-based web service that brings _functions-as-a-service_ to analytical computing. This system is in active development and will be integrated into the ETL process after the Q0 working meeting. More information will be available soon about Reactors. 

## Assumptions

1. The software assets powering each application and ETL process are packaged into a versioned Docker container
2. These containers are either derived from SD2E's base images or are constructed to align with operational requirements for the SD2E platform
3. Each application is deployed as either an Agave application or a Reactor (or both). The process for doing so is documented in tutorial materials as well as via the working codes found in this repository.
4. Applications can be used in the TACC Cloud API via an interactive web workspace, inside Jupyter notebooks (SD2E-hosted or 3rd party), within Python scripts and programs using the [AgavePy library][4], or via an [interactive CLI][5]

## Requirements

* Docker 17.X.X-ce
* Python 2.7.10+
* Bash 3.2.57+
* Git 2.12+
* jq 1.5+
* A GitHub account
* A Docker Hub account
* An active SD2E account

## Relevant documentation

1. [SD2E API User's Guide][8]
2. [Agave API Developer Docs][1]
3. [SD2 App ETL Example](sd2-app-etl.md)
4. [SD2 App ETL Jupyter Notebook]

## Base images

* [sd2e/base][6] 
    * ubuntu16 (recommended)
    * ubuntu14
    * alpine36
* [sd2e/python2][7] 
    * ubuntu16 (recommended)
    * ubuntu14
* [sd2e/python3][9]
    * ubuntu16 (recommended)
    * ubuntu14

## Best practices for developing containerized app bundles

1. Write a clean Dockerfile so there is no question of source code / version provenance. Minimize image size where possible by removing, e.g. source code tarballs and installation directories.
2. Design a robust, but small and portable test case to package with the app bundle. Make liberal use of error checking in `tester.sh` and `runner_template.sh`.
3. Use only command line arguments when calling the containerized executable (with the `container_exec` function). If the executable requires a configuration file, use a wrapper script inside the container to parse inputs from the command line and generate the appropriate configuration file.
4. Explicitly declare all inputs, and explicitly write all outputs. This includes file name and full path.
5. Package and curate outputs into a user-friendly format. Some use cases may benefit from a tarball of all output files; some use cases may benefit from individual files.
6. Make output file names deterministic and predictable to facilitate scripting and job chaining.
7. Document all expected outputs in the `tester.sh` and `runner-template.sh` wrapper scripts. Where appropriate, validate output and provide helpful error messaging.
8. Share your Docker images and app bundles with the SD2E community to benefit others and elicit feedback.

*Best practices were adapted from the [Computational Genomics Lab][10].*

[1]: http://developer.agaveapi.co/
[2]: https://cyverse.org/
[3]: https://www.designsafe-ci.org/
[4]: https://pypi.python.org/pypi/agavepy/
[5]: https://github.com/SD2E/sd2e-cli/#overview
[6]: https://hub.docker.com/r/sd2e/base/
[7]: https://hub.docker.com/r/sd2e/python2/
[8]: https://sd2e.github.io/api-user-guide/
[9]: https://hub.docker.com/r/sd2e/python3/
[10]: https://toil.readthedocs.io/en/3.12.0/developingWorkflows/developing.html#best-practices-for-dockerizing-toil-workflows
