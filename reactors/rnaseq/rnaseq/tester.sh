#!/usr/bin/env bash 

. _util/container_exec.sh


version=$(cat VERSION)
export CONTAINER_IMAGE="sd2e/rnaseq:$version"

export read1="4311028_S61_R1_001.fastq.gz"
export read2="4311028_S61_R2_001.fastq.gz"
export trim=1
export sortmerna=1
export minlen=36
export adaptersfile="TruSeq3-PE.fa:2:30:10"
export filterseqs="silva-bac-16s-id90.fasta,silva-bac-16s-db:silva-bac-23s-id98.fasta,silva-bac-23s-db:silva-arc-16s-id95.fasta,silva-arc-16s-db:silva-arc-23s-id98.fasta,silva-arc-23s-db:silva-euk-18s-id95.fasta,silva-euk-18s-db:silva-euk-28s-id98.fasta,silva-euk-28s:rfam-5s-database-id98.fasta,rfam-5s-db:rfam-5.8s-database-id98.fasta,rfam-5.8s-db"

echo read1 is ${read1}
echo read2 is ${read2}


# Set up test data
cp -R ../test-data-cache/${read1} . || exit 1
cp -R ../test-data-cache/${read2} . || exit 1


echo DEBUG=1 container_exec ${CONTAINER_IMAGE} /opt/scripts/runsortmerna.sh ${read1} ${read2} ${trim} ${adaptersfile} ${minlen} ${sortmerna} ${filterseqs}
DEBUG=1 container_exec ${CONTAINER_IMAGE} /opt/scripts/runsortmerna.sh ${read1} ${read2} ${trim} ${adaptersfile} ${minlen} ${sortmerna} ${filterseqs}

