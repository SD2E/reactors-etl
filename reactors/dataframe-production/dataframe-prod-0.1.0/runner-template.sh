CONTAINER_IMAGE="sd2e/dataframe-prod-0.1.0:latest"

. _util/container_exec.sh

container_exec ${CONTAINER_IMAGE} /opt/scripts/dataframe-prod.sh ${config_json} ${output}
