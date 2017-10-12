# Image: sd2e/fcs

FROM sd2e/base:ubuntu16

RUN apt-get update
RUN apt-get install git -y
RUN apt-get install octave -y
RUN apt-get install octave-io -y
RUN apt-get install wget -y
RUN apt-get install build-essential -y
RUN apt-get install python -y
RUN apt-get install python-pip -y
RUN pip install --upgrade pip
RUN pip install oct2py 
RUN apt-get install python-numpy -y
RUN apt-get install python-scipy -y

# Revised installation a bit to install
# in a sub of /opt
#
# Avoid working out of top-level root dirs 
# where possible, as it limits portability
# to container solutions where we have 
# actual root inside the container when
# it is running.

ADD src /opt/src

WORKDIR /opt
RUN wget https://github.com/jegentile/TASBEFlowAnalytics/archive/master.zip
RUN unzip master.zip
RUN cd TASBEFlowAnalytics-master && make install

WORKDIR /root

# Default command should show usage by
# convention emerging among other
# tool builders
CMD python /opt/src/fc.py --help
