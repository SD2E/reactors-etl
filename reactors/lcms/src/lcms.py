"""Tool to parse mass spec files using R's xcms file

This is a tool to auto-generate data set summaries.

Example:
    Recommended way to run this tool is:

        $ python lcms.py --in <input_filename> --out <output_filename>

"""
import pandas as pd
import numpy as np
import argparse
from pyteomics import mgf, mzml, fasta, auxiliary 

def ingest_mgf(input_filename):
    """Ingest an mgf file given it's name and return a dataframe of the file
    """
    with mgf.read('tests/test.mgf') as reader:
        auxiliary.print_tree(next(reader))

def ingest_fasta(input_filename):
    """Ingest an fasta file given it's name and return a dataframe of the file
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
        
def main():
    
    #Parse the arguments to read in the file name and export another file
    parser = argparse.ArgumentParser(description='LC/MS ETL')
    parser.add_argument("--in", help="Input Filename",  required=True)
    parser.add_argument("--out", help="Output Filename", required=True)
    args = vars(parser.parse_args())
    
    #variables will be
    print "args",args["in"],"---",args["out"]
    
    if "mgf" in args["in"]:
        ingest_mgf(args["in"])
    elif "fasta" in args["in"]:
        df = ingest_fasta(args["in"])
        print df.shape
    else:
        ingest_mzML(args["in"])

if __name__ == "__main__":
    main()