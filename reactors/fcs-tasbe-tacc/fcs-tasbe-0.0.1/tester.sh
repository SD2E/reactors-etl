_CONTAINER_ENGINE=docker
CONTAINER_IMAGE="index.docker.io/sd2e/fcs:0.0.2"

# Temporary until we get the container executor configured each TACC system
. _util/container_exec.sh

threads=$(auto_maxthreads)

type=geo_mean_std
label="Dox_0.1"
files="localtest/LacI-CAGop_B10_B10_P3.fcs"

container_exec ${CONTAINER_IMAGE} python /opt/scripts/fc.py --label ${label} \
 --octave-method-path /opt/scripts/ \
 --files ${files} \
 --type ${type} \
 --output "local.output.txt"
