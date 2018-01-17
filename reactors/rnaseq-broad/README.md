#RNASeq Mapping & Counts reactor

This RNAseq application takes the output of the RNASeq reactor and processes the reads into three data files.

* `STAR` (HISAT2) maps reads to a reference genome with default mapping parameters. Creates a coordinate sorted binary .sam file.
* `Samtools | bedtools` generate the per-base coverage profile of sequence alignments across regions specified in the '.bed' file
* `HTSeq-count` quantifies uniquely mapping reads and provides integer counts for feature types specified in the '.gff' file

Input requirements for this reactor are specified in the job.json file:

* the R1 fastq file after pre-processing (e.g. trimming and/or rRNA filter)
* the R2 fastq file after pre-processing (optional)
* fasta file containing the reference genome of the host organism and synthetic constructs
* gff file containing the reference genome feature details and sythnetic construct feature details
* bed file with regions of the genome and synthetic constructs to create a transcriptional profile for
* Yes or No flag of whether a stranded RNA seq protocol was used (optional, default Yes)

Deposit location of reference '.fasta', '.gff', '.bed' are to be determined.

Cores for parallelization are determiend upon runtime & submission machine and passed at runtime to python for each step of the pipeline.

Output data files are stored in a directory named following a convention in src/rnaseqbroad.sh roughly looking like "Sample.reference/", outside this directory are various log files from agave, STAR, docker.
