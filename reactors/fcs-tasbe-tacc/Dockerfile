# Pin to a specific major version, not latest
# xenial = 16.0.4 LTS
# trusty = 14.0.4 LTS

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

RUN apt-get -y install liboctave-dev
RUN octave --no-gui --quiet --eval "pkg install -forge io"

RUN mkdir tasbe
RUN cd tasbe
RUN wget https://github.com/jegentile/TASBEFlowAnalytics/archive/master.zip
RUN unzip master.zip
RUN cd /TASBEFlowAnalytics-master && make install

# There may be a better global solution for Octave containers
# but reading from ~/.octaverc is fraught with peril in a container
# as we can't assure that the username or $HOME path will be stable
# across invocations. Alternatives might be to override OCTAVE_SITE_INITFILE
# and point it to /root/.octaverc
#RUN cat /root/.octaverc >> /usr/share/octave/site/m/startup/octaverc && rm -f /root/.octaverc

RUN mkdir -p /opt/scripts

ADD src /opt/scripts

# Print help by default
CMD python /opt/scripts/fc.py --help

RUN chmod a+rx /root && \
    chmod a+r /root/.octaverc

