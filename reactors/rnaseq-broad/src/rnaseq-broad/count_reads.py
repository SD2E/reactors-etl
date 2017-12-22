#!/usr/bin/env python

#	Copyright (C) 2015 by
#	Voigt Lab, MIT
# 	All rights reserved.
#	OSI Non-Profit Open Software License ("Non-Profit OSL") 3.0 license.

# Supporting modules
import argparse
import genetic_analyzer as ga
import sys


def main():
    # Parse the command line inputs
    parser = argparse.ArgumentParser(description="count_reads")
    parser.add_argument("-settings", dest="settings", required=True, help="settings.txt", metavar="string")
    parser.add_argument("-samples", dest="samples", required=True, help="1,2", metavar="string")
    parser.add_argument("-attribute", dest="attribute", required=False, metavar="string", default='name')
    parser.add_argument("-strand_opt", dest="strand_opt", required=False, help="If stranded protocol was used",
                        metavar="string", default='reverse')
    parser.add_argument("-cores", dest="cores", required=True, help="# cores", metavar="int")
    args = parser.parse_args()
    # Run the command
    cores = args.cores
    samples = args.samples.split(',')
    settings = ga.load_settings(args.settings)
    attribute = args.attribute
    s_opt = args.strand_opt
    for s in samples:
        features = ga.load_features(settings, s)
        status1 = ga.mapped_reads(settings, s, cores)
        status2 = ga.gene_lengths(settings, s, features=features)
        for f in features:
            status3 = ga.count_reads(settings, s, feature=f, attribute=attribute, strand_opt=s_opt)
            if status3 == 0:
                continue
            else:
                return "Count reads failed"
    return (status1 + status2)


if __name__ == "__main__":
    status = main()
    sys.exit(status)
