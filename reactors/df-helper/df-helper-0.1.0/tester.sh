#!/usr/bin/env bash

version=$(cat VERSION)

# No need to set _CONTAINER_ENGINE now. The container_exec function detects
# Docker and Singularity, preferring to run with Docker
CONTAINER_IMAGE="sd2e/df-helper:$version"

# Temporary until we get the container executor configured each TACC system
# This code is evolving and will eventually become a service on the host
. _util/container_exec.sh

COMMAND='python'

PARAMS='/opt/scripts/df-helper.py --manifest localtest/107795-manifest.json'

DEBUG=1 container_exec ${CONTAINER_IMAGE} ${COMMAND} ${PARAMS}

######################
#  FUNCTIONAL TESTS  #
#                    #
# Dont include in    #
# runner-template.sh #
######################

function run_tests() {

    return 0
}


function cleanup() {

    echo "Cleaning up..."
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
