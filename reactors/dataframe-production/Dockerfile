# Pin to a specific major version, not latest
# xenial = 16.0.4 LTS
# trusty = 14.0.4 LTS

FROM sd2e/base:ubuntu16

ENV CONFIG_FILENAME=config.json
ENV OUTPUT_FILENAME=output.csv

RUN apt-get update && \
    apt-get install python python-pip -y && \
    apt-get clean

RUN pip install --upgrade pip
RUN pip install pandas


WORKDIR /root

RUN mkdir -p /opt/scripts

ADD src /opt/scripts

VOLUME ["/files"]

CMD python /opt/scripts/dataframe-prod.py --config /files/$CONFIG_FILENAME -o /files/$OUTPUT_FILENAME