from setuptools import setup
from setuptools.command.install import install
from redisinstaller.installer import install_redis, install_redis_json, generate_config, copy_config

FULL_VERSION = "0.2.0"

"""
This file installs the redis.

"""


## NOTE: The order of these calls is fairly important. Do not move.

class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install_redis()
        install_redis_json()
        generate_config()
        copy_config()

        install.run(self)


setup(
    name="redis-installer",
    version=FULL_VERSION,
    packages=('rediscontroller',),
    author="Anand S",
    author_email="anandtrex@users.noreply.github.com",
    description="This module installs redis to the current virtual environment bin",
    install_requires=['jinja2', 'pycurl', 'patool', 'pyunpack', 'gitpython', 'redis', 'rejson'],
    provides=['rediscontroller'],
    cmdclass={
        'install': PostInstallCommand,
    },
)
