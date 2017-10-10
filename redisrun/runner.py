import subprocess

import os


def run_redis():
    install_prefix = os.environ['VIRTUAL_ENV']

    result = subprocess.run(['{}/bin/redis-server'.format(install_prefix), '-j5'])
    assert result.returncode == 0
