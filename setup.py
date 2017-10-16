from setuptools import setup


FULL_VERSION = "0.2.0"

"""
This file installs the redis.

"""

## NOTE: The order of these calls is fairly important. Do not move.


setup(
    name="redis-installer",
    version=FULL_VERSION,
    packages=('rediscontroller',),
    author="Anand S",
    author_email="anandtrex@users.noreply.github.com",
    description="This module installs redis to the current virtual environment bin",
    install_requires=['jinja2', 'pycurl', 'patool', 'pyunpack', 'gitpython', 'redis', 'rejson'],
    provides=['rediscontroller'],
    # data_files=[
    #     ('config', ['config/redis.conf']),
    # ]
)

from redisinstaller.installer import install_redis, install_redis_json, generate_config, copy_config

install_redis()
install_redis_json()
generate_config()
copy_config()
