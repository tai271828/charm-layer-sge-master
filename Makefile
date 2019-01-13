export CHARM_NAME := sge-master
export CHARM_BUILDING := ./built-charms
export CHARM_BUILD_DIR := ${CHARM_BUILDING}/xenial

# Makefile Targets
deploy-clean-model: build
	juju destroy-model sge-sandbox -y; juju add-model sge-sandbox; juju switch sge-sandbox
	juju deploy $(CHARM_BUILD_DIR)/$(CHARM_NAME) --series xenial

deploy: build
	juju deploy $(CHARM_BUILD_DIR)/$(CHARM_NAME) --series xenial

build: clean
	tox -e build

clean:
	rm -rf .tox/
	rm -rf ${CHARM_BUILDING}
