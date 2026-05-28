from setuptools import find_packages
from setuptools import setup

setup(
    name='servo',
    version='0.0.0',
    packages=find_packages(
        include=('servo', 'servo.*')),
)
