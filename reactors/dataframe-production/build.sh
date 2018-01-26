#!/usr/bin/env bash

CONTAINER_TAG="sd2e/dataframe-prod-0.1.0"

docker build -t ${CONTAINER_TAG} . && docker push ${CONTAINER_TAG}
