#!/usr/bin/env bash 

. _util/container_exec.sh


version=$(cat VERSION)
export CONTAINER_IMAGE="sd2e/rnaseq:$version"

echo DEBUG=1 container_exec ${CONTAINER_IMAGE} /opt/scripts/runsortmerna.sh ${read1} ${read2} ${trim} ${adaptersfile} ${minlen} ${sortmerna} ${filterseqs}
DEBUG=1 container_exec ${CONTAINER_IMAGE} /opt/scripts/runsortmerna.sh ${read1} ${read2} ${trim} ${adaptersfile} ${minlen} ${sortmerna} ${filterseqs}

