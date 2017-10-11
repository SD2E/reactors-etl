#!/usr/bin/env bash

version=$(cat VERSION)

CONTAINER_IMAGE="sd2e/lcms:$version"

docker push ${CONTAINER_IMAGE}
