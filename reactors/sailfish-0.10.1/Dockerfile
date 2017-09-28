# Source for sd2e/sailfish:0.10.1--1

FROM quay.io/biocontainers/sailfish:0.10.1--1
LABEL origin="quay.io/biocontainers/sailfish:0.10.1--1"
LABEL description="Additional root directories added to support TACC HPC systems under Singularity"

RUN mkdir -p /work && chown root:root /work
RUN mkdir -p /gpfs && chown root:root /gpfs
RUN mkdir -p /data && chown root:root /data
