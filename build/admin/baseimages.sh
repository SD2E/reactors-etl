#!/usr/bin/env bash

_TENANT_DOCKER_ORG=$1
_APIVERSION=$2
_COMMAND=$3

echo "Command: $_COMMAND"

if [[ -z "$DIR" ]]; then
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
fi

OWD=$PWD
for _BASE in base
do
    echo "Building base..."
    cd $DIR/docker/$_BASE
    for _VERSION in alpine36 ubuntu14 ubuntu16
    do
        echo "Version: $_VERSION"
        ls 
        if [ -f "Dockerfile.${_VERSION}" ];
        then
            ../../docker.sh "$_TENANT_DOCKER_ORG/$_BASE" "${_VERSION}" "Dockerfile.${_VERSION}" "${_COMMAND}"
        fi
    done
    cd $OWD
done
