CONTAINER_IMAGE="index.docker.io/sd2e/lcms:latest"

. _util/container_exec.sh

COMMAND='python'
PARAMS='/opt/scripts/lcms.py --files ${lcmsDataFile} --output ${outputFileName}'

DEBUG= container_exec ${CONTAINER_IMAGE} ${COMMAND} ${PARAMS}
