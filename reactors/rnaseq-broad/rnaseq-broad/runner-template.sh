#!/usr/bin/env bash 

. _util/container_exec.sh

version=$(cat VERSION)
CONTAINER_IMAGE="sd2e/rnaseq-broad:$version"

echo DEBUG=1 container_exec ${CONTAINER_IMAGE} /opt/scripts/rnaseqbroad.sh ${read1} ${read2} ${fasta} ${gff} ${bed} ${stranded}
DEBUG=1 container_exec ${CONTAINER_IMAGE} /opt/scripts/rnaseqbroad.sh ${read1} ${read2} ${fasta} ${gff} ${bed} ${stranded}
