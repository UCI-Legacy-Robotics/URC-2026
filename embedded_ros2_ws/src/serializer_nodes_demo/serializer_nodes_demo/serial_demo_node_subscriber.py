# serial_subscriber_node.py
import rclpy
from rclpy.node import Node
from drive_teleop.msg import DriveControlMessage
import serial
import json

class SerialSubscriber(Node):
    def __init__(self):
        super().__init__('serial_subscriber')
        self.declare_parameter('serial_port', '/dev/ttyUSB0')
        self.declare_parameter('topic', '/drive_teleop_node/command')
        self.declare_parameter('baud_rate', 57600)
        self.declare_parameter('update_rate_hz', 50)
        
        port = self.get_parameter('serial_port').get_parameter_value().string_value
        topic = self.get_parameter('topic').get_parameter_value().string_value
        baud = self.get_parameter('baud_rate').get_parameter_value().integer_value
        update_rate = self.get_parameter('update_rate_hz').get_parameter_value().integer_value

        self.ser = serial.Serial(port, baud, timeout=0.1)
        self.latest_msg = None
        
        self.create_subscription(DriveControlMessage, topic, self.sub_callback, 10)
        self.create_timer(1/update_rate, self.send_callback) # Send messages over radio at 50 Hz
        
    def sub_callback(self, msg: DriveControlMessage):
        self.latest_msg = msg
        
    def send_callback(self):
        if self.latest_msg is not None:
            message = f"{self.latest_msg.left_input_pwm} {self.latest_msg.right_input_pwm}"
            line = json.dumps({'type': 'drive_cmd', 'data': message}) + '\n'
            self.ser.write(line.encode())
            self.get_logger().info(f"Sent: {message}")

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
