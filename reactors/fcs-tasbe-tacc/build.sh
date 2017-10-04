DOCKER_IMAGE="sd2e/fcs:0.0.6"

docker build -t ${DOCKER_IMAGE} . ; docker push ${DOCKER_IMAGE}
