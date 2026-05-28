from setuptools import find_packages
from setuptools import setup

setup(
    name='drive_teleop',
    version='0.0.0',
    packages=find_packages(
        include=('drive_teleop', 'drive_teleop.*')),
)
