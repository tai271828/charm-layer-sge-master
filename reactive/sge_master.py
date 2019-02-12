import subprocess as sp
from charms.reactive import when, when_not, set_flag, clear_flag, get_flags
from charms.reactive.relations import endpoint_from_flag
from charmhelpers.core import hookenv
from charmhelpers.core.hookenv import application_version_set, status_set
from charmhelpers.fetch import get_upstream_version
from charms.layer import sge_master


CLIENT_ADDRESS_PATH = '/home/ubuntu/mpi_host_list'


@when('apt.installed.gridengine-master')
@when('apt.installed.gridengine-client')
@when('apt.installed.gridengine-common')
@when('apt.installed.gridengine-exec')
@when('apt.installed.gridengine-qmon')
@when('apt.installed.mpich')
@when('apt.installed.nfs-kernel-server')
@when_not('sge-master.installed')
def install_sge_master():
    # workaround for MaaS cloud
    sge_master.deb_719621_workaround(hookenv.unit_public_ip())
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
    #cmd = ['mkdir', '-p', '/usr/share/charm-sge-cluster/']
    #sp.check_call(cmd)
    cc = endpoint_from_flag('endpoint.config-exchanger.new-exchanger')
    client_config = cc

    with open(CLIENT_ADDRESS_PATH, 'wt') as fout:
        for client in client_config.exchangers():
            hookenv.log('client: {}'.format(client['hostname']))
            fout.write(client['hostname'] + "\n")

            sge_master.connect_sge_client(client['hostname'])

    sge_master.publish_mpi_hosts_info()
    set_flag('sge-master.mpi-cluster.host-info.published')
    hookenv.log('Set flag: sge-master.mpi-cluster.host-info.published')
    all_flags = get_flags()
    hookenv.log('All flags now: {}'.format(all_flags))

    clear_flag('endpoint.config-exchanger.new-exchanger')


@when('endpoint.config-exchanger.joined')
def publish_host_info():
    endpoint_master = endpoint_from_flag('endpoint.config-exchanger.joined')
    endpoint_master.publish_info(hostname=hookenv.unit_public_ip())


@when('sge-master.mpi-cluster.host-info.published')
def publish_mpi_cluster_info():
    mpi_hosts = []
    with open(CLIENT_ADDRESS_PATH, 'rt') as fin:
        lines = fin.readlines()
        for line in lines:
            # should be an IP address so there are 4 digits at least (IPv4)
            ls = line.strip()
            if len(ls) > 4:
                mpi_hosts.append(line)

    endpoint_master = endpoint_from_flag('endpoint.config-exchanger.joined')
    endpoint_master.publish_info_mpi(mpi_hosts=mpi_hosts)

