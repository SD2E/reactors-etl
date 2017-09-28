# Pin to a specific major version, not latest
# xenial = 16.0.4 LTS
# trusty = 14.0.4 LTS

FROM ubuntu:xenial

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

# Customizing 101
# 
# 1. Try to avoid working in / (unless that's your intent)
# 2. Do ADD and COPY operations as late as possible as 
#    they invalidate the Docker cache on downstream layers
# 3. Import archive files from GitHub using tagged releases
# 4. Clean up your build directories when done
# 5. Put scripts and other assets in relatively standard places
# 6. Don't actually have the default ENTRYPOINT or 
#    CMD do work. Enlist it for debugging instead.

WORKDIR /root

RUN mkdir tasbe && \
    cd tasbe && \
    wget https://github.com/jegentile/TASBEFlowAnalytics/archive/master.zip && \
    unzip master.zip && \
    cd TASBEFlowAnalytics-master && \
    make install && \
    rm -rf master.zip TASBEFlowAnalytics-master 

#RUN cd tasbe
#RUN wget https://github.com/jegentile/TASBEFlowAnalytics/archive/master.zip
#RUN unzip master.zip
#RUN cd /TASBEFlowAnalytics-master && make install

RUN mkdir -p /opt/scripts

ADD src /opt/scripts

#CMD python /opt/scripts/fc.py --octave-method-path /opt/scripts/ --config $CONFIG 
CMD /usr/bin/env
