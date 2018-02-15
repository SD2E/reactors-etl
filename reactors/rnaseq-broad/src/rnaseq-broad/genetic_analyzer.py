#!/usr/bin/env python

#	Copyright (C) 2015 by
#	Thomas E. Gorochowski <tom@chofski.co.uk>, Voigt Lab, MIT
#	Alexander Cristofaro <acristof@mit.edu>, Voigt Lab, MIT
#	All rights reserved.
#	OSI Non-Profit Open Software License ("Non-Profit OSL") 3.0 license.

"""
Requires following software is available and in user path:
	- STAR
	- HTSeq
	- BEDTools
	- R + edgeR package
"""


# Required modules
import sys
import csv
import subprocess
import re
import math
import os
import matplotlib
matplotlib.use('Agg')


def bwa_index_filename(settings, sample):
    return settings[sample]['temp_path'] + sample


def sam_filename(settings, sample):
    return settings[sample]['temp_path'] + sample + '.sam'


def bam_filename(settings, sample, extension=True, sorted=False):
    bam_filename = settings[sample]['temp_path'] + sample
    if sorted == True:
        bam_filename += '.Aligned.sortedByCoord.out'
    if extension == True:
        bam_filename += '.bam'
    return bam_filename


def bam_duplicate_name(settings, sample, extension=True):
    bam_duplicate_name = settings[sample]['temp_path'] + sample + '.mdup'
    if extension == True:
        bam_duplicate_name += '.bam'
    return bam_duplicate_name


def fragment_dist_filename(settings, sample):
    return settings[sample]['output_path'] + sample + '.fragment.distribution.txt'


def count_filename(settings, sample, feature):
    return settings[sample]['output_path'] + sample + '.' + feature + '.counts.txt'


def mapped_reads_filename(settings, sample):
    return settings[sample]['output_path'] + sample + '.mapped.reads.txt'


def mapped_reads_matrix_filename(settings):
    return settings['None']['output_path'] + 'mapped.reads.matrix.txt'


def gene_length_filename(settings, sample):
    return settings[sample]['output_path'] + sample + '.feature.lengths.txt'


def profile_filename(settings, sample):
    return settings[sample]['output_path'] + sample + '.profiles.txt'


def profile_fwd_filename(settings, sample):
    return settings[sample]['output_path'] + sample + '.fwd.profiles.txt'


def profile_rev_filename(settings, sample):
    return settings[sample]['output_path'] + sample + '.rev.profiles.txt'


def profile_norm_fwd_filename(settings, sample):
    return settings[sample]['output_path'] + sample + '.fwd.norm.profiles.txt'


def profile_norm_rev_filename(settings, sample):
    return settings[sample]['output_path'] + sample + '.rev.norm.profiles.txt'


def count_matrix_filename(settings):
    return settings['None']['output_path'] + 'counts.matrix.txt'


def normed_counts_filename(settings):
    return settings['None']['output_path'] + 'fpkm.normed.matrix.txt'


def gene_length_matrix_filename(settings):
    return settings['None']['output_path'] + 'gene.lengths.matrix.txt'


def promoter_profile_perf_filename(settings, sample):
    return settings[sample]['output_path'] + sample + '.promoter.profile.perf.txt'


def terminator_profile_perf_filename(settings, sample):
    return settings[sample]['output_path'] + sample + '.terminator.profile.perf.txt'


def ribozyme_profile_perf_filename(settings, sample):
    return settings[sample]['output_path'] + sample + '.ribozyme.profile.perf.txt'


def combined_promoter_profile_perf_filename(settings):
    return settings['None']['output_path'] + 'promoter.profile.perf.txt'


def combined_terminator_profile_perf_filename(settings):
    return settings['None']['output_path'] + 'terminator.profile.perf.txt'


def combined_ribozyme_profile_perf_filename(settings):
    return settings['None']['output_path'] + 'ribozyme.profile.perf.txt'


def combined_fitted_promoter_perf_filename(settings, output_name):
    return settings['None']['output_path'] + 'fitted.promoter.perf.' + output_name + '.txt'


def promoter_reu_filename(settings, sample):
    """Load promoter reu filename
    Modify /rna-seq/ if the destination of RNA seq related project specific REU data changes.

    Args:
        settings: (dict) Described in load_settings()
        sample: string, which sample to look for within settings dict

    Returns:
        (str) File path of location for promoter reu data.
    """
    synthetic_construct = settings[sample]['fasta_file'].split('/')[-1].split('.')[0]
    prefix = '/'.join(settings[sample]['fasta_file'].split('/')[:4])
    return str(prefix) + '/rna-seq/' +  str(synthetic_construct) + '/' + 'promoter_reu.txt'


def terminator_reu_filename(settings, sample):
    """Load terminator reu filename
    Modify /rna-seq/ if the destination of RNA seq related project specific REU data changes.

    Args:
        settings: (dict) Described in load_settings()
        sample: string, which sample to look for within settings dict

    Returns:
        (str) File path of location for terminator reu data.
    """
    synthetic_construct = settings[sample]['fasta_file'].split('/')[-1].split('.')[0]
    prefix = '/'.join(settings[sample]['fasta_file'].split('/')[:4])
    return str(prefix) + '/rna-seq/' +  str(synthetic_construct) + '/' + 'terminator_reu.txt'


def vcf_name(settings, sample, contig=None):
    if not contig:
        return settings[sample]['output_path'] + sample + '.vcf'
    else:
        return settings[sample]['output_path'] + sample + '.' + contig + '.vcf'


def context_filename(settings):
    return settings['None']['output_path'] + 'context_data.txt'


def bam_readgroup_name(settings, sample, extension=True):
    bam_readgroup_name = settings[sample]['temp_path'] + sample + '.mdup.rg'
    if extension == True:
        bam_readgroup_name += '.bam'
    return bam_readgroup_name


def index_reference(settings, sample):
    cmd_index = 'samtools faidx ' + settings[sample]['fasta_file']
    print("Making reference .fai file: " + cmd_index)
    subprocess.call(cmd_index, shell=True)


def load_settings(filename):
    """Load the settings file
    """
    settings = {}
    try:
        data_reader = csv.reader(open(filename, 'rU'), delimiter='\t')
    except IOError:
        return sys.exit(1)
    # Ignore header
    header = next(data_reader)
    # Process each line
    for row in data_reader:
        if len(row) == len(header):
            sample = row[0]
            sample_data = {}
            for el_idx, el in enumerate(header[1:]):
                sample_data[el] = row[el_idx + 1]
            settings[sample] = sample_data
    return settings


def load_features(settings, sample):
    gff = load_gff(settings, sample)
    features = set()
    for chrom, part in gff.items():
        for g in gff[chrom].values():
            features.add(g[0])
    return features


def get_contigs(settings, sample, host=False):
    contigs = []
    with open(settings[sample]['fasta_file'].rstrip(".fasta") + '.dict', 'r') as inf:
        while True:
            data = inf.readline()
            if not data:
                break
            if data.startswith("@SQ"):
                dats = data.split()
                if not host:
                    if int(dats[2][3:]) < 1000000:
                        contigs.append(dats[1][3:])
                else:
                    contigs.append(dats[1][3:])
            else:
                continue
    return contigs


def trim_adaptors(settings, sample):
    adaptor_seq = settings[sample]['seq_adaptor']
    cmd_index = 'bowtie-build index' + \
                ' -p ' + bwa_index_filename(settings, sample) + \
                ' ' + settings[sample]['fasta_file']
    print("Making index: " + cmd_index)
    subprocess.call(cmd_index, shell=True)


def map_ribo_reads(settings, sample):
    cmd_index = 'bowtie-build index' + \
                ' -p ' + bwa_index_filename(settings, sample) + \
                ' ' + settings[sample]['fasta_file']
    print("Making index: " + cmd_index)
    subprocess.call(cmd_index, shell=True)

    cmd_index = 'bowtie ' + \
                ' -p ' + bwa_index_filename(settings, sample) + \
                ' ' + settings[sample]['fasta_file']
    print("Perform mapping: " + cmd_index)
    subprocess.call(cmd_index, shell=True)


def map_reads(settings, sample, cores):
    """Map reads using STAR
    """
    # Make the indexes
    # Formula to get genomeSAindexNbases: min(14, log2(GenomeLength)/2 - 1)
    # for yeast: 10.76
    with open(settings[sample]['bed_file']) as bedfile:
        data = bedfile.readlines()
    genomesize = sum([int(x.split()[2].rstrip()) for x in data])
    Nbases = min(14, (math.log(genomesize, 2) / 2) - 1)
    cmd_index = 'STAR --runMode genomeGenerate ' + \
                '--runThreadN ' + str(cores) + ' ' + \
                '--genomeDir ./ ' + \
                '--genomeFastaFiles ' + settings[sample]['fasta_file'] + ' ' + \
                '--genomeSAindexNbases ' + str(Nbases)

    print("Making index: " + cmd_index)
    status3 = subprocess.call(cmd_index, shell=True)
    if status3 != 0:
        return 1
    # Perform the mapping
    sam_file = sam_filename(settings, sample)
    if settings[sample]['R2_fastq_file'] == '':
        cmd_mapping = 'STAR ' + \
                      ' --runThreadN ' + str(cores) + \
                      ' --genomeDir ./ ' + \
                      ' --readFilesIn ' + settings[sample]['R1_fastq_file'] + \
                      ' --outSAMtype ' + 'BAM SortedByCoordinate ' + \
                      '--limitBAMsortRAM 40000000 ' + \
                      '--outFileNamePrefix ' + settings[sample]['temp_path'] + sample + '.'
    else:
        cmd_mapping = 'STAR ' + \
                      ' --runThreadN ' + str(cores) + \
                      ' --genomeDir ./ ' + \
                      ' --readFilesIn ' + settings[sample]['R1_fastq_file'] + \
                      ' ' + settings[sample]['R2_fastq_file'] + \
                      ' --outSAMtype ' + 'BAM SortedByCoordinate ' + \
                      '--limitBAMsortRAM 40000000 ' + \
                      '--outFileNamePrefix ' + settings[sample]['temp_path'] + sample + '.'
    print("Mapping Reads (HISAT2): " + cmd_mapping)
    status1 = subprocess.call(cmd_mapping, shell=True)
    if status1 != 0:
        return 1
    return 0


def count_reads(settings, sample, feature='gene', attribute='name', strand_opt='reverse'):
    """Count reads falling in a specific feature type, group on an attribute
    """
    # Use HTSeq to count the reads in specific features
    if settings[sample]['R2_fastq_file'] == '' and strand_opt != '':
        strand_opt = 'yes'
    cmd_count = 'htseq-count' + \
                ' -f bam' + \
                ' -m union' + \
                ' -s ' + strand_opt + \
                ' -a 10' + \
                ' -t ' + feature + \
                ' -i ' + attribute + \
                ' ' + bam_filename(settings, sample, extension=True, sorted=True) + \
                ' ' + settings[sample]['gff_file'] + \
                ' > ' + count_filename(settings, sample, feature)
    print("Counting reads: " + cmd_count)
    status = subprocess.call(cmd_count, shell=True)
    return status


def mapped_reads(settings, sample, cores):
    cmd_total = 'samtools view -@ ' + str(cores) + ' -c -F 4' + \
                ' ' + bam_filename(settings, sample, extension=True, sorted=True) + \
                ' > ' + mapped_reads_filename(settings, sample)
    print("Total mapped reads: " + cmd_total)
    status = subprocess.call(cmd_total, shell=True)
    return status


def load_mapped_reads(settings, sample):
    file_in = open(mapped_reads_filename(settings, sample), 'rU')
    file_data = file_in.readlines()
    if len(file_data) > 0:
        return int(file_data[0])
    else:
        return 0


def load_gene_lengths(settings, sample):
    gene_lengths = {}
    data_reader = csv.reader(open(gene_length_filename(settings, sample), 'rU'), delimiter='\t')
    header = next(data_reader)
    for row in data_reader:
        if len(row) == 2:
            gene_lengths[row[0]] = int(row[1])
    return gene_lengths


def read_count_file(filename):
    """ Read the count file generated by HTSeq
        count_data is a dict (tag -> count)
    """
    count_data = {}
    data_reader = csv.reader(open(filename, 'rU'), delimiter='\t')
    for row in data_reader:
        # Check that data exists and is not reporting by HTSeq
        if len(row) == 2:
            if len(row[0]) > 2 and row[0][0:2] != '__':
                count_data[row[0]] = int(row[1])
    return count_data


def combine_counts(counts, sample_names):
    """ Combine a set of count dictionaries
        counts is a dictorinary of count_data where key is sample name
    """
    full_tag_list = []
    num_of_samples = len(sample_names)
    # Generate the complete tag list (some samples won't have some tags)
    for sample in sample_names:
        for featuredict in counts[sample]:
            full_tag_list = full_tag_list + [x for x in featuredict]
    full_tag_list = list(set(full_tag_list))
    # Generate matrix zero matrix
    count_matrix = {}
    for tag in full_tag_list:
        count_matrix[tag] = [0] * num_of_samples
    # Update where count exists
    for sample_idx in range(num_of_samples):
        sample = sample_names[sample_idx]
        for featuredict in counts[sample]:
            for tag in featuredict:
                count_matrix[tag][sample_idx] = featuredict[tag] 
    return count_matrix


def save_count_matrix(count_matrix, sample_names, filename):
    """ Save a count_matrix with the sample_names to file
    """
    f_out = open(filename, 'w')
    # Write the header
    f_out.write('\t'.join(['gene_name'] + sample_names) + '\n')
    for tag in sorted(count_matrix):
        count_strs = [str(x) for x in count_matrix[tag]]
        f_out.write('\t'.join([tag] + count_strs) + '\n')
    f_out.close()


def save_mapped_reads_matrix(mapped_reads, sample_names, filename):
    f_out = open(filename, 'w')
    f_out.write('sample\ttotal_mapped_reads\n')
    for s in sample_names:
        f_out.write(s + '\t' + str(mapped_reads[s]) + '\n')
    f_out.close()


def save_gene_length_matrix(gene_lengths, filename):
    f_out = open(filename, 'w')
    f_out.write('gene\tlength\n')
    seen = []
    for s in gene_lengths.keys():
        for gene in gene_lengths[s].keys():
            if gene not in seen:
                f_out.write(gene + '\t' + str(gene_lengths[s][gene]) + '\n')
                seen.append(gene)
    f_out.close()


def count_matrix(settings):
    counts = {}
    for sample in settings.keys():
        if sample != 'None':
            counts[sample] = read_count_file(count_filename(settings, sample))
    sample_names = counts.keys()
    count_matrix = combine_counts(counts, sample_names)
    save_count_matrix(count_matrix, sample_names,
                      settings['None']['output_path'] + 'read_count.matrix')


def gene_lengths(settings, sample):
    """ Calculate the gene lengths from set of GTF references
    """
    len_file = gene_length_filename(settings, sample)
    f_out = open(len_file, 'w')
    f_out.write('gene_name\tlength\n')
    data_reader = csv.reader(open(settings[sample]['gff_file'], 'rU'), delimiter='\t')
    for row in data_reader:
        if not row[0].startswith('#'):
            attribs = row[8].split(';')[0]
            key = attribs.split('=')[0]
            value = attribs.split('=')[1]
            if "hypothetical" not in value.lower():
                gene_length = int(row[4]) - int(row[3]) + 1
                f_out.write(value + '\t' + str(gene_length) + '\n')
    f_out.close()
    if os.stat(len_file).st_size == 0:
        return 1
    return 0


def make_profile(settings, sample, cores):
    """ Calculate transcription profile for given regions in BED file
        http://seqanswers.com/forums/showthread.php?t=29399
    """
    if settings[sample]['R2_fastq_file'] == '':
        # https://www.biostars.org/p/14378/
        fwd_filename = bam_filename(settings, sample, extension=False) + '.fwd.bam'
        cmd_fwd_coverage = 'samtools view -@ ' + str(cores) + ' -b -F 20 ' + \
                           bam_filename(settings, sample, extension=True, sorted=True) + \
                           ' > ' + fwd_filename + ' && ' + \
                           'samtools index ' + fwd_filename + ' && ' + \
                           'bedtools coverage -d -abam ' + fwd_filename + ' -b ' + settings[sample]['bed_file'] + \
                           ' > ' + profile_fwd_filename(settings, sample) + \
                           ' && gzip ' + profile_fwd_filename(settings, sample)
        print("Making forward profile: " + cmd_fwd_coverage)
        subprocess.call(cmd_fwd_coverage, shell=True)
        rev_filename = bam_filename(settings, sample, extension=False) + '.rev.bam'
        cmd_rev_coverage = 'samtools view -@ ' + str(cores) + ' -b -f 16 ' + \
                           bam_filename(settings, sample, extension=True, sorted=True) + \
                           ' > ' + rev_filename + ' && ' + \
                           'samtools index ' + rev_filename + ' && ' + \
                           'bedtools coverage -d -abam ' + rev_filename + ' -b ' + settings[sample]['bed_file'] + \
                           ' > ' + profile_rev_filename(settings, sample) + \
                           ' && gzip ' + profile_rev_filename(settings, sample)
        print("Making reverse profile: " + cmd_rev_coverage)
        status = subprocess.call(cmd_rev_coverage, shell=True)

    else:
        fwd_filename = bam_filename(settings, sample, extension=False) + '.fwd.bam'
        fwd1_filename = bam_filename(settings, sample, extension=False) + '.fwd.1.bam'
        fwd2_filename = bam_filename(settings, sample, extension=False) + '.fwd.2.bam'
        cmd_fwd_coverage = 'samtools view -@ ' + str(cores) + ' -b -f 83 ' + \
                           bam_filename(settings, sample, extension=True, sorted=True) + \
                           ' > ' + fwd1_filename + ' && ' + \
                           'samtools index ' + fwd1_filename + ' && ' + \
                           'samtools view -@ ' + str(cores) + ' -b -f 163 ' + \
                           bam_filename(settings, sample, extension=True, sorted=True) + \
                           ' > ' + fwd2_filename + ' && ' + \
                           'samtools index ' + fwd2_filename + ' && ' + \
                           'samtools merge -@ ' + str(cores) + ' -f ' + fwd_filename + \
                           ' ' + fwd1_filename + ' ' + fwd2_filename + ' && ' + \
                           'samtools index ' + fwd_filename + ' && ' + \
                           'bedtools coverage -d -abam ' + fwd_filename + ' -b ' + settings[sample]['bed_file'] + \
                           ' > ' + profile_fwd_filename(settings, sample) + \
                           ' && gzip ' + profile_fwd_filename(settings, sample)
        print("Making forward profile: " + cmd_fwd_coverage)
        subprocess.call(cmd_fwd_coverage, shell=True)
        rev_filename = bam_filename(settings, sample, extension=False) + '.rev.bam'
        rev1_filename = bam_filename(settings, sample, extension=False) + '.rev.1.bam'
        rev2_filename = bam_filename(settings, sample, extension=False) + '.rev.2.bam'
        cmd_rev_coverage = 'samtools view -@ ' + str(cores) + ' -b -f 99 ' + \
                           bam_filename(settings, sample, extension=True, sorted=True) + \
                           ' > ' + rev1_filename + ' && ' + \
                           'samtools index ' + rev1_filename + ' && ' + \
                           'samtools view -@ ' + str(cores) + ' -b -f 147 ' + \
                           bam_filename(settings, sample, extension=True, sorted=True) + \
                           ' > ' + rev2_filename + ' && ' + \
                           'samtools index ' + rev2_filename + ' && ' + \
                           'samtools merge -@ ' + str(cores) + ' -f ' + rev_filename + \
                           ' ' + rev1_filename + ' ' + rev2_filename + ' && ' + \
                           'samtools index ' + rev_filename + ' && ' + \
                           'bedtools coverage -d -abam ' + rev_filename + ' -b ' + settings[sample]['bed_file'] + \
                           ' > ' + profile_rev_filename(settings, sample) + \
                           ' && gzip ' + profile_rev_filename(settings, sample)
        print("Making reverse profile: " + cmd_rev_coverage)
        status = subprocess.call(cmd_rev_coverage, shell=True)
    return status


########## CHARACTERIZATION ##########

def load_gff(settings, sample):
    """Function to load gff file data into a dictionary

    Load the information within the gff file into a dictionary. This will be used to generate a list of all parts
    for generation of the context data structure. The first column contains chromosome or plasmid name to serve as main
    keys in the gff dictionary. Mostly the RNAseq analysis focuses on the host plasmid, but information is obtained for
    all entries in the gff.
    The part names are determined by scanning the 9th column in the file for the identifier 'Name='. Parts are further
    classified into different feature types by values in the third column.

    Args:
        filename (str): File path to gff file with all part information

    Return:
        gff (dict): Dictionary with information for every part within the plasmid and host organism

            {
                chromosome:
                    {
                        part1: [part_type, part_direction, start_bp, end_bp, part_attributes],
                        part2: ...
                    }
            }
    """
    gff = {}
    data_reader = csv.reader(open(settings[sample]['gff_file'], 'rU'), delimiter='\t')
    # Process each line
    for row in data_reader:
        if len(row) == 9:
            chromo = row[0]
            part_type = row[2]
            start_bp = int(row[3])
            end_bp = int(row[4])
            part_dir = row[6]
            part_attribs = {}
            split_attribs = row[8].split(';')
            part_name = None
            for attrib in split_attribs:
                key_value = attrib.split('=')
                if len(key_value) == 2:
                    if key_value[0].lower() == 'name':
                        part_name = key_value[1]
                    else:
                        part_attribs[key_value[0]] = key_value[1]
            if part_name is not None:
                if chromo not in gff.keys():
                    gff[chromo] = {}
                gff[chromo][part_name] = [part_type, part_dir, start_bp, end_bp, part_attribs]
    return gff


def reverse_region(region):
    return [region[1][::-1], region[0][::-1]]


########## FRAGMENT DISTRIBUTIONS ##########

def fragment_length_dists(settings, sample, reads_to_sample=1000000):
    """ PE: Adapted from get_insert_size.py (Wei Li)
    """
    frag_file = fragment_dist_filename(settings, sample)
    sam_file = sam_filename(settings, sample)
    if settings[sample]['R2_fastq_file'] == '':
        nline = 0
        plrdspan = {}
        with open(sam_file, 'rU') as ins:
            for lines in ins:
                field = lines.strip().split()
                nline = nline + 1
                if nline >= reads_to_sample:
                    break
                if len(field) < 12:
                    continue
                try:
                    for f in field:
                        if 'AS:i' in f:
                            dist = int(f.split(':')[-1])
                    if dist == 0:
                        continue
                    elif dist in plrdspan.keys():
                        plrdspan[dist] = plrdspan[dist] + 1
                    else:
                        plrdspan[dist] = 1
                except ValueError:
                    continue
    else:
        plrdlen = {}
        plrdspan = {}
        objmrl = re.compile('([0-9]+)M$')
        objmtj = re.compile('NH:i:(\d+)')
        nline = 0
        with open(sam_file, 'rU') as ins:
            for lines in ins:
                field = lines.strip().split()
                nline = nline + 1
                if nline >= reads_to_sample:
                    break
                if len(field) < 12:
                    continue
                try:
                    mrl = objmrl.match(field[5])
                    if mrl == None:  # ignore non-perfect reads
                        continue
                    readlen = int(mrl.group(1))
                    if readlen in plrdlen.keys():
                        plrdlen[readlen] = plrdlen[readlen] + 1
                    else:
                        plrdlen[readlen] = 1
                    if field[6] != '=':
                        continue
                    dist = int(field[8])
                    if dist <= 0:  # ignore neg dist
                        continue
                    mtj = objmtj.search(lines)
                    if dist in plrdspan.keys():
                        plrdspan[dist] = plrdspan[dist] + 1
                    else:
                        plrdspan[dist] = 1
                except ValueError:
                    continue
    f_out = open(frag_file, 'w')
    for k in sorted(plrdspan.keys()):
        f_out.write(str(k) + '\t' + str(plrdspan[k]) + '\n')
    if os.stat(frag_file).st_size == 0:
        return 1
    return 0
