import subprocess as sp

from charms.reactive import when, when_not, set_flag
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

    # Set the active status with the message
    status_set('active', sge_master.get_installed_message())

    # Signal that we know the version
    set_flag('gridengine-master.version.set')

    set_flag('sge-master.installed')

