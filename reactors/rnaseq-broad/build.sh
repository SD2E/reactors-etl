#!/usr/bin/env bash

version=$(cat rnaseq-broad/VERSION)

CONTAINER_IMAGE="acristo/rnaseq-broad:$version"

docker build -t ${CONTAINER_IMAGE} .