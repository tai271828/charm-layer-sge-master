export CHARM_NAME := sge-master
export CHARM_BUILD_DIR ?= ../../build
export JUJU_MODEL := sge-solvcon

# Makefile Targets
# clean model deployement
deploy-clean-model: build redeploy-model

redeploy-model:
	juju destroy-model $(JUJU_MODEL) -y
	juju add-model $(JUJU_MODEL)
	#juju switch $(JUJU_MODEL)
	# to support GCE (LP: #1761838). for maas it does not matter to tweak
	# the model in this way or not.
	juju model-config fan-config="" container-networking-method=""
	juju deploy $(CHARM_BUILD_DIR)/$(CHARM_NAME) --series xenial
	# you may want to use --constraints tags=virtual for MaaS cloud
	# because MaaS supports KVM pods
	#juju deploy $(CHARM_BUILD_DIR)/$(CHARM_NAME) --series xenial --constraints tags=virtual

deploy: build
	juju deploy $(CHARM_BUILD_DIR)/$(CHARM_NAME) --series xenial

build: clean
	tox -e build

clean:
	rm -rf .tox/
	rm -rf $(CHARM_BUILD_DIR)/$(CHARM_NAME)

# publish the built charm
publish: build republish

republish:
	$(eval published_url := $(shell charm push $(CHARM_BUILD_DIR)/$(CHARM_NAME) | grep url | awk {'print $$2'}))
	charm release $(published_url)
