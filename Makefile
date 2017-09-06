sdk_version := $(shell cat VERSION)
api_version := v2
api_release := 2.2.5

PREFIX := $(HOME)

TENANT_NAME := $(TENANT_NAME)
TENANT_KEY := $(TENANT_KEY)
TENANT_DOCKER_ORG := $(TENANT_DOCKER_ORG)
OBJ := $(MAKE_OBJ)
SOURCES = customize

.SILENT: test
test:
	echo "Not implemented"

docker-base-build:
	build/admin/baseimages.sh $(TENANT_DOCKER_ORG) $(sdk_version) build && \
	touch .docker-base-build

docker-base-release: .docker-base-build
	build/admin/docker.sh $(TENANT_DOCKER_ORG) $(sdk_version) release

docker-base-clean:
	build/admin/baseimages.sh $(TENANT_DOCKER_ORG) $(sdk_version) clean && \
	rm -f .docker-base-build

