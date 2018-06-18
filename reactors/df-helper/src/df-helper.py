"""

Helper code to support common tasks related to post-ETL dataframe generation

For now, this does very little:

It retrieves manifests and queries for a plan given a manifest

Will be expanded or shared among dataframe producing code for each ETL'd data type

$ python df-helper.py --manifest <input_manifest>

"""
import sys, json, argparse

parser = argparse.ArgumentParser()
parser.add_argument('--manifest', help='Input manifest', required=True)

def main(args):
    
    with open(args.manifest) as manifest_file:    
        manifest_json = json.loads(manifest_file.read())
    
    # TODO SBH manifest->plan query
    # This is not currently in SBH, Nic is working on adding it
    # See discussion in chaos-xplan channel
    
if __name__ == '__main__':
    args = parser.parse_args()
    main(args)