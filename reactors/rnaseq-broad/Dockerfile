From sd2e/python2:ubuntu16

# Make apt-get secure and up to date
RUN apt-get update
RUN apt-get -y upgrade

# Install packages that are essential for the next installations
RUN apt-get install -y \
	build-essential \
	bzip2 \
	gzip \
	libbz2-dev \
	liblzma-dev \
	libncurses5-dev \
	libncursesw5-dev \
	libz-dev \
	python2.7-dev \
	python-htseq \
	python-matplotlib \
	python-numpy \
	python-pysam \
	wget \
	zip

# Install python packages
RUN pip install dnaplotlib
RUN pip install HTSeq==0.9.1
RUN pip install matplotlib

# Install everyone's favorite NGS tool
RUN wget https://github.com/samtools/samtools/releases/download/1.6/samtools-1.6.tar.bz2
RUN bzip2 -d samtools-1.6.tar.bz2 && tar fx samtools-1.6.tar && cd samtools-1.6 && make && make install
CMD samtools --version

# Install older bedtools (has coverage output format we need)
RUN wget https://launchpad.net/ubuntu/+archive/primary/+files/bedtools_2.17.0.orig.tar.gz
RUN tar zfx /bedtools_2.17.0.orig.tar.gz && cd bedtools-2.17.0 && make
ENV PATH=/bedtools-2.17.0/bin:$PATH

# Install our aligner
RUN wget https://github.com/alexdobin/STAR/archive/2.5.3a.tar.gz
RUN tar xfz 2.5.3a.tar.gz && rm 2.5.3a.tar.gz
ENV PATH=/STAR-2.5.3a/bin/Linux_x86_64_static:$PATH
RUN chmod 777 /STAR-2.5.3a/bin/Linux_x86_64_static/*

# Install R from bioconductor
#RUN apt-get install -y r-base
#RUN echo 'source("http://bioconductor.org/biocLite.R")\nbiocLite("edgeR")' > /tmp/packages.R \
#	&& Rscript /tmp/packages.R

# Root directories added to support Singularity @ TACC
LABEL description="Root directories added to support Singularity @ TACC"
RUN mkdir -p /work && chown root:root /work
RUN mkdir -p /gpfs && chown root:root /gpfs
RUN mkdir -p /data && chown root:root /data

# Test installations
#RUN STAR
#RUN bowtie2 --version
#RUN bedtools --version
#RUN R --version
#RUN python -c "print(help('modules'))"

# Setup working directory and scriptfiles
#RUN mkdir -p /home/work/mapping
#RUN mkdir /home/work/results
#RUN mkdir /home/work/test
RUN mkdir test mapping results
RUN mkdir -p /opt/scripts/
ADD /src/rnaseq-broad /opt/rnaseq-broad
ADD /src/rnaseqbroad.sh /opt/scripts/rnaseqbroad.sh
ADD /src/terms_skip.txt /opt/scripts/terms_skip.txt
RUN chmod 777 /opt/scripts/rnaseqbroad.sh
RUN chmod 777 /opt/rnaseq-broad/*

# Transfer our test data
ADD /rnaseq-broad/test/ /test

# Test python version
CMD python --version
