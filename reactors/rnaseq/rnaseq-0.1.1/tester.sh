#!/usr/bin/env bash 

. _util/container_exec.sh


version=$(cat VERSION)
export CONTAINER_IMAGE="sd2e/rnaseq:$version"

export read1="4311028_S61_R1_001.fastq.gz"
export read2="4311028_S61_R2_001.fastq.gz"
export rnadb_dir="rRNA_databases"


if [ ${read2}x == x ] ; then export read2=ENOSUCH_R2.fastq.gz;fi
if [ ${trim}x == x ] ; then export trim=1;fi
if [ ${sortmerna}x == x ] ; then export sortmerna=1;fi
if [ ${minlen}x == x ] ; then export minlen=36;fi
if [ ${adaptersfile}x == x ] ; then export adaptersfile="TruSeq3-PE.fa:2:30:10";fi
if [ ${filterseqs}x == x ] ; then export filterseqs="rRNA_databases";fi


# Set up test data
cp -R ../test-data-cache/${read1} . || exit 1
cp -R ../test-data-cache/${read2} . || exit 1
cp -r ../test-data-cache/${filterseqs} . || exit 1

DEBUG=1 container_exec ${CONTAINER_IMAGE} /opt/scripts/runsortmerna.sh ${read1} ${read2} ${trim} ${adaptersfile} ${minlen} ${sortmerna} ${filterseqs}

