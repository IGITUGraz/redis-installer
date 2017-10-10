import os
import subprocess
import pycurl
from pyunpack import Archive


def install_redis():
    install_prefix = os.environ['VIRTUAL_ENV']
    assert install_prefix is not None, "Running from outside a virtual environment not supported"

    if not os.path.exists(os.path.join(install_prefix, 'bin', 'redis-server')):
        # As long as the file is opened in binary mode, both Python 2 and Python 3
        # can write response body to it without decoding.
        redis_unpacked_root = '/tmp'
        redis_archive_path = os.path.join(redis_unpacked_root, 'redis-stable.tar.gz')
        redis_unpacked_path = os.path.join(redis_unpacked_root, 'redis-stable')
        with open(redis_archive_path, 'wb') as f:
            c = pycurl.Curl()
            c.setopt(c.URL, 'http://download.redis.io/redis-stable.tar.gz')
            c.setopt(c.WRITEDATA, f)
            c.perform()
            c.close()

        Archive(redis_archive_path).extractall(redis_unpacked_root)

        os.chdir(redis_unpacked_path)

        result = subprocess.run(['make', '-j5'])
        assert result.returncode == 0

        result = subprocess.run(['make', 'PREFIX={}'.format(install_prefix), 'install'])
        assert result.returncode == 0
    else:
        print("redis-server already installed")
