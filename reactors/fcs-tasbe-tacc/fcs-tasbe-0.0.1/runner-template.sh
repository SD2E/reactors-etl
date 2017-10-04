CONTAINER_IMAGE="index.docker.io/sd2e/fcs:0.0.6"

# Temporary until we get the container executor configured each TACC system
. _util/container_exec.sh

threads=$(auto_maxthreads)

container_exec ${CONTAINER_IMAGE} python /opt/scripts/fc.py --octave-method-path /opt/scripts/ \
 --label ${label} \
 --files ${files} \
 --type ${type} \
 --output "output.csv"
