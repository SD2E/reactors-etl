"""Tool to parse mass spec files using R's xcms file

This is a tool to auto-generate data set summaries.

Example:
    Recommended way to run this tool is:

        $ python lcms.py --files <input_filename> --output <output_filename>

"""
import pandas as pd
import numpy as np
import argparse
from pyteomics import mgf, mzml, fasta, auxiliary 

parser = argparse.ArgumentParser()
parser.add_argument('--files', help='Input fasta or mzML file(s) for parsing', required=True)
parser.add_argument('--output', help='Name of output CSV file', default='output.csv')

def ingest_mgf(input_filename):
    """Ingest an mgf file given its name and return a dataframe of the file
    """
    with mgf.read('tests/test.mgf') as reader:
        auxiliary.print_tree(next(reader))

def ingest_fasta(input_filename):
    """Ingest an fasta file given its name and return a dataframe of the file
    """
    with fasta.read(input_filename) as reader:
        for entry in reader:
            prot_list = [[item.description.split("|")[0]+":"+item.description.split("|")[1],
                          item.description.split("|")[3],item.description.split("|")[4],item.sequence] for item in reader]
    df = pd.DataFrame(prot_list,columns=["GeneInfo ID","Accession","Description","Sequence"])
    return df
        
def ingest_mzML(input_filename):
    """Ingest an mzML or mzXML file given it's name and return a dataframe of the file
    """
    with mzml.read('tests/test.mzML') as reader:
        auxiliary.print_tree(next(reader))
        
def main(args):
    
    if "mgf" in args.files:
        ingest_mgf(args.files)
    elif "fasta" in args.files:
        df = ingest_fasta(args.files)
        df.to_csv(args.output)
    else:
        ingest_mzML(args.files)

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)