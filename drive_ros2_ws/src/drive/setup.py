from setuptools import find_packages, setup

package_name = 'drive_manager'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/teleop_drive_launch.yaml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dhrish',
    maintainer_email='dhrishreddyk@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'drive_manager_node = src.drive_manager_node:main'
        ],
    },
)
