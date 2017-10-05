#!/usr/bin/env bash

CONTAINER_TAG="sd2e/kallisto:0.43.1--hdf51.8.17_0"

docker build -t ${CONTAINER_TAG} . && docker push ${CONTAINER_TAG}
