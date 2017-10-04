#!/usr/bin/env bash

# No need to set _CONTAINER_ENGINE now. The container_exec function detects
# Docker and Singularity, preferring to run with Docker
CONTAINER_IMAGE="index.docker.io/sd2e/lcms:latest"

# Temporary until we get the container executor configured each TACC system
# This code is evolving and will eventually become a service on the host
. _util/container_exec.sh

COMMAND='python'
PARAMS='/opt/scripts/lcms.py --files localtest/ec_K12.fasta --output ec_K12.csv'

DEBUG=1 container_exec ${CONTAINER_IMAGE} ${COMMAND} ${PARAMS}


######################
#  FUNCTIONAL TESTS  #
#                    #
# Dont include in    #
# runner-template.sh #
######################

function run_tests() {

    validate_csv ec_K12.csv
    return 0
}

function validate_csv() {

    return 0

}

function cleanup() {

    rm -f ec_K12.csv
    rm -f .container_exec.*

}

run_tests && \
    echo "Success" && \
    cleanup

