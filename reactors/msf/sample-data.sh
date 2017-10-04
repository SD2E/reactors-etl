#!/usr/bin/env bash

files-mkdir -N msf -S data-sd2e-community sample/
files-upload -F msf-0.1.0/localtest/exp2801-04-ds731218.msf -S data-sd2e-community sample/msf/
files-pems-update -u world -p READ -S data-sd2e-community -R sample/msf
files-pems-update -u public -p READ -S data-sd2e-community -R sample/msf
