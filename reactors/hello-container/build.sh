#!/usr/bin/env bash

CONTAINER_TAG="sd2e/hello-container:0.1.0"

docker build -t ${CONTAINER_TAG} . && docker push ${CONTAINER_TAG}
