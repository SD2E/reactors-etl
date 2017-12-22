#!/usr/bin/env bash

version=$(cat rnaseq-0.1.1/VERSION)

CONTAINER_IMAGE="sd2e/rnaseq:$version"

docker push ${CONTAINER_IMAGE}
