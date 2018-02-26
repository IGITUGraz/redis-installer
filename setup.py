import re

from setuptools import setup
from setuptools.command.install import install

FULL_VERSION = "1.0.2"

"""
This file installs the redis.
"""


def get_requirements(filename):
    """
    Helper function to read the list of requirements from a file
    """
    dependency_links = []
    with open(filename) as requirements_file:
        requirements = requirements_file.read().strip('\n').splitlines()
    for i, req in enumerate(requirements):
        if ':' in req:
            match_obj = re.match(r"git\+(?:https|ssh|http):.*#egg=(\w+)-(.*)", req)
            assert match_obj, "Cannot make sence of url {}".format(req)
            requirements[i] = "{req}=={ver}".format(req=match_obj.group(1), ver=match_obj.group(2))
            dependency_links.append(req)
    return requirements, dependency_links


def _post_install():
    from redisinstaller.installer import install_redis, install_redis_json, generate_config, copy_config

    install_redis()
    install_redis_json()
    generate_config()
    copy_config()


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)
        _post_install()


requirements, dependency_links = get_requirements('requirements.txt')

setup(
    name="redis-installer",
    version=FULL_VERSION,
    packages=('rediscontroller',),
    author="Anand S",
    author_email="anandtrex@users.noreply.github.com",
    description="This module installs redis to the current virtual environment bin",
    install_requires=requirements,
    dependency_links=dependency_links,
    provides=['rediscontroller'],
    cmdclass={
        'install': PostInstallCommand,
    },

)
