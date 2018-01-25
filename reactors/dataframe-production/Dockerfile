# Pin to a specific major version, not latest
# xenial = 16.0.4 LTS
# trusty = 14.0.4 LTS

FROM sd2e/base:ubuntu16

RUN apt-get update && \
    apt-get install python python-pip -y && \
    apt-get clean

RUN pip install --upgrade pip
RUN pip install pandas, json, argparse


WORKDIR /root

RUN mkdir -p /opt/scripts

ADD src /opt/scripts

CMD python /opt/scripts/dataframe-prod.py --help
