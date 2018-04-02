#!/usr/bin/env bash

. _util/container_exec.sh

version=$(cat ./VERSION)
export CONTAINER_IMAGE="jurrutia/rnaseq-broad:$version"

cp ../test-data-cache/* test/
DEBUG=1 container_exec ${CONTAINER_IMAGE} /opt/scripts/rnaseqbroad.sh \
	./test/4342744_rrna_free_reads_unmerged_R1.fastq \
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

	local PROFILEIDS=$(grep -c pMOD ./4342744.circuit1/4342744.circuit1.feature.counts.txt)
	if [ "$PROFILEIDS" -eq 5 ]
		then
			return 0
		else
			return 1
	fi

}


function check_mapped_reads() {

	local MAPPED=$(cat ./4342744.circuit1/4342744.circuit1.mapped.reads.txt)
	if [ ""$MAPPED" -eq 19997 ]
		then
			return 0
		else
			return 1
	fi

}

function cleanup() {

    echo "Cleaning up..."
    #rm -rf 4342744*
    rm -f .container_exec.*
    rm Log.out
}

trap cleanup EXIT
run_tests
if [ ""$?" -eq 0 ]; then
    echo "Success!"
    exit 0
else
    echo "Test failed!"
    exit 1
fi
