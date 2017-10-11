version=$(cat ../VERSION)

CONTAINER_IMAGE="index.docker.io/sd2e/msf:$version"
. _util/container_exec.sh

COMMAND='python'
PARAMS='/opt/scripts/msf.py --files ${msfDataFile} --output ${outputFileName}'

DEBUG= container_exec ${CONTAINER_IMAGE} ${COMMAND} ${PARAMS}
