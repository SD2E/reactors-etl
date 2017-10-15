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
    '''
    {'count': 2,
    'index': 2,
    'highest observed m/z': 2020.216835219264,
    'm/z array': array([  346.51808351
    'ms level': 1,
    'total ion current': 5284812.0,
    'profile spectrum': '',
    'lowest observed m/z': 346.518083514683,
    'defaultArrayLength': 6305,
    'intensity array':,
    'positive scan': '',
    'MS1 spectrum': '',
    'spectrum title': 'exp1720-04-ds259269.3.3. File:"exp1720-04-ds259269.raw", NativeID:"controllerType=0 controllerNumber=1 scan=3"',
    'base peak intensity': 836452.44,
    'scanList': {'count': 1, 'no combination': '', 'scan': [{'filter string': 'FTMS + p NSI Full ms [350.00-2000.00]',
    'scan start time': 5.0165227,
    'ion injection time': 100.000001490116,
    'scanWindowList': {'count': 1, 'scanWindow': [{'scan window lower limit': 350.0, 'scan window upper limit': 2000.0}]}, 'preset scan configuration': 1.0}]},
    'id': 'controllerType=0 controllerNumber=1 scan=3',
    'base peak m/z': 371.1017749}
        '''
    columns = []
    colProc = False
    with mzml.read(input_filename) as reader:
      mzml_list = []
      for item in reader:
        row = []
        #item["count"],
        #item["index"],
        col = "highest observed m/z"
        if col in item:
          row.append(float(item[col]))
          if not colProc:
            columns.append(col)
        #item["m/z array"],
        col = "ms level"
        if col in item:
          row.append(int(item[col]))
          if not colProc:
            columns.append(col)
        col = "total ion current"
        if col in item:
          row.append(float(item[col]))
          if not colProc:
            columns.append(col)
       #item["profile spectrum"],
        col = "lowest observed m/z"
        if col in item:
          row.append(float(item[col]))
          if not colProc:
            columns.append(col)
        #item["intensity array"],
        #item["positive scan"],
        #item["MS1 spectrum"],
        #exp1720-04-ds259269.3.3. File:"exp1720-04-ds259269.raw", NativeID:"controllerType=0 controllerNumber=1 scan=3"
        col = "spectrum title"
        if col in item:
          row.append(str(item[col].split("File:\"")[1].split("\",")[0]))
          row.append(int(item[col].split("controllerType=")[1].split(" ")[0]))
          row.append(int(item[col].split("controllerNumber=")[1].split(" ")[0]))
          row.append(int(item[col].split("scan=")[1].split("\"")[0]))
          if not colProc:
            columns.append("File")
            columns.append("controllerType")
            columns.append("controllerNumber")
            columns.append("scan")
        col = "base peak intensity"
        if col in item:
          row.append(float(item[col]))
          if not colProc:
            columns.append(col)
        #item["scanList"],
        #item["id"],
        col = "base peak m/z"
        if col in item:
          row.append(float(item[col]))
          if not colProc:
            columns.append(col)
        if not colProc:
          colProc = True
        mzml_list.append(row)
    df = pd.DataFrame(mzml_list,columns=columns)

    return df
        
def main(args):
    
    if "mgf" in args.files.lower():
        ingest_mgf(args.files)
    elif "fasta" in args.files.lower():
        df = ingest_fasta(args.files)
    elif "mzml" in args.files.lower():
        df = ingest_mzML(args.files)
    else:
        raise ValueError('Could not parse:' + args.files)

    df.to_csv(args.output)

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)