#!/usr/bin/env bash 

. _util/container_exec.sh


version=$(cat VERSION)
export CONTAINER_IMAGE="sd2e/rnaseq:$version"

echo the input parameters
echo read1 is ${read1}
echo read2 is ${read2}
echo trim is ${trim}
echo sortmerna is ${sortmerna}
echo minlen is ${minlen}
echo adaptersfile is ${adaptersfile}
echo filterseqs is ${filterseqs}

DEBUG=1 container_exec ${CONTAINER_IMAGE} /opt/scripts/runsortmerna.sh ${read1} ${read2} ${trim} ${adaptersfile} ${minlen} ${sortmerna} ${filterseqs}

