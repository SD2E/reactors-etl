#!/usr/bin/env bash

# No need to set _CONTAINER_ENGINE now. The container_exec function detects
# Docker and Singularity, preferring to run with Docker
CONTAINER_IMAGE="index.docker.io/chrismit7/pyquant"

# Temporary until we get the container executor configured each TACC system
# This code is evolving and will eventually become a service on the host
. _util/container_exec.sh

COMMAND='pyQuant'

PARAMS='--search-file localtest/exp3978-2-ds1266896.msf'

container_exec ${CONTAINER_IMAGE} ${COMMAND} ${PARAMS}