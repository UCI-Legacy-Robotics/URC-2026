
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('listener_node_rover')
        self.get_logger().info('Started listener')
        self.subscription = self.create_subscription(
            String,              # message type
            'chatter',           # topic name
            self.listener_callback,
            10                   # QoS depth
        )
        # prevent unused variable warning
        self.subscription
        
    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    rclpy.shutdown()


if __name__ == '__main__':
    main()