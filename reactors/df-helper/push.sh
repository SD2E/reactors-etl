#!/usr/bin/env bash

version=$(cat df-helper-0.1.0/VERSION)

CONTAINER_IMAGE="sd2e/df-helper:$version"

docker push ${CONTAINER_IMAGE}
