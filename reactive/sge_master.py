import subprocess as sp

from charms.reactive import when, when_not, set_flag
from charmhelpers.core.hookenv import application_version_set, status_set
from charmhelpers.fetch import get_upstream_version

from charms.layer import sge_master

@when_not('sge-master.installed')
def install_sge_layer():
    # Do your setup here.
    #
    # If your charm has other dependencies before it can install,
    # add those as @when() clauses above., or as additional @when()
    # decorated handlers below
    #
    # See the following for information about reactive charms:
    #
    #  * https://jujucharms.com/docs/devel/developer-getting-started
    #  * https://github.com/juju-solutions/layer-basic#overview
    #
    set_flag('sge-master.installed')

@when('apt.installed.gridengine-master')
@when('apt.installed.gridengine-client')
@when('apt.installed.gridengine-common')
@when('apt.installed.gridengine-exec')
@when('apt.installed.gridengine-qmon')
def set_unit_ready_message():
    sge_master.bootstrap_pre_sge_master()

    # Set the upstream version of hello for juju status.
    application_version_set(get_upstream_version('gridengine-master'))

    # Run hello and get the message
    #message = sp.check_output('hello', stderr=sp.STDOUT)

    # Set the active status with the message
    status_set('active', sge_master.get_installed_message())

    # Signal that we know the version of hello
    #set_flag('hello.version.set')

