from setuptools import find_packages, setup

package_name = 'serializer_nodes_demo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/telemetry_launch.yaml']),
    ],
    install_requires=['setuptools', 'rclpy',],
    zip_safe=True,
    maintainer='lenat',
    maintainer_email='lenat@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': ["test_node = serializer_nodes_demo.listener_node_rover:main",
                            'usb_serial_node=serializer_nodes_demo.serial_demo_node_basestation:main', 
                            'pub_serial_node=serializer_nodes_demo.serial_demo_node_publisher:main', 
                            'sub_serial_node=serializer_nodes_demo.serial_demo_node_subscriber:main'
        ],
    },
)
