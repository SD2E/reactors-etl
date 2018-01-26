CONTAINER_IMAGE="sd2e/dataframe-prod-0.1.0:latest"

. _util/container_exec.sh

COMMAND='pyQuant'
PARAMS='--config ${config_json} -o ${output}'

container_exec ${CONTAINER_IMAGE} ${COMMAND} ${PARAMS}
