from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import LaunchConfigurationEquals
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Define the command-line argument (default is 'mock')
    mode_arg = DeclareLaunchArgument(
        'mode',
        default_value='mock',
        description='Which GNSS data source to use: "mock" or "real"'
    )

    # 2. Get the value of the argument
    mode = LaunchConfiguration('mode')

    # 3. Define the Mock Node (runs only if mode:=mock)
    mock_node = Node(
        package='mock_gps',
        executable='mock_gps_node',
        name='gnss_node',
        condition=LaunchConfigurationEquals('mode', 'mock')
    )

    # 4. Define the Real SparkFun Driver Node (runs only if mode:=real)
    real_node = Node(
        package='nmea_navsat_driver',
        executable='nmea_serial_driver',
        name='gnss_node',
        parameters=[{
            'port': '/dev/ttyACM0',
            'baud': 115200
        }],
        condition=LaunchConfigurationEquals('mode', 'real')
    )

    # 5. Return the launch description
    return LaunchDescription([
        mode_arg,
        mock_node,
        real_node
    ])
