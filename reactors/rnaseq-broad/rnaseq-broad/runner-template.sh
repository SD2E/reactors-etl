#!/usr/bin/env bash

. _util/container_exec.sh

version=$(cat ./VERSION)
CONTAINER_IMAGE="sd2e/rnaseq-broad:$version"

R1=${read1}
R2=${read2}
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
BED=${bed}
bioawk -version >> vers
echo ${vers}
if [ ${BED}x = x ]; then
   echo BED is blank, creating bed
   
   bioawk -c fastx '{print $name"\t0\t"length($seq)}' ${fasta}
   bioawk -c fastx '{print $name"\t0\t"length($seq)}' ${fasta} >> created_bed.bed
   BED=created_bed.bed
fi


# ## FIX THIS!
echo "read1 is ${R1}"
echo "read2 is ${R2}"
echo "fasta is ${fasta}"
echo "gff is ${gff}"
echo "bed is ${BED}"
echo "stranded is ${stranded}"

echo DEBUG=1 container_exec ${CONTAINER_IMAGE} /opt/scripts/rnaseqbroad.sh ${R1} ${R2} ${fasta} ${gff} ${BED} ${stranded}
#DEBUG=1 container_exec ${CONTAINER_IMAGE} /opt/scripts/rnaseqbroad.sh ${R1} ${R2} ${fasta} ${gff} ${BED} ${stranded}
