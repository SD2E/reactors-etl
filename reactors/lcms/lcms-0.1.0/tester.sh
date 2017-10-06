#!/usr/bin/env bash

# No need to set _CONTAINER_ENGINE now. The container_exec function detects
# Docker and Singularity, preferring to run with Docker
CONTAINER_IMAGE="index.docker.io/sd2e/lcms:latest"

# Temporary until we get the container executor configured each TACC system
# This code is evolving and will eventually become a service on the host
. _util/container_exec.sh

COMMAND='python'
PARAMS='/opt/scripts/lcms.py --files localtest/exp1720-04-ds259269.mzML --output exp1720-04-ds259269.mzML.csv'

DEBUG=1 container_exec ${CONTAINER_IMAGE} ${COMMAND} ${PARAMS}

#PARAMS='/opt/scripts/lcms.py --files localtest/exp1720-04-ds259269.mzML --output exp1720-04-ds259269.csv'
#DEBUG=1 container_exec ${CONTAINER_IMAGE} ${COMMAND} ${PARAMS}

######################
#  FUNCTIONAL TESTS  #
#                    #
# Dont include in    #
# runner-template.sh #
######################

function run_tests() {

    validate_csv exp1720-04-ds259269.mzML.csv
    if [ $? -ne 0 ]; then
        return 1
    fi
    return 0
}

function validate_csv() {
    if [ -f "$1" ]; then
        return 0
    else
        echo "$1 not found"
        return 1
    fi
}

function cleanup() {

    echo "Cleaning up..."
    rm -f exp1720-04-ds259269.mzML.csv
    rm -f .container_exec.*
}

trap cleanup EXIT

run_tests
if [ $? -eq 0 ]; then
    echo "Success!"
    exit 0
else
    echo "Test failed!"!
    exit 1
fi
