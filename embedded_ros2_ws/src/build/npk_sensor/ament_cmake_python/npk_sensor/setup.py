from setuptools import find_packages
from setuptools import setup

setup(
    name='npk_sensor',
    version='0.0.0',
    packages=find_packages(
        include=('npk_sensor', 'npk_sensor.*')),
)
