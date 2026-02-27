from setuptools import find_packages, setup

package_name = 'blender_motor'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/blender_motor.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='fernando',
    maintainer_email='navarretef7905@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'blender_motor_node = blender_motor.blender_motor_node:main',
        ],
    },
)
