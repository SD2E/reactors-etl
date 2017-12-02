#!/usr/bin/env bash

version=$(cat rnaseq-broad/VERSION)

CONTAINER_IMAGE="sd2e/rnaseq-broad:$version"

docker push ${CONTAINER_IMAGE}
