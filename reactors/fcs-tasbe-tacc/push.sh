#!/usr/bin/env bash

version=$(cat fcs-tasbe-0.2.0/VERSION)

CONTAINER_IMAGE="sd2e/fcs:$version"

docker push ${CONTAINER_IMAGE}
