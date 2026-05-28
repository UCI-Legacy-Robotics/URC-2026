from setuptools import find_packages
from setuptools import setup

setup(
    name='stepper_can',
    version='0.0.1',
    packages=find_packages(
        include=('stepper_can', 'stepper_can.*')),
)
