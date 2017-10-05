CONTAINER_IMAGE="index.docker.io/sd2e/hello-container:0.1.0"

. _util/container_exec.sh

COMMAND='bash'
PARAMS='/opt/scripts/hello.sh WORLD'

container_exec ${CONTAINER_IMAGE} ${COMMAND} ${PARAMS}
