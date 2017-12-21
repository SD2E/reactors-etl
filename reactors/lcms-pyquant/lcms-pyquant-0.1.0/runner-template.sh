CONTAINER_IMAGE="index.docker.io/chrismit7/pyquant"

. _util/container_exec.sh

#COMMAND='pyQuant'
PARAMS='--search-file ${search_file}'

container_exec ${CONTAINER_IMAGE} ${COMMAND} ${PARAMS}
