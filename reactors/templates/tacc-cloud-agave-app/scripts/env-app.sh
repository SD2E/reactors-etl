#!/usr/bin/env bash

APPNAME="%app"
DOCKER_CONTAINER="cyverse/dnasub_apps"
SINGULARITY_CONTAINER="cyverse-dnasub_apps.img"

TYPE=${TYPE:-docker}

#singularity exec
if [[ "$TYPE" == "docker" ]];
then
	docker run -v $PWD:/home:rw ${DOCKER_CONTAINER}
fi

if [[ "$TYPE" == "singularity" ]];
then
	singularity run ${SINGULARITY_CONTAINER}
fi
