#!/bin/bash

CONFIG_FILE=${1}
OUTPUT=${2}

python /opt/py/dataframe-prod.py --config $CONFIG_FILE -o $OUTPUT
