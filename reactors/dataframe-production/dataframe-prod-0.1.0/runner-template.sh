CONTAINER_IMAGE="sd2e/dataframe-prod-0.1.0:latest"

# . _util/container_exec.sh
# Temporary - once this code stabilizes it will come bundled with the
# tacc-singularity module
chmod a+x ./_util/contained
ls >> .agave.archive

CONTAINED_NOCACHE=1 ; ./_util/contained run ${CONTAINER_IMAGE} /opt/scripts/dataframe-prod.sh ${config_json} ${output}
