#!/usr/bin/env bash

_CONTAINER_ENGINE=docker
CONTAINER_IMAGE="index.docker.io/sd2e/kallisto:0.43.1--hdf51.8.17_0"

. _util/container_exec.sh

threads=3

container_exec ${CONTAINER_IMAGE} kallisto index -i local.test/transcript.idx local.test/transcripts.fasta.gz
container_exec ${CONTAINER_IMAGE} kallisto quant -i local.test/transcript.idx -t ${threads} -b 100 --seed=42 -o local.output local.test/reads_1.fastq.gz local.test/reads_2.fastq.gz


function run_tests() {

    set -x
    validate_ids
    set +x
}

function validate_ids() {

    COUNTIDS=$(grep -c -e "N[MR]_" local.output/abundance.tsv)
    if [ $COUNTIDS == 15 ]
    then
        return 0
    else
        return 1
    fi

}

run_tests && echo "Success" && rm -rf local.output
