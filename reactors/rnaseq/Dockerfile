# Image: sd2e/rnaseq:0.1.0

FROM sd2e/java8:ubuntu16

RUN apt-get update
RUN apt-get install software-properties-common python-software-properties -y
RUN apt-get install perl -y
RUN apt-get install gzip -y
RUN apt-get install libgomp1 -y

## Install Oracle's JDK
#RUN echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 select true" | debconf-set-selections
#RUN echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu xenial main" > /etc/apt/sources.list.d/webupd8team-java-trusty.list
#RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys EEA14886
#RUN apt-get update && \
#  apt-get install -y --no-install-recommends oracle-java8-installer && \
#  apt-get clean all
#RUN apt install oracle-java8-set-default

RUN mkdir /opt/scripts

ADD /src/runsortmerna /opt/scripts/runsortmerna.sh
ADD /src/sortmerna-2.1b /opt/sortmerna-2.1b
ADD /src/Trimmomatic-0.36 /opt/Trimmomatic-0.36

CMD /opt/scripts/runsortmerna.sh

