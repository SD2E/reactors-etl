#!/usr/bin/env bash

version=$(cat VERSION)

CONTAINER_IMAGE="sd2e/lcms:$version"

docker build -t ${CONTAINER_IMAGE} .