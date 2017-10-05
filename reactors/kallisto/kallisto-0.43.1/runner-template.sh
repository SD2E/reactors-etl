CONTAINER_IMAGE="index.docker.io/sd2e/kallisto:0.43.1--hdf51.8.17_0"

. _util/container_exec.sh

threads=19

container_exec ${CONTAINER_IMAGE} kallisto index -i transcript.idx ${transcripts}
container_exec ${CONTAINER_IMAGE} kallisto quant -i transcript.idx -t ${threads} ${bootstrap} ${seed} ${output} ${fastq1} ${fastq2}
