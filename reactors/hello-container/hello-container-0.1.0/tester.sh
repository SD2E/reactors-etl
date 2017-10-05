#!/usr/bin/env bash

CONTAINER_IMAGE="index.docker.io/sd2e/hello-container:0.1.0"

. _util/container_exec.sh

COMMAND='bash'
PARAMS='/opt/scripts/hello.sh WORLD'

DEBUG=1 container_exec ${CONTAINER_IMAGE} ${COMMAND} ${PARAMS}

######################
#  FUNCTIONAL TESTS  #
#                    #
# Dont include in    #
# runner-template.sh #
######################


function cleanup() {

    rm -f .container_exec.*

}

function validate_output() {

    return 0

}

function run_tests() {

    validate_output
    return 0
}

run_tests && \
    echo "Success" && \
    cleanup

