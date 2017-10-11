#!/usr/bin/env bash

version=$(cat msf-0.1.0/VERSION)

CONTAINER_IMAGE="sd2e/msf:$version"

docker build -t ${CONTAINER_IMAGE} .