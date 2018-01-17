# Data analysis on mapped reads for RNASeq

The entrypoint for these analysis scripts is a tab delimited settings file. This file is created upon runtime from the parameters as determined from the command line.
Three commands guide the entire script, each creating output data files.
* The first script map_reads.py performs the mapping with STAR and generates the coordinate sorted bam file.
* The second script count_reads.py uses HTSeq to count the uniquely mapping reads and creates the *.counts.txt files. The number of these count files is dependent on the number of feature types in the third column of the '.gff' file.
* The third script transcription_profile.py creates the *fwd.profiles.txt and *rev.profiles.txt files containing the per-basepair coverage transcription profile. The region for which to generate this profile is specific in the '.bed' file.

### map_reads.py
Input:

`-settings` settings.txt

`-samples` SAMPLENAME specified from the input json and some string manipulation

`-cores` integer determined by the driver shell script
       
Output files:
       
A coordinate sorted bam file. http://www.htslib.org/doc/samtools.html

### count_reads.py
Input:

`-settings` settings.txt

`-samples` SAMPLENAME specified from the input json and some string manipulation

`-attribute` default to 'name', corresponds to the left-handed assignment in the 9th column in the '.gff' file 

`-strand_opt` default to 'reverse', means a stranded protocol was used for RNAseq

`-cores` integer determined by the driver shell script

Output files:

The number of output files depends on the number of unique attributes in the third column of the '.gff' file. A file contains counts for one attribute type. Each output file follows the same format:

The first column contains the name of the attribute, this name is taken from the righthand of the 9th column.
The second column contains the number of read counts found for an named attribute.

### transcription_profile.py
Input:

`-settings` settings.txt

`-samples` SAMPLENAME specified from the input json and some string manipulation

`-cores` integer determined by the driver shell script

Output files:

Two output files are created for the input sample. A forward transcription profile and reverse transcription profile. The first column contains each reference chromosome, second column is the lower bound of the chromosome, third column is the upper bound of the chromosome, fourth column is the evaluated basepair, and the fifth column contains the read counts for the basepair in column 4.
