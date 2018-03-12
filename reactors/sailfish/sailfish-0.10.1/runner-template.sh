CONTAINER_IMAGE="index.docker.io/sd2e/sailfish:0.10.1--1"

. _util/container_exec.sh

threads=19

R1=${fastq1}
R2=${fastq2}

#unzips files if necessary
if [[ ${R1} =~ \.gz$ ]]; then
   echo READ1 is gzipped, upzipping
   gunzip ${R1}
   R1=${R1%.gz}
else
   echo READ1 is not gzipped
fi
if [[ ${R2} =~ \.gz$ ]]; then
   echo READ2 is gzipped, upzipping
   gunzip ${R2}
   R2=${R2%.gz}
else
   echo READ2 is not gzipped
fi

echo fastq1 is ${R1}
echo fastq2 is ${R2}

container_exec ${CONTAINER_IMAGE} sailfish index -t ${transcripts} -o ${output}
container_exec ${CONTAINER_IMAGE} sailfish quant ${vbopt} -i ${output} -1 ${R1} -2 ${R2} -o ${output} ${libtype}
