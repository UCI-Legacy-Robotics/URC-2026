#!/usr/bin/env python3

import rclpy
from rclpy.node import Node


class BlenderMotorNode(Node):
    def __init__(self):
        super().__init__('blender_motor_node')
        self.get_logger().info('Blender motor node has started.')


def main(args=None):
    rclpy.init(args=args)
    node = BlenderMotorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()