CONTAINER_IMAGE="index.docker.io/sd2e/hello-container:0.1.0"

# Temporary until we get the container executor configured each TACC system
. _util/container_exec.sh

threads=$(auto_maxthreads)

DEBUG=0 container_exec ${CONTAINER_IMAGE} /opt/scripts/hello.sh "WORLD"
