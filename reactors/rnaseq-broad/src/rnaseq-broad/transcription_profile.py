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
    parser = argparse.ArgumentParser(description="transcription_profile")
    parser.add_argument("-settings", dest="settings", required=True, help="settings.txt", metavar="string")
    parser.add_argument("-samples", dest="samples", required=True, help="1,2", metavar="string")
    parser.add_argument("-cores", dest="cores", required=True, help="# cores", metavar="int")
    args = parser.parse_args()
    # Run the command
    cores = args.cores
    samples = args.samples.split(',')
    settings = ga.load_settings(args.settings)
    for s in samples:
        status = ga.make_profile(settings, s, cores)
    return status


if __name__ == "__main__":
    status = main()
    sys.exit(status)
