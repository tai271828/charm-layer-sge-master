import os
import shutil
from subprocess import check_call

__all__ = ['bootstrap_pre_sge_master', 'get_installed_message']

def bootstrap_pre_sge_master():
    # prepare basic configuration files and scripts
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


def add_worker(worker, slot=1):
    cmd = ['/usr/local/sbin/sge-init-conf.sh', 'homemade.q',  worker, slot]
    check_call(cmd)


def get_installed_message():
    return 'SGE master is installed'

