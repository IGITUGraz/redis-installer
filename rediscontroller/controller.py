import os
import random
import subprocess
from numbers import Integral

from rediscontroller.utils import get_install_prefix, which, changed_dir
from rediscontroller.utils import reserve_port

REDIS_PORT = 65535


def _careful_start_redis(redis_server_path, data_directory, config_file_path, redis_port):
    """
    Tries to start redis at the specified directory, port, with the specified
    config file. Returns None if there was a port conflict and raises a
    RuntimeError if the redis server wasn't successfully started.

    If successful, returns True
    """
    reserved_port = reserve_port(redis_port)
    if reserved_port is not None:
        with changed_dir(data_directory):
            creation_proc_result = subprocess.run([redis_server_path, config_file_path,
                                                   '--port', str(redis_port)])

        if creation_proc_result.returncode != 0:
            raise RuntimeError(
                "The redis server could not be launched:\n"
                " in directory: {} \n"
                " on port number: {}\n"
                " with config file: {}\n"
                "\n"
                "The following is the output of the launch command:\n{}"
                ""
                .format(data_directory, redis_port, config_file_path, creation_proc_result.stdout))

        while True:
            if is_redis_running(redis_port=redis_port):
                break

        return True
    else:
        return None


def start_redis(data_directory, config_file_path=None, redis_port=REDIS_PORT):
    """
    Start the redis server with the following options:
    :param data_directory: The directory where redis should construct its data
        files. Note that only one instance of a redis server must be active on a
        particular directory. This is the responsibility of the script calling this
        function. If multiple instances are run, the database risks getting
        corrupted.
    :param config_file_path: The redis config for redis to use It is highly recommended
        to use the redis.conf installed with this package which sets up redis properly.
        Otherwise, make sure the config you pass in has at least rejson enabled. You
        should also use the port you set in your clients to connect redis clients.
    :param redis_port: int or the string 'random'. The default port that redis is
        started on is port 65535. If 'random', redis is started on a random port
        between 60000 to 65535.
    :return: The port number on which the client was started
    """
    # I've noticed that if a port collision occurs it isn't really detected by
    # redis if you use daemonize on. it just fails completely silently, i.e.
    # returns 0 and doesn't construct the server. Moreover, if there is an already
    # existing server then that is the one that is assumed constructed. This is
    # particularly a disaster for randomized ports.
    #
    # The only way to be sure the port is free is to try binding a socket to it.
    # Only if a port is free will the redis instance be started on it. This is done
    # using a helper function reserve_port in utils.py
    os.makedirs(data_directory, exist_ok=True)

    redis_server_path = which('redis-server')
    assert redis_server_path is not None, "redis-server not found in PATH. Is redis installed?"

    if config_file_path is None:
        install_prefix = get_install_prefix()
        config_file_path = os.path.join(install_prefix, 'config', 'redis.conf')

    assert os.path.exists(config_file_path), "File {} does not exist".format(config_file_path)

    if redis_port == 'random':
        n_random_trials = 4
        for i in range(n_random_trials):  # makes n_random_trials tries to start a redis server at a random port
            redis_port = random.randint(60000, 65535)
            result = _careful_start_redis(redis_server_path, data_directory, config_file_path, redis_port)
            if result:
                break
        else:
            raise RuntimeError("Tried {} Random ports between 60000-65535, could not find a free port"
                               .format(n_random_trials))
    else:
        assert isinstance(redis_port, Integral), "The redis port should be one of the string 'random' or an integer"
        result = _careful_start_redis(redis_server_path, data_directory, config_file_path, redis_port)
        if not result:
            raise RuntimeError("It appears there is a port conflict on the specified port {}".format(redis_port))

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
