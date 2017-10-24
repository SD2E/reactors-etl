#!/bin/bash

echo "Running BYTE UNIXbench 5.1.3 ..."

cd /app/byte-unixbench-5.1.3/UnixBench

# SINGULARITY_CONTAINER exists inside 
# container and are a good hallmark for
# whether we are running in that context
if [ ! -z  "$SINGULARITY_CONTAINER" ]  
then
    DEST=$OPWD
else
    DEST=$PWD
fi

# Core count on Centos 6+
CPUS=$(grep -c "^processor" /proc/cpuinfo)
if [ -z "${CPUS}" ]
then
    CPUS=1
else
    CPUS=$(expr $CPUS / 2)
fi

echo "Results will be copied to $DEST"

./Run -c $CPUS -i 5 -q && \
  tar -czf results.tgz results && \
  cp -f results.tgz ${DEST}/

echo "Done"
