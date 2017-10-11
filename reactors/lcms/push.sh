#!/usr/bin/env bash

version=$(cat lcms-0.1.0/VERSION)

CONTAINER_IMAGE="sd2e/lcms:$version"

docker push ${CONTAINER_IMAGE}
