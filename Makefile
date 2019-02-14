export CHARM_NAME := sge-master
export CHARM_BUILD_DIR ?= ../../build

# Makefile Targets
# clean model deployement
deploy-clean-model: build
	juju destroy-model sge-sandbox -y; juju add-model sge-sandbox; juju switch sge-sandbox
	# to support GCE (LP: #1761838). for maas it does not matter to tweak
	# the model in this way or not. btw you may want to use --constraints
	# tags=virtual for MaaS cloud.
	juju model-config fan-config="" container-networking-method=""
	juju deploy $(CHARM_BUILD_DIR)/$(CHARM_NAME) --series xenial

redeploy-model:
	juju destroy-model sge-sandbox -y; juju add-model sge-sandbox; juju switch sge-sandbox
	# to support GCE (LP: #1761838). for maas it does not matter to tweak
	# the model in this way or not. btw you may want to use --constraints
	# tags=virtual for MaaS cloud.
	juju model-config fan-config="" container-networking-method=""
	juju deploy $(CHARM_BUILD_DIR)/$(CHARM_NAME) --series xenial

deploy: build
	juju deploy $(CHARM_BUILD_DIR)/$(CHARM_NAME) --series xenial

build: clean
	tox -e build

clean:
	rm -rf .tox/
	rm -rf $(CHARM_BUILD_DIR)/$(CHARM_NAME)
