from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='pano_stitch_ros2',
            executable='pano_stitch_node',
            name='pano_stitch_node',
            output='screen',
            parameters=[{
                'image_topic': '/zed2/zed_node/left/image_rect_color',
                'max_buffer_size': 8,
            }],
        )
    ])
