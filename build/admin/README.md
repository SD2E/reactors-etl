# Building SD2E Reactor base Docker images

1. Make any required changes to assets in `build/admin/docker`
2. `cd ../../` - Go to the top level project directory
3. . config.rc - Source the configuration variables
4. `make docker-base-build` - Build base images
5. To change the version tag, increment VERSION and re-run `make docker-base-build`
6. `make docker-base-release` - Push to Docker Hub

