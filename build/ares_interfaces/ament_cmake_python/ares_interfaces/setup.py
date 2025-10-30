from setuptools import find_packages
from setuptools import setup

setup(
    name='ares_interfaces',
    version='0.0.1',
    packages=find_packages(
        include=('ares_interfaces', 'ares_interfaces.*')),
)
