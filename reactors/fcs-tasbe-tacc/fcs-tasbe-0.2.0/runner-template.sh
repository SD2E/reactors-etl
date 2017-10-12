# Allow over-ride
if [ -z "${CONTAINER_IMAGE}" ]
then
    version=$(cat VERSION)
    CONTAINER_IMAGE="index.docker.io/sd2e/fcs:$version"
fi
. _util/container_exec.sh

function log(){
    mesg "INFO" $@
}

function die() {
    mesg "ERROR" $@
    # AGAVE_JOB_CALLBACK_FAILURE is macro populated at runtime 
    # by the platform and gives us an eject button from
    # anywhere the application is running
    ${AGAVE_JOB_CALLBACK_FAILURE}
}

function mesg() {
    lvl=$1
    shift
    message=$@
    echo "[$lvl] $(utc_date) - $message"
}

function utc_date() {
    echo $(date -u +"%Y-%m-%dT%H:%M:%SZ")
}

#### BEGIN SCRIPT LOGIC
# Assumptions
#
# <inputData> can be a directory - agave://data-sd2e-community/sample/fcs-tasbe/Q0-ProtStab-BioFab-Flow_29092017
# <inputData> can be a compressed directory - agave://data-sd2e-community/sample/fcs-tasbe/Q0-ProtStab-BioFab-Flow_29092017.[zip|tgz]
# fc.json is inside <inputData>
# fc.json might still have hard-coded /data/ paths 
# fc.json should be minimally validated

OWD=$PWD
# Predicted directory. Saem as inputData if not archive
inputDir=$(basename ${inputData} .zip)

# Allow user to pass in an override fc.json file
fcFilename="fc.json"
if [ ! -z "${fcOverride}" ]
then
    log "Override specified: ${fcOverride}"
    if [ "${fcOverride}" == "fc.json" ]
    then
       fcFilename="$RANDOM-fc.json"
       mv "fc.json" "${fcFilename}"
    else
       fcFilename=${fcOverride}
    fi
    log "Override actual: ${fcFilename}"
fi

# Double check existence of inputData
if [ ! -e "${inputData}" ];
then
    die "inputData ${inputData} not found or accesible"
fi

# is inputData a zip archive?
# If so, unzip it, ignoring MacOSX line noise
if [[ ${inputData} == *.zip ]]
then
    unzip -q -o ${inputData} -x "*.DS_Store" "*__MACOSX*" && rm -rf ${inputData} || die "Error unzipping/removing $inputData"
fi

# By now, we should have a decent chance of having a directory of Flow data
if [ -d "${inputDir}" ]
then
    # Add contents of inputDir to .agave.archive
    # Why? Because we don't need to copy the inputs
    # back out at the end. This file is used by
    # Agave to mark files for omission during the
    # "archive" step
    for A in $(find ${inputDir})
    do
        echo "${A#*/}" >> .agave.archive
    done
    # Move contents of inputDir up to run-level 
    # directory and delete the original directory 
    mv ${inputDir}/* . && rm -rf ${inputDir} || die "Couldn't move files for processing"
fi

# Remove residual hard-coded /data/ paths from fc.json
# as they're just an artifact of early containerization
# efforts and are completely deprecated
if [ -f "${fcFilename}" ];
then
    sed -e 's/\/data\//.\//g' -i'.bak' "${fcFilename}" || die "Error correcting paths in ${fcFilename}"
else
    die "Could not find or access ${fcFilename}"
fi

# Do more validation on fc.json
# Noop for now - assume it's fine

# We have not failed yet. Systems are probably nominal.
# Kick off the analysis 
container_exec ${CONTAINER_IMAGE} python /opt/src/fc.py \
    --octave-method-path /opt/src/ \
    --config "${fcFilename}"

