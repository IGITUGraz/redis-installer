import subprocess

import os


def start_redis(data_directory, config_file_path=None):
    os.makedirs(data_directory, exist_ok=True)
    current_dir = os.getcwd()
    os.chdir(data_directory)
    install_prefix = os.environ['VIRTUAL_ENV']
    assert install_prefix is not None, "Running from outside a virtual environment not supported"

    redis_server_path = os.path.join(install_prefix, 'bin', 'redis-server')
    if config_file_path is None:
        config_file_path = os.path.join(install_prefix, 'config', 'redis.conf')

    assert os.path.exists(config_file_path), "File {} does not exist".format(config_file_path)

    result = subprocess.run([redis_server_path, config_file_path])
    assert result.returncode == 0
    os.chdir(current_dir)


def stop_redis(redis_host='localhost', redis_port=6379):
    import redis
    r = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
    r.shutdown()
