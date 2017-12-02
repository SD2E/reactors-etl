#!/usr/bin/env bash

. _util/container_exec.sh

version=$(cat VERSION)
export CONTAINER_IMAGE="sd2e/rnaseq-broad:$version"

#./test/4342744_R1_001_rna_free_reads.fastq \
DEBUG=1 container_exec ${CONTAINER_IMAGE} /opt/scripts/rnaseqbroad.sh \
	./test/4342744_R1_rna_free_reads.fastq \
	./test/4342744_R2_001_rna_free_reads.fastq \
	./test/circuit1.fasta \
	./test/circuit1.gff \
	./test/circuit1.bed \
	reverse


function run_tests() {

	set -x
	check_counts
	check_mapped_reads
	set +x
}


function check_counts() {

	local PROFILEIDS=$(grep -c pMOD ./4342744.circuit1/4342744.circuit1.syn.counts.txt)
	if [ $PROFILEIDS == 5 ]
		then
			return 0
		else
			return 1
	fi

}


function check_mapped_reads() {

	local MAPPED=$(cat ./4342744.circuit1/4342744.circuit1.mapped.reads.txt)
	if [ $MAPPED == 19997 ]
		then
			return 0
		else
			return 1
	fi

}

function cleanup() {

    echo "Cleaning up..."
    rm -rf 4342744*
    rm -f .container_exec.*
}

trap cleanup EXIT
run_tests
if [ $? -eq 0 ]; then
    echo "Success!"
    exit 0
else
    echo "Test failed!"!
    exit 1
fi