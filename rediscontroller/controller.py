import subprocess

import os


def start_redis(data_directory):
    os.makedirs(data_directory, exist_ok=True)
    os.chdir(data_directory)
    install_prefix = os.environ['VIRTUAL_ENV']
    redis_server_path = os.path.join(install_prefix, 'bin', 'redis-server')
    redis_conf_path = os.path.join(install_prefix, 'config', 'redis.conf')

    result = subprocess.run([redis_server_path, redis_conf_path])
    assert result.returncode == 0


def stop_redis(redis_host='localhost', redis_port=6379):
    import redis
    r = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
    r.shutdown()
