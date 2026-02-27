# serial_subscriber_node.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import serial
import json

class SerialSubscriber(Node):
    def __init__(self):
        super().__init__('serial_subscriber')
        self.declare_parameter('serial_port', '/dev/ttyUSB0')
        self.declare_parameter('topic', 'drive_control')
        self.declare_parameter('baud_rate', 57600)
        
        port = self.get_parameter('serial_port').get_parameter_value().string_value
        topic = self.get_parameter('topic').get_parameter_value().string_value
        baud = self.get_parameter('baud_rate').get_parameter_value().integer_value

        self.ser = serial.Serial(port, baud, timeout=0.1)
        self.create_subscription(Int32, topic, self.send_serial, 10)

    def send_serial(self, msg: Int32):
        line = json.dumps({'type': 'cmd', 'data': msg.data}) + '\n'
        self.ser.write(line.encode())
        self.get_logger().info(f"Sent: {msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = SerialSubscriber()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()