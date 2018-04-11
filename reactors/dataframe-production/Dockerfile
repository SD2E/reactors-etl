# Pin to a specific major version, not latest
# xenial = 16.0.4 LTS
# trusty = 14.0.4 LTS

#FROM sd2e/base:ubuntu16
From sd2e/apps:python2

RUN apt-get update && \
    apt-get install python python-pip -y && \
    apt-get clean

RUN pip install --upgrade pip
RUN pip install pandas

WORKDIR /root

# Root directories added to support Singularity @ TACC
LABEL description="Root directories added to support Singularity @ TACC"
RUN mkdir -p /work && chown root:root /work
RUN mkdir -p /gpfs && chown root:root /gpfs
RUN mkdir -p /data && chown root:root /data

RUN mkdir -p /opt/scripts/
ADD /src/dataframe-prod.sh /opt/scripts/dataframe-prod.sh
ADD /src/py /opt/py

RUN chmod 777 /opt/scripts/dataframe-prod.sh
RUN chmod 777 /opt/py/*

CMD python --version
