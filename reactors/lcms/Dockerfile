# Pin to a specific major version, not latest
# xenial = 16.0.4 LTS
# trusty = 14.0.4 LTS

FROM ubuntu:xenial

RUN apt-get update
RUN apt-get install python -y
RUN apt-get install python-pip -y
RUN pip install --upgrade pip
RUN pip install pandas
RUN pip install pyteomics
RUN pip install lxml

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

RUN mkdir -p /opt/scripts

ADD src /opt/scripts

CMD /usr/bin/env
