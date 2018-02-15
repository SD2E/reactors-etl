This applicaiton takes input fastq files and annotates their 
contents based on a reference fasta file formatted for the
sailfish application. For this applicaiton users must
use a fasta file that is organized by gene. e.g.

```
>gene_1 more info about this gene
ATGTTATCTCTTGTAAAAAGAAGTATTCTTCATTCAATACCAATTACTCG
>gene_2 some info about this gene
ATGTTATCTCTTGTAAAAAGAAGTATTCTTCATTCAATACCAATTACTCG
```
The first word after the ">" will be used as the gene name in the sailfish output files; gene_1, gene_2...

The outputs will be placed in a directory named after the reads sampleID_sailfish and will contain
if successful

* quant.sf: quantification by gene, columns: Name, Length, EffectiveLength, TPM, NumReads.
aux/meta_info.json: shows percent mapped.

More detailed output information about quality control can be found in
[this google doc](https://docs.google.com/spreadsheets/d/1s0O6NWP4H2q0YC7FvTkVvUEr5k5-p-0phBESSx9Gy5s)
