from setuptools import setup

from redisinstaller.installer import install_redis, install_redis_json, generate_config

FULL_VERSION = "0.2.0"

"""
This file installs the redis.

"""

## NOTE: The order of these calls is fairly important. Do not move.

generate_config()

setup(
    name="redis-installer",
    version=FULL_VERSION,
    packages=('rediscontroller',),
    author="Anand S",
    author_email="anandtrex@users.noreply.github.com",
    description="This module installs redis to the current virtual environment bin",
    install_requires=['pycurl', 'patool', 'pyunpack', 'gitpython', 'redis', 'rejson'],
    provides=['rediscontroller'],
    data_files=[
        ('config', ['config/redis.conf']),
    ]
)

install_redis()
install_redis_json()
