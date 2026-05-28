from setuptools import find_packages
from setuptools import setup

setup(
    name='yellowjacket_can',
    version='0.0.1',
    packages=find_packages(
        include=('yellowjacket_can', 'yellowjacket_can.*')),
)
