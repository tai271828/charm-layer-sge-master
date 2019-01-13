import shutil

__all__ = ['bootstrap_pre_sge_master', 'get_installed_message']

def bootstrap_pre_sge_master():
    shutil.copy2('bin/sge-add-work.sh', '/usr/local/sbin/')

def get_installed_message():
    return 'SGE master is installed'

