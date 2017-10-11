#!/usr/bin/env bash

version=$(cat VERSION)

# No need to set _CONTAINER_ENGINE now. The container_exec function detects
# Docker and Singularity, preferring to run with Docker
CONTAINER_IMAGE="index.docker.io/sd2e/msf:$version"

# Temporary until we get the container executor configured each TACC system
# This code is evolving and will eventually become a service on the host
. _util/container_exec.sh

COMMAND='python'
PARAMS='/opt/scripts/msf.py --files localtest/exp2801-04-ds731218.msf --output exp2801-04-ds731218.msf.csv'

DEBUG=1 container_exec ${CONTAINER_IMAGE} ${COMMAND} ${PARAMS}


######################
#  FUNCTIONAL TESTS  #
#                    #
# Dont include in    #
# runner-template.sh #
######################


function cleanup() {

    rm -f exp2801-04-ds731218.msf.csv
    rm -f .container_exec.*

}

function validate_csv() {

    return 0

}

function run_tests() {

    validate_csv exp2801-04-ds731218.msf.csv
    return 0
}

run_tests && \
    echo "Success" && \
    cleanup

