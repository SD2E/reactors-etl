#!/usr/bin/env bash

CONTAINER_IMAGE="sd2e/msf:latest"

docker build -t ${CONTAINER_IMAGE} . && docker push ${CONTAINER_IMAGE}
