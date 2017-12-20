# Pin to a specific major version, not latest
# xenial = 16.0.4 LTS
# trusty = 14.0.4 LTS

FROM sd2e/base:ubuntu16

RUN apt-get update && \
    apt-get install python python-pip -y && \
    apt-get clean

RUN pip install --upgrade pip

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

# After much discussion, it seems that a standard is for
# the default code in the container at least return help/usage
CMD python /opt/scripts/df-helper.py --help
