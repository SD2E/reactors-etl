#!/usr/bin/env bash

version=$(cat rnaseq-broad/VERSION)

CONTAINER_IMAGE="jurrutia/rnaseq-broad:$version"

docker push ${CONTAINER_IMAGE}
