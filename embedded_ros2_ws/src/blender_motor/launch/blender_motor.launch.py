from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
   return LaunchDescription([
       Node(
           package='blender_motor',
           executable='blender_motor_node',
           name='blender_motor_node',
           output='screen',
           parameters=[
               {'gpio_pin': 12},
               {'duty_cycle': 0.5},
               {'enable_on_start': False},
           ],
       ),
   ])
