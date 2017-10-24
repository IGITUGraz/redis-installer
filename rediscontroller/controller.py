import subprocess

import os

# REDIS_PORT = 6379
REDIS_PORT = 65535


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

    while True:
        if is_redis_running():
            break


def stop_redis(redis_host='localhost', redis_port=REDIS_PORT):
    import redis
    r = redis.StrictRedis(host=redis_host, port=redis_port)
    r.shutdown()


def is_redis_running(redis_host='localhost', redis_port=REDIS_PORT):
    import redis
    r = redis.StrictRedis(host=redis_host, port=redis_port)
    try:
        r.ping()
        return True
    except redis.exceptions.ConnectionError:
        return False
