#!/usr/bin/env bash

# This is a prototype of a runner that will eventually read the app.yml and 
# prestage test data in a local cache directory for use in local development

TEST_DATA_CSV=${TEST_DATA_CSV:-test-data.tsv}
TEST_DATA_CACHE=${TEST_DATA_CACHE:-test-data-cache}

auth-tokens-refresh -q -S > /dev/null 2>&1

mkdir -p ${TEST_DATA_CACHE}

function _import_agave_uri() {

    local SRC=$1
    local DEST=$2

    local ASYS=$(get_agave_system $SRC)
    local APATH=$(get_agave_path $SRC)
    local AFNAME=$(get_agave_fname $SRC)
    local RECURSE=
    case "$APATH" in
        */)
            RECURSE="--recursive "
            ;;
        *)
            RECURSE=""
            ;;
    esac

    files-get "${RECURSE}" -S "${ASYS}" -N "${DEST}" "${APATH}"

}

function _import_public_uri() {

    local SRC=$1
    local DEST=$2
    echo "Not implemented"
}

function get_agave_fname() {

    local AGAVE_URI=$1
    # remove the protocol
    local url=$(echo $AGAVE_URI | sed -e s,"agave://",,g)
    local afile=$(echo "${url##*/}")
    echo $afile

}

function get_agave_path() {

    local AGAVE_URI=$1

    # remove the protocol
    local url=$(echo $AGAVE_URI | sed -e s,"agave://",,g)
    local apath=$(echo "${url#*/}")
    echo $apath

}

function get_agave_system() {

    local AGAVE_URI=$1

    # remove the protocol
    local url=$(echo $AGAVE_URI | sed -e s,"agave://",,g)
    local sysid=$(awk -F '/' '{print $1}' <<< $url)
    echo $sysid

}

function get_uri_scheme() {

    local URL=$1
    proto="$(echo $1 | grep :// | sed -e's,^\(.*://\).*,\1,g' | tr -d /\// | tr -d :)"
    echo $proto

}


function die() {

    mesg "ERROR" $1 
    exit 1
}

function warn() {

    mesg "WARNING" $1 
}

function log() {

    mesg "INFO" $1
}

function mesg() {

    level=$1
    shift
    message=$@
    echo "[$level] $message"
}

function import_uri() {

    local SRC=$1
    local DEST=$2

    if [ ! -e "${TEST_DATA_CACHE}/${DEST}" ]
    then
    
        local scheme=$(get_uri_scheme $SRC)

        case $scheme in
            agave)
                _import_agave_uri "${SRC}" "${TEST_DATA_CACHE}/${DEST}"
                ;;
            http|https)
                _import_public_uri "${SRC}" "${TEST_DATA_CACHE}/${DEST}"
                ;;
            *)
                warn "URI scheme $scheme not recognized"
                ;;
        esac

    else
        warn "${TEST_DATA_CACHE}/$DEST exists. Delete it or re-run with FORCE=1."
    fi

}

while read dat; do
  SOURCE_URI=$(awk '{ print $1 }' <<< $dat)
  DEST_PATH=$(awk '{ print $2 }' <<< $dat)
  log "Importing $SOURCE_URI"
  import_uri $SOURCE_URI $DEST_PATH
done <${TEST_DATA_CSV}
