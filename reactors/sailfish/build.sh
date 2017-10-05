#!/usr/bin/env bash

CONTAINER_TAG="sd2e/sailfish:0.10.1--1"

docker build -t ${CONTAINER_TAG} . && docker push ${CONTAINER_TAG}
