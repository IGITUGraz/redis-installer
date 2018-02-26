import subprocess

import os
import shutil

REDIS_PORT = 65535


def get_install_prefix():
    install_prefix = os.environ.get('VIRTUAL_ENV')
    if install_prefix is None:
        print("Installing to user home ~/.local")
        install_prefix = os.path.expanduser('~/.local')
    return install_prefix


def install_redis():
    from pyunpack import Archive

    install_prefix = get_install_prefix()

    if not os.path.exists(os.path.join(install_prefix, 'bin', 'redis-server')):
        # As long as the file is opened in binary mode, both Python 2 and Python 3
        # can write response body to it without decoding.
        redis_unpacked_root = '/tmp'
        redis_archive_path = os.path.join(redis_unpacked_root, 'redis-4.0.8.tar.gz')
        redis_unpacked_path = os.path.join(redis_unpacked_root, 'redis-4.0.8')

        if not os.path.exists(redis_archive_path):
            import pycurl

            ## Download the archive
            with open(redis_archive_path, 'wb') as f:
                c = pycurl.Curl()
                c.setopt(c.URL, 'http://download.redis.io/releases/redis-4.0.8.tar.gz')
                c.setopt(c.WRITEDATA, f)
                c.perform()
                c.close()

        Archive(redis_archive_path).extractall(redis_unpacked_root)

        current_path = os.path.realpath(os.getcwd())
        os.chdir(redis_unpacked_path)

        result = subprocess.run(['make', '-j5'])
        assert result.returncode == 0

        result = subprocess.run(['make', 'PREFIX={}'.format(install_prefix), 'install'])
        assert result.returncode == 0
        os.chdir(current_path)
    else:
        print("redis-server already installed")


def install_redis_json():
    from pyunpack import Archive

    install_prefix = get_install_prefix()

    so_name = 'rejson.so'
    rejson_file_dest = os.path.join(install_prefix, 'lib', so_name)
    if not os.path.exists(rejson_file_dest):
        rejson_unpacked_root = '/tmp'
        rejson_archive_path = os.path.join(rejson_unpacked_root, 'rejson-v1.0.1.tar.gz')
        rejson_unpacked_path = os.path.join(rejson_unpacked_root, 'rejson-1.0.1')

        if not os.path.exists(rejson_archive_path):
            import pycurl

            ## Download the archive
            with open(rejson_archive_path, 'wb') as f:
                c = pycurl.Curl()
                c.setopt(pycurl.FOLLOWLOCATION, 1)  # Follow redirects
                c.setopt(c.URL, 'https://github.com/RedisLabsModules/rejson/archive/v1.0.1.tar.gz')
                c.setopt(c.WRITEDATA, f)
                c.perform()
                c.close()

        Archive(rejson_archive_path).extractall(rejson_unpacked_root)

        current_path = os.path.realpath(os.getcwd())
        os.chdir(rejson_unpacked_path)

        result = subprocess.run(['make', '-j5'])
        assert result.returncode == 0

        shutil.copyfile(os.path.join(rejson_unpacked_path, 'src', so_name), rejson_file_dest)
        os.chdir(current_path)
    else:
        print("rejson is already installed")


def generate_config():
    print("Generating config file")
    from jinja2 import Environment, FileSystemLoader

    install_prefix = get_install_prefix()

    env = Environment(loader=FileSystemLoader('./config'))

    template = env.get_template("redis.conf.jinja")
    so_name = 'rejson.so'
    rejson_module_path = os.path.join(install_prefix, 'lib', so_name)
    rendered_data = template.render(rejson_module_path=rejson_module_path, port=REDIS_PORT)

    with open('./config/redis.conf', 'w') as f:
        f.write(rendered_data)
    print("Done")


def copy_config():
    install_prefix = get_install_prefix()

    os.makedirs(os.path.join(install_prefix, 'config'), exist_ok=True)
    shutil.copyfile(os.path.join('config', 'redis.conf'), os.path.join(install_prefix, 'config', 'redis.conf'))
