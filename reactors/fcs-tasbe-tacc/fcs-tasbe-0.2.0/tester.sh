#!/usr/bin/env bash

version=$(cat VERSION)
export CONTAINER_IMAGE="sd2e/fcs:$version"

export inputData="Q0-ProtStab-BioFab-Flow_29092017.zip"
export fcOverride="updated-fc.json"

if [ ! "$CLEAN" == 1 ]
then

    # Set up test data
    cp -R ../test-data-cache/${fcOverride} . || exit 1
    cp -R ../test-data-cache/${inputData} . || exit 1
    touch .dirty

    bash runner-template.sh

fi

# Outputs
if [ "$CLEAN" == 1 ]
then
    # Delete likely workflow outputs
    for F in beads_001 samples_001 plots output.csv octave-workspace fc.json
    do
        rm -rf $F
    done
    # Delete miscellaneous
    for G in .agave.archive .dirty $inputData $fcOverride "*.bak"
    do
        rm -rf $G
    done
fi
