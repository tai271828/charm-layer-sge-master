import subprocess as sp
from charms.reactive import when, when_not, set_flag
from charms.reactive.relations import endpoint_from_flag
from charmhelpers.core import hookenv
from charmhelpers.core.hookenv import application_version_set, status_set
from charmhelpers.fetch import get_upstream_version
from charms.layer import sge_master


@when('apt.installed.gridengine-master')
@when('apt.installed.gridengine-client')
@when('apt.installed.gridengine-common')
@when('apt.installed.gridengine-exec')
@when('apt.installed.gridengine-qmon')
@when_not('sge-master.installed')
def install_sge_layer():
    sge_master.bootstrap_pre_sge_master()

    # Set the upstream version of hello for juju status.
    application_version_set(get_upstream_version('gridengine-master'))

    # Signal that we know the version
    set_flag('gridengine-master.version.set')
    # Signal that the sge-master is installed
    set_flag('sge-master.installed')

    # Set the active status with the message
    status_set('active', sge_master.get_installed_message())


@when('endpoint.master-config-provider.joined')
def publish_host_info():
    endpoint_master = endpoint_from_flag('endpoint.master-config-provider.joined')
    print(dir(hookenv))
    print(hookenv.unit_public_ip())
    print(hookenv.unit_private_ip())
    endpoint_master.publish_info(hookenv.unit_public_ip())

