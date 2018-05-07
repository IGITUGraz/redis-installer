import os
import random
import subprocess

from rediscontroller.utils import get_install_prefix, which

REDIS_PORT = 65535


def start_redis(data_directory, config_file_path=None, redis_port=REDIS_PORT):
    """
    Start the redis server with the following options:
    :param data_directory: The directory where redis should construct its data files
    :param config_file_path: The redis config for redis to use
        It is highly recommended to use the redis.conf installed with this package which sets up redis properly.
        Otherwise, make sure the config you pass in has at least rejson enabled. You should also use the port you set
        in your clients to connect redis clients.
    :param redis_port: None or int or the string 'random'. If None, redis is started on port 65535. If 'random', redis is
        started on a random port between 60000 to 65535
    :return: The port number on which the client was started
    """
    os.makedirs(data_directory, exist_ok=True)
    current_dir = os.getcwd()
    os.chdir(data_directory)

    redis_server_path = which('redis-server')
    assert redis_server_path is not None, "redis-server not found in PATH. Is redis installed?"

    if config_file_path is None:
        install_prefix = get_install_prefix()
        config_file_path = os.path.join(install_prefix, 'config', 'redis.conf')

    assert os.path.exists(config_file_path), "File {} does not exist".format(config_file_path)

    if redis_port == 'random':
        redis_port = random.randint(60000, 65535)
    else:
        assert isinstance(redis_port, int), "The redis port should be one of None, the string 'random' or an integer"

    result = subprocess.run([redis_server_path, config_file_path, '--port', str(redis_port)])
    assert result.returncode == 0
    os.chdir(current_dir)

    while True:
        if is_redis_running(redis_port=redis_port):
            break

    return redis_port


def stop_redis(redis_host='localhost', redis_port=REDIS_PORT):
    """
    Stop the redis server. It sends a SHUTDOWN signal to the redis server specified
    :param redis_host:
    :param redis_port:
    :return:
    """
    import redis
    r = redis.StrictRedis(host=redis_host, port=redis_port)
    r.shutdown()


def is_redis_running(redis_host='localhost', redis_port=REDIS_PORT):
    """
    Check if redis is running at the provided host and port
    :param redis_host:
    :param redis_port:
    :return:
    """
    import redis
    r = redis.StrictRedis(host=redis_host, port=redis_port)
    try:
        r.ping()
        return True
    except redis.exceptions.ConnectionError:
        return False


def get_running_redis_dir(redis_host='localhost', redis_port=REDIS_PORT):
    """
    Get the directory where the redis server at the given host and port is active

    :param redis_host:
    :param redis_port:
    :return: directory
    """
    import redis
    r = redis.StrictRedis(host=redis_host, port=redis_port)
    try:
        directory = r.config_get('dir')['dir']
        return directory
    except redis.exceptions.ConnectionError:
        return None
