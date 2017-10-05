include config.mk

PREFIX := $(HOME)

TENANT_NAME := $(TENANT_NAME)
TENANT_KEY := $(TENANT_KEY)
TENANT_DOCKER_ORG := $(TENANT_DOCKER_ORG)
OBJ := $(MAKE_OBJ)
SOURCES = customize

.SILENT: test
test:
	echo "Not implemented"

help:
	echo "You can run docker-base-build, docker-base-release, and docker-base-clean"

docker-base-build:
	build/admin/baseimages.sh $(TENANT_DOCKER_ORG) $(SYSTEM_VERSION) build && \
	touch .docker-base-build

docker-base-release: .docker-base-build
	build/admin/baseimages.sh $(TENANT_DOCKER_ORG) $(SYSTEM_VERSION) release

docker-base-clean:
	build/admin/baseimages.sh $(TENANT_DOCKER_ORG) $(SYSTEM_VERSION) clean && \
	rm -f .docker-base-build

