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
        
        port = self.get_parameter('serial_port').get_parameter_value().string_value
        topic = self.get_parameter('topic').get_parameter_value().string_value
        baud = self.get_parameter('baud_rate').get_parameter_value().integer_value

        self.ser = serial.Serial(port, baud, timeout=0.1)
        self.create_subscription(DriveControlMessage, topic, self.send_serial, 10)

    def send_serial(self, msg: DriveControlMessage):
        # Print out difference in timestamps and pass on current time
        input_timestamp = msg.header.stamp
        current_time = self.get_clock().now()
        diff = current_time - input_timestamp
        self.get_logger.info(f"Time delay (s) from drive_teleop_node to base radio: {diff}")
        
        message = f"{msg.left_input_pwm} {msg.right_input_pwm} {current_time}"
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