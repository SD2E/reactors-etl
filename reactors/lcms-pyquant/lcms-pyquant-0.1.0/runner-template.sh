CONTAINER_IMAGE="sd2e/lcms-pyquant-0.1.0:latest"

. _util/container_exec.sh

COMMAND='pyQuant'
PARAMS='--search-file ${search_file} --isobaric-tags --label-method TMT10 --no-ratios -o ${output} -p9'

container_exec ${CONTAINER_IMAGE} ${COMMAND} ${PARAMS}
