import os
import shutil
import subprocess as sp
from subprocess import check_call
from charmhelpers.core import hookenv

__all__ = ['bootstrap_pre_sge_master', 'get_installed_message']


def bootstrap_pre_sge_master():
    # for MPI cluster
    # We make the SGE master is the head node of the cluster as well
    _setup_nfs_server_dir()

    # prepare basic configuration files and scripts for SGE master
    dir_bin = '/usr/local/sbin/'
    shutil.copy2('bin/sge-init-conf.sh', dir_bin)
    shutil.copy2('bin/sge-add-work.sh', dir_bin)

    dir_sge = '/usr/share/charm-sge-cluster/'
    cmd = ['mkdir', '-p', dir_sge]
    check_call(cmd)
    shutil.copy2('data/scheduler.conf', dir_sge)
    shutil.copy2('data/hostlist.conf', dir_sge)
    shutil.copy2('data/queue.conf', dir_sge)

    cmd = os.path.join(dir_bin, 'sge-init-conf.sh')
    check_call(cmd)


def connect_sge_client(hostname_address):
    _add_worker(hostname_address)
    _setup_ssh_key_over_nodes(hostname_address)


def aggregate_mpi_hosts():
    _setup_mpi_cluster()


def _add_worker(worker, slot=1):
    print("Add worker: {}".format(worker))
    cmd = ['/usr/local/sbin/sge-add-work.sh', 'homemade.q',  worker, str(slot)]
    check_call(cmd)


def get_installed_message():
    return 'SGE master is installed'


def deb_719621_workaround(host_address):
    """
    Apply the workaround for bug #719621 of deb distro.

    Many deb-based distributions apply a workaround for bug #719621 by adding a
    line to loopback FQDN with 127.0.1.1. The debian manual 5.1.1. The hostname
    resolution suggests to use a permanent IP address if the IP is available.

    This function will try to find out the workaround IP 127.0.1.1 and replace
    the workaround IP with the target permanent IP. Otherwise SGE will be
    confused with where to find out the master node when configuring queues
    etc.
    """
    target_file = '/etc/hosts'
    ip_old = '127.0.1.1'
    ip_new = host_address
    with open(target_file, 'rt') as fin:
        text = fin.read().replace(ip_old, ip_new)

    with open(target_file, 'wt') as fout:
        fout.write(text)

    # should be skipped because when juju add-relation
    # the client grid engine will restart and it works
    # restart_systemd_service(networking.service)


def _setup_nfs_server_dir(dir_name='mpi_nfs_mnt'):
    dir_abs = '/home/ubuntu/' + dir_name
    cmd = ['mkdir', dir_abs]
    check_call(cmd)

    cmd = ['chown', 'ubuntu', dir_abs]
    check_call(cmd)

    lt = dir_abs + ' *(rw,sync,no_root_squash,no_subtree_check)'
    insert_line_in_file(lt, '/etc/exports')

    cmd = ['exportfs', '-a']
    check_call(cmd)


def _setup_mpi_cluster():
    source = '/usr/share/charm-sge-cluster/client_address'
    destination = '/home/ubuntu/host_file'
    cmd = 'cp ' + source + ' ' + destination
    sp.run(cmd, shell=True)

    with open('/home/ubuntu/host_file', 'at') as fout:
        fout.write(hookenv.unit_public_ip() + "\n")

    # TODO: could be done for only once. no need to create this file each time
    with open('/etc/profile.d/mpi-host-file.sh', 'w') as fout:
        fout.write('export MPI_HOSTS=/home/ubuntu/host_file' + "\n")


def _setup_ssh_key_over_nodes(address):
    cmd = 'mkdir /home/ubuntu/.ssh; chmod 700 /home/ubuntu/.ssh/'
    sp.run(cmd, shell=True)

    cmd = 'ssh-keygen -t rsa -f /home/ubuntu/.ssh/id_rsa -N ""'
    sp.run(cmd, shell=True)

    destination = '/home/ubuntu/.ssh/authorized_keys'
    cmd = 'cat /home/ubuntu/.ssh/id_rsa.pub >> ' + destination
    sp.run(cmd, shell=True)

    cmd = 'chmod 600 /home/ubuntu/.ssh/authorized_keys'
    sp.run(cmd, shell=True)

    cmd = 'sh-keyscan -t rsa localhost >> /home/ubuntu/.ssh/known_hosts'
    sp.run(cmd, shell=True)

    cmd = 'ssh-keyscan -t rsa 127.0.0.1 >> /home/ubuntu/.ssh/known_hosts'
    sp.run(cmd, shell=True)

    cmd = 'ssh-keyscan -t rsa ' + address + ' >> /home/ubuntu/.ssh/known_hosts'
    sp.run(cmd, shell=True)

    cmd = 'chown ubuntu -R /home/ubuntu/.ssh'
    sp.run(cmd, shell=True)

    # TODO: silliy and security concern method. change me later by publish_info
    cmd = 'mkdir /home/ubuntu/mpi_nfs_mnt/keys; '
    cmd = cmd + 'cp /home/ubuntu/.ssh/id_rsa* /home/ubuntu/mpi_nfs_mnt/keys/'
    sp.run(cmd, shell=True)


def get_public_key():
    with open('/home/ubuntu/.ssh/id_rsa.pub', 'rt') as fin:
        key = fin.read()
    return key


def insert_line_in_file(line_target, file_target):
    with open(file_target, 'rt') as fin:
        text = fin.read()

    text = text + line_target + "\n"

    with open(file_target, 'wt') as fout:
        fout.write(text)


def restart_systemd_service(service):
    cmd = ['systemctl', 'restart', service]
    check_call(cmd)

