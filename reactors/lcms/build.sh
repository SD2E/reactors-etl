#!/usr/bin/env bash

CONTAINER_IMAGE="sd2e/lcms:latest"

docker build -t ${CONTAINER_IMAGE} . && docker push ${CONTAINER_IMAGE}
