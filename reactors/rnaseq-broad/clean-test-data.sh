#!/usr/bin/env bash
# Path to app bundle
APP=$1
DEST=${2-localtest}

TEST_DATA_CACHE=${TEST_DATA_CACHE:-test-data-cache}

if [ ! -d "$APP/test" ]
then
    echo "Can't find or access $APP/test. Re-run $0 <app> <destpath>"
fi

function clean_data() {

    local APATH=$1
    local RECURSE=
    rm -rf $APP/test/*
    find . -name .dirty -exec rm {} \;

}

clean_data "${APP}"
