FROM ubuntu:latest 

ADD src /src

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
RUN pip install --upgrade --force-reinstall octave_kernel
RUN apt-get install python-numpy -y
RUN apt-get install python-scipy -y

RUN wget https://github.com/jegentile/TASBEFlowAnalytics/archive/master.zip
RUN unzip master.zip
RUN cd /TASBEFlowAnalytics-master && make install


CMD python /src/fc.py --config $CONFIG --octave-method-path /src/
