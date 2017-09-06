#!/usr/bin/env bash

_TENANT_DOCKER_ORG=$1
_VERSION=$2
_COMMAND=$3

if [ -z "$_COMMAND" ]; then COMMAND="build"; fi

if [[ -z "$DIR" ]]; then
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
fi

for BASE in alpine_36 ubuntu_xenial centos_7
do
    cd $DIR/docker/reactor_$BASE
    ../../docker.sh "$_TENANT_DOCKER_ORG/reactor_${BASE}" "${_VERSION}" Dockerfile ${_COMMAND}
done
