FROM index.docker.io/chrismit7/pyquant

LABEL origin="index.docker.io/chrismit7/pyquant:v0.2.2"
LABEL description="Root directories added to support Singularity @ TACC"

RUN mkdir -p /work && chown root:root /work
RUN mkdir -p /gpfs && chown root:root /gpfs
RUN mkdir -p /data && chown root:root /data

ENTRYPOINT []
