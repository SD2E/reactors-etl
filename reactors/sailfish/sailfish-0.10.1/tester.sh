CONTAINER_IMAGE="index.docker.io/sd2e/sailfish:0.10.1--1"

. _util/container_exec.sh

threads=3

transcripts=localtest/reference.fasta
fastq1=localtest/reads_1.fastq
fastq2=localtest/reads_2.fastq
bootstrap=100
libtype="-l IU"
output="local.output"

DEBUG=1 container_exec ${CONTAINER_IMAGE} sailfish index -t ${transcripts} -o ${output}
DEBUG=1 container_exec ${CONTAINER_IMAGE} sailfish quant -i ${output} -1 ${fastq1} -2 ${fastq2} -o ${output} ${libtype}

function run_tests() {

    set -x
    if validate_ids
    then
        return 0
    else
        return 1
    fi
    set +x
}

function validate_ids() {

    COUNTIDS=$(grep -c -e "N[MR]_" local.output/quant.sf)
    if [ "$COUNTIDS" == 15 ]
    then
        return 0
    else
        return 1
    fi

}

run_tests && echo "Success" && rm -rf local.output || echo "Failure"

