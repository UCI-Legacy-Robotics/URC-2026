from setuptools import find_packages
from setuptools import setup

setup(
    name='cubemars_can',
    version='0.0.1',
    packages=find_packages(
        include=('cubemars_can', 'cubemars_can.*')),
)
