
function container_exec() {
    
    # [TODO] Check for existence of docker or singularity executable
    # [TODO] Enable honoring a DEBUG global
    # [TODO] Figure out how to accept more optional arguments (env-file, etc)
    # [TODO] Better error handling and reporting

    local CONTAINER_IMAGE=$1
    shift
    local COMMAND=$1
    shift
    local PARAMS=$@

    echo $CONTAINER_IMAGE
    echo $COMMAND
    echo $PARAMS

    if [ -z "$SINGULARITY_PULLFOLDER" ];
    then
        if [ ! -z "$STOCKYARD" ];
        then
            SINGULARITY_PULLFOLDER="${STOCKYARD}/.singularity"
        else
            SINGULARITY_PULLFOLDER="$HOME/.singularity"
        fi
    fi

    if [ -z "$SINGULARITY_CACHEDIR" ];
    then
        if [ ! -z "$STOCKYARD" ];
        then
            SINGULARITY_CACHEDIR="${STOCKYARD}/.singularity"
        else
            SINGULARITY_CACHEDIR="$HOME/.singularity"
        fi
    fi

    if [[ "$_CONTAINER_ENGINE" == "docker" ]];
    then
        local OPTS="-v $PWD:/home:rw -w /home --rm=true"
        if [ ! -z "$ENVFILE" ]
        then
            OPTS="$OPTS --env-file ${ENVFILE}"
        fi
        set -x
        docker run $OPTS ${CONTAINER_IMAGE} ${COMMAND} ${PARAMS}
        set +x
    elif [[ "$_CONTAINER_ENGINE" == "singularity" ]];
    then
        # [TODO] Detect if a .img has been passed it (rare)
        # [TODO]
        singularity exec docker://${CONTAINER_IMAGE} ${COMMAND} ${PARAMS}
    else
        echo "_CONTAINER_ENGINE needs to be 'docker' or 'singularity' [$_CONTAINER_ENGINE]"
    fi

}
