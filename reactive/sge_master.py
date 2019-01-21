import subprocess as sp
from charms.reactive import when, when_not, set_flag, clear_flag
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
def install_sge_master():
    sge_master.bootstrap_pre_sge_master()

    # Set the upstream version of hello for juju status.
    application_version_set(get_upstream_version('gridengine-master'))

    # Signal that we know the version
    set_flag('gridengine-master.version.set')
    # Signal that the sge-master is installed
    set_flag('sge-master.installed')

    # Set the active status with the message
    status_set('active', sge_master.get_installed_message())


@when('endpoint.config-exchanger.new-exchanger')
def update_client_config():
    cmd = ['mkdir', '-p', '/usr/share/charm-sge-cluster/']
    sp.check_call(cmd)
    client_config = endpoint_from_flag('endpoint.config-exchanger.new-exchanger')
    for client in client_config.exchangers():
        hookenv.log('client: {}'.format(client['hostname']))

        filename = '/usr/share/charm-sge-cluster/client_address'
        with open(filename, 'a') as fout:
            fout.write(client['hostname'] + "\n")

        sge_master.connect_sge_client(client['hostname'])

    clear_flag('endpoint.config-exchanger.new-exchanger')


@when('endpoint.config-exchanger.joined')
def publish_host_info():
    endpoint_master = endpoint_from_flag('endpoint.config-exchanger.joined')
    endpoint_master.publish_info(hookenv.unit_public_ip())

