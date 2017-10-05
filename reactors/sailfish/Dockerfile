FROM quay.io/biocontainers/sailfish:0.10.1--1

LABEL origin="quay.io/biocontainers/sailfish:0.10.1--1"

LABEL description="Root directories added to support Singularity @ TACC"
RUN mkdir -p /work && chown root:root /work
RUN mkdir -p /gpfs && chown root:root /gpfs
RUN mkdir -p /data && chown root:root /data
