#!/usr/bin/env bash
# Path to app bundle
APP=$1
DEST=${2-localtest}

TEST_DATA_CACHE=${TEST_DATA_CACHE:-test-data-cache}

if [ ! -d "$APP/$DEST" ]
then
    echo "Can't find or access $APP/$DEST. Re-run $0 <app> <destpath>"
fi

function clean_data() {

    local APATH=$1
    local RECURSE=
    rm -rf $APP/$DEST/*
    find . -name .dirty -exec rm {} \;

}

clean_data "${APP}"