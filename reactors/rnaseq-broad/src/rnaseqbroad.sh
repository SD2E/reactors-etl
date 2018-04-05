#!/bin/bash
set -e
# Handle arguments
if [ ${1}x = x ]; then
   echo READ1 is blank
   exit 1
fi
if [ ${2}x = x ]; then
   echo READ2 is blank
   exit 1
fi
if [ ${3}x = x ]; then
   echo FASTA is blank
   exit 1
fi
if [ ${4}x = x ]; then
   echo GFF is blank
   exit 1
fi

if [ ${5}x = x ]; then
   echo STRANDED is blank, using default.
   STRANDED='reverse'
fi

R1=${1}
R2=${2}
FASTA=${3}
GFF=${4}
STRANDED=${5}
BED=${6}

if [ ${BED}x = x ]; then
   echo BED is blank, creating bed
   bioawk -c fastx '{print $name"\t0\t"length($seq)}' ${FASTA} >> created_bed.bed
   BED=created_bed.bed
fi

# This pattern match will take processed rRNA & trimmed fastq files or unprocessed raw fastq files
PATTERN='^(.*)_R[1-2]_00[1-8]_rna_free_reads.fastq$'
PATTERN2='^(.*)_rrna_free_reads_unmerged_R[1-2].fastq$'
TESTPATTERN='^(.*)_rrna_free_reads_unmerged_R[1-2].40k.fastq$'
PATTERN3='^(.*)_R[1-2]_00[1-8]_paired.fastq$'
SAMPLE=$(basename $R1)
SAMPLEFASTA=$(echo $(basename $FASTA) | cut -f 1 -d '.')
if [[ $SAMPLE =~ $PATTERN ]]
    then
        SAMPLE="${BASH_REMATCH[1]}.$SAMPLEFASTA"
fi
if [[ $SAMPLE =~ $PATTERN2 ]]
    then
        SAMPLE="${BASH_REMATCH[1]}.$SAMPLEFASTA"
fi
if [[ $SAMPLE =~ $TESTPATTERN ]]
    then
        SAMPLE="${BASH_REMATCH[1]}.$SAMPLEFASTA"
fi
if [[ $SAMPLE =~ $PATTERN3 ]]
    then
        SAMPLE="${BASH_REMATCH[1]}.$SAMPLEFASTA"
fi
# If we get the default R2 value of DEFAULT.rna_free_reads, this is an unpaired run
if [ $R2 = "DEFAULT.rna_free_reads" ]; then
    paired=0
    R2=""
fi


function count_logical_cores() {

    local _count_cores=4
    local _uname=$(uname)

    if [ "$_uname" == "Darwin" ]
    then
        _count_cores=$(sysctl -n hw.logicalcpu)
    elif [ "$_uname" == "Linux" ]
    then
        _count_cores=$(grep -c processor /proc/cpuinfo)
    fi

    echo $_count_cores

}

CORES=$(count_logical_cores)

# Create the settings file for use in the python scripts
echo "Running alignment, count, and profile on $SAMPLE"

echo "sample	fasta_file	gff_file	bed_file	R1_fastq_file	R2_fastq_file	temp_path	output_path" > settings.txt
echo "None						./	" >> settings.txt
echo "$SAMPLE	$FASTA	$GFF	$BED	$R1	$R2	./mapping/	./results/" >> settings.txt
mkdir mapping results

# Run the python scripts that steer the ship
python /opt/rnaseq-broad/map_reads.py -settings settings.txt -sample $SAMPLE -cores $CORES
python /opt/rnaseq-broad/count_reads.py -settings settings.txt -sample $SAMPLE -strand_opt $STRANDED -cores $CORES
python /opt/rnaseq-broad/transcription_profile.py -settings settings.txt -sample $SAMPLE -cores $CORES

# Copy the output files we want to keep
mkdir $SAMPLE
cp results/* $SAMPLE/
cp mapping/*sortedByCoord.out.bam $SAMPLE/
mv mapping/*Log.final.out $SAMPLE.star.final.report.out
mv mapping/*Log.out $SAMPLE.star.log.out
grep -hv -f /opt/scripts/terms_skip.txt $SAMPLE/*counts.txt | sort >> $SAMPLE/$SAMPLE.feature.counts.txt
#add tab-delimted headers to output file
echo -e "Name\tCounts" | cat - $SAMPLE/$SAMPLE.feature.counts.txt > /tmp/outf && mv /tmp/outf $SAMPLE/$SAMPLE.feature.counts.txt
# Cleanup
rm -rf $R1 $R2 $FASTA $GFF $BED mapping results *.fastq *.fa *.gff chr*.txt Genome genomeParameters.txt SA SAindex settings.txt
rm -rf test tester.sh runner-template.sh _util *json
