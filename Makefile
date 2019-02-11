export CHARM_NAME := sge-master
export CHARM_BUILD_DIR ?= ../../build

# Makefile Targets
# clean model deployement
deploy-clean-model: build
	juju destroy-model sge-sandbox -y; juju add-model sge-sandbox; juju switch sge-sandbox
	juju deploy $(CHARM_BUILD_DIR)/$(CHARM_NAME) --series xenial --constraints tags=virtual

deploy: build
	juju deploy $(CHARM_BUILD_DIR)/$(CHARM_NAME) --series xenial

build: clean
	tox -e build

clean:
	rm -rf .tox/
	rm -rf $(CHARM_BUILD_DIR)/$(CHARM_NAME)
