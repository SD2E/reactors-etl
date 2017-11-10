#!/usr/bin/env bash

version=$(cat rnaseq/VERSION)

CONTAINER_IMAGE="sd2e/rnaseq:$version"

docker build -t ${CONTAINER_IMAGE} .
