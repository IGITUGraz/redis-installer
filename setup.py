from setuptools import setup
from setuptools import find_packages

from redisinstall.installer import install_redis

FULL_VERSION = "0.1.0"

"""
This file installs the redis.
Note that it does not perform any installation of the documentation. For this, follow the specified procedure in the
 README. For updating the version, update MAJOR_VERSION and FULL_VERSION in ltl/version.py
"""

setup(
    name="Redis Installer",
    version=FULL_VERSION,
    packages=find_packages(exclude='redisinstall'),
    author="Anand Subramoney",
    author_email="anand@igi.tugraz.at",
    description="This module installs redis to the current virtual environment bin",
    install_requires=['pycurl', 'patool', 'pyunpack', 'redis'],
    provides=['redisrun'],
    # dependency_links=dependency_links,
    data_files=[
        ('config', ['redis.conf']),
    ]
)

install_redis()
