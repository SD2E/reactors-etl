#!/usr/bin/env bash

CONTAINER_TAG="jurrutia/sailfish:0.10.2--1"

docker build -t ${CONTAINER_TAG} . && docker push ${CONTAINER_TAG}
