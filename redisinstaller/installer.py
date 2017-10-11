import os
import subprocess
import pycurl
import shutil
from jinja2 import Environment, FileSystemLoader
from pyunpack import Archive
from git import Repo


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


def install_redis_json():
    install_prefix = os.environ['VIRTUAL_ENV']
    assert install_prefix is not None, "Running from outside a virtual environment not supported"

    so_name = 'rejson.so'
    rejson_file_dest = os.path.join(install_prefix, 'lib', so_name)
    if not os.path.exists(rejson_file_dest):
        build_root = '/tmp'
        build_dir = os.path.join(build_root, 'rejson')
        Repo.clone_from('https://github.com/RedisLabsModules/rejson.git', build_dir)

        os.chdir(build_dir)

        result = subprocess.run(['make', '-j5'])
        assert result.returncode == 0

        shutil.copyfile(os.path.join(build_dir, 'src', so_name), rejson_file_dest)
    else:
        print("rejson is already installed")


def generate_config():
    install_prefix = os.environ['VIRTUAL_ENV']
    assert install_prefix is not None, "Running from outside a virtual environment not supported"
    env = Environment(loader=FileSystemLoader('config'))

    template = env.get_template("redis.conf.jinja")
    so_name = 'rejson.so'
    rejson_module_path = os.path.join(install_prefix, 'lib', so_name)
    rendered_data = template.render(rejson_module_path=rejson_module_path)

    with open('config/redis.conf', 'w') as f:
        f.write(rendered_data)
