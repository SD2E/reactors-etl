CONTAINER_IMAGE="index.docker.io/sd2e/sailfish:0.10.1--1"

. _util/container_exec.sh

threads=19

container_exec ${CONTAINER_IMAGE} sailfish index -t ${transcripts} -o ${output}
container_exec ${CONTAINER_IMAGE} sailfish quant ${vbopt} -i ${output} -1 ${fastq1} -2 ${fastq2} -o ${output} ${libtype}
