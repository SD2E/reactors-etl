#!/bin/bash

IMAGENAME=$1
SDKVERSION=$2
DOCKERFILE=$3
COMMAND=$4

echo "Command: $COMMAND"

function die {

    die "$1"
    exit 1

}

DOCKER_INFO=`docker info > /dev/null`
if [ $? -ne 0 ] ; then die "Docker not found or unreachable. Exiting." ; fi

if [[ "$COMMAND" == 'build' ]];
then

echo "image: $IMAGENAME"
echo "version: $SDKVERSION"
echo "dockerfile: $DOCKERFILE"
echo "cmd: $COMMAND"

docker build --rm=true -t ${IMAGENAME}:${SDKVERSION} -f ${DOCKERFILE} .
if [ $? -ne 0 ] ; then die "Error on build. Exiting." ; fi

IMAGEID=`docker images -q  ${IMAGENAME}:${SDKVERSION}`
if [ $? -ne 0 ] ; then die "Can't find image ${TENANT_DOCKER_ORG}/${IMAGENAME}:${SDKVERSION}. Exiting." ; fi

docker tag ${IMAGEID} ${IMAGENAME}:latest
if [ $? -ne 0 ] ; then die "Error tagging with 'latest'. Exiting." ; fi

fi


if [[ "$COMMAND" == 'release' ]];
then

docker push ${IMAGENAME}:${SDKVERSION}

if [ $? -ne 0 ] ; then die "Error pushing to Docker Hub. Exiting." ; fi
fi


if [[ "$COMMAND" == 'clean' ]];
then

docker rmi -f ${IMAGENAME}:${SDKVERSION} && docker rmi -f ${IMAGENAME}:latest

if [ $? -ne 0 ] ; then die "Error deleting local images. Exiting." ; fi
fi
