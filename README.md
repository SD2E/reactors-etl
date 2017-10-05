# ETL Components for the SD2 Program Data

This repository holds source code and test materials for developing various ETL components to power data and metdata extraction, transformation, and loading for the DARPA SD2 program. ETL components are developed and operated in TACC's Cloud API platform, which features the Agave and Reactors application runtimes. 

* *[Agave][1]* is platform-as-a-service which is the foundation of several large cyberinfrastructure platforms, including [CyVerse][2] and [DesignSafe[3]. Designed from the ground up to support reproducible, collaborative science, it provides data management and marshalling, full application lifecycle support, identity management and access control, document store functionality, callback-driven programming, and integration with diverse cloud, hpc, and htc resource types. 
* *Reactors* is a REST-based web service that brings _functions-as-a-service_ to analytical computing. This system is in active development and will be integrated into the ETL process after the Q0 working meeting. More information will be available soon about Reactors. 

## Assumptions

1. The software assets powering each application and ETL process are packaged into a versioned Docker container
2. These containers are either derived from SD2E's base images or are constructed to align with operational requirements for the SD2E platform
3. Each application is deployed as either an Agave application or a Reactor (or both). The process for doing so is documented in tutorial materials as well as via the working codes found in this repository.
4. Applications can be used in the TACC Cloud API via an interactive web workspace, inside Jupyter notebooks (SD2E-hosted or 3rd party), within Python scripts and programs using the [AgavePy library][4], or via an [interactive CLI][5]

## Relevant documentation

1. [SD2E API User's Guide][8]
2. [Agave API Developer Docs][1]

## Base images

* [sd2e/base][6] 
    * ubuntu16 (recommended)
    * ubuntu14
    * alpine36
* [sd2e/python2][7] 
    * ubuntu16 (recommended)
    * ubuntu14
    * alpine36

[1] http://agaveapi.tacc.cloud/
[2] https://cyverse.org/
[3] https://www.designsafe-ci.org/
[4] https://pypi.python.org/pypi/agavepy/
[5] https://github.com/SD2E/sd2e-cli/#overview
[6] https://hub.docker.com/r/sd2e/base/
[7] https://hub.docker.com/r/sd2e/python2/
