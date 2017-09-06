FROM sd2e/reactor_ubuntu:latest

RUN wget https://github.com/pachterlab/kallisto/releases/download/v0.43.0/kallisto_linux-v0.43.0.tar.gz && \
    tar -zxvf kallisto_linux-v0.43.0.tar.gz && 
    mv kallisto_linux-v0.43.0 /usr/local

ENV PATH=$PATH:/usr/local/kallisto_linux-v0.43.0

