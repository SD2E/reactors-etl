CONTAINER_IMAGE="sd2e/lcms-pyquant-0.1.1:latest"

. _util/container_exec.sh

COMMAND='pyQuant'

PARAMS=''
if [ -z "${search_file}" ]
then
    PARAMS='${PARAMS} --search-file ${search_file}'
fi

if [ -z "${scan_file_dir}" ]
then
    PARAMS='${PARAMS} --scan-file-dir ${scan_file_dir}'
fi

if [ -z "${scan_file}" ]
then
    PARAMS='${PARAMS} --scan-file ${scan_file}'
fi

if [ -z "${label_method}" ]
then
    PARAMS='${PARAMS} --label-method ${label_method}'
fi

if [ -z "${isobaric_tags}" ]
then
    PARAMS='${PARAMS} --isobaric-tags'
fi

if [ -z "${html_output}" ]
then
    PARAMS='${PARAMS} --html'
fi

if [ -z "${msn_peaklist}" ]
then
    PARAMS='${PARAMS} --msn-peaklist ${msn_peaklist}'
fi

echo ${PARAMS}

container_exec ${CONTAINER_IMAGE} ${COMMAND} ${PARAMS}
