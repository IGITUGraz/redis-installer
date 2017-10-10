from setuptools import setup

from redisinstaller.installer import install_redis

FULL_VERSION = "0.1.0"

"""
This file installs the redis.

"""

setup(
    name="redis-installer",
    version=FULL_VERSION,
    packages=('rediscontroller',),
    author="Anand S",
    author_email="anandtrex@users.noreply.github.com",
    description="This module installs redis to the current virtual environment bin",
    install_requires=['pycurl', 'patool', 'pyunpack', 'redis'],
    provides=['rediscontroller'],
    data_files=[
        ('config', ['redis.conf']),
    ]
)

install_redis()
