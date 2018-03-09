#!/usr/bin/env bash

# Path to app bundle
APP=$1
DEST=${2-test}

# If you want to stage in only a subset of data, create another TSV file
# and override TEST_DATA_CSV variable at run time
TEST_DATA_CSV=${TEST_DATA_CSV:-test-data.tsv}
TEST_DATA_CACHE=${TEST_DATA_CACHE:-test-data-cache}

mkdir -p $APP/test

function stage_data() {

    local APATH=$1
    local RECURSE=

    case "$APATH" in
        */)
            RECURSE="-R "
            ;;
        *)
            RECURSE=""
            ;;
    esac
    cp -Rf $APATH $APP/test ; touch "$APP/test/.dirty"

}

while read dat; do
  SOURCE_URI=$(awk '{ print $1 }' <<< $dat)
  DEST_PATH=$(awk '{ print $2 }' <<< $dat)
  stage_data $TEST_DATA_CACHE/$DEST_PATH
done <${TEST_DATA_CSV}
