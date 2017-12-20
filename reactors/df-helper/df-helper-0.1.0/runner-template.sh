version=$(cat VERSION)

CONTAINER_IMAGE="index.docker.io/sd2e/df-helper:$version"

. _util/container_exec.sh

COMMAND='python'
PARAMS='/opt/scripts/df-helper.py --manifest ${manifestFile}'

DEBUG= container_exec ${CONTAINER_IMAGE} ${COMMAND} ${PARAMS}
