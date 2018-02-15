#!/usr/bin/env bash

CONTAINER_TAG="sd2e/lcms-pyquant-0.1.1"

docker build -t ${CONTAINER_TAG} . && docker push ${CONTAINER_TAG}
