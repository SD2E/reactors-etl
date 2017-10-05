FROM quay.io/biocontainers/kallisto:0.43.1--hdf51.8.17_0

LABEL origin="quay.io/biocontainers/kallisto:0.43.1--hdf51.8.17_0"
LABEL description="Root directories added to support Singularity @ TACC"

RUN mkdir -p /work && chown root:root /work
RUN mkdir -p /gpfs && chown root:root /gpfs
RUN mkdir -p /data && chown root:root /data
