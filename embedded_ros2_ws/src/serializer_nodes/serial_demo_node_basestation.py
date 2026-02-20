import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist   # <-- If your rover uses a different command message, change this
from std_msgs.msg import String       # <-- Replace with a custom telemetry message if needed
import serial, json


# Message format must include a type or header so both ends know whether it’s a command or telemetry.
# Serial baud should match both FTDI radios.
# Use non-blocking reads (timeout=0.1) to keep ROS 2 spinning smoothly.
# Start one node per USB radio on each machine.

class SerialBridge(Node):
    def __init__(self):
        super().__init__('serial_bridge')
        self.declare_parameter('serial_port', '/dev/ttyUSB0')
        self.declare_parameter('cmd_topic', 'chatter')
        self.declare_parameter('telemetry_topic', 'chatter')
        self.declare_parameter('baud_rate', 57600)
        
        serial_port = self.get_parameter('serial_port').get_parameter_value().string_value
        cmd_topic = self.get_parameter('cmd_topic').get_parameter_value().string_value
        baud_rate = self.get_parameter('baud_rate').get_parameter_value().integer_value
        telemetry_topic = self.get_parameter('telemetry_topic').get_parameter_value().string_value
        self.ser = serial.Serial(serial_port, baud_rate, timeout=0.1)
        # -------------------------
        # Subscribers (incoming messages from ROS -> serial)
        # -------------------------
        self.cmd_sub = self.create_subscription(String, cmd_topic, self.send_command, 10)
        self.telemetry_sub = self.create_subscription(String, telemetry_topic, self.send_telemetry, 10)

        # -------------------------
        # Publishers (incoming serial -> ROS)
        # -------------------------
        self.cmd_pub = self.create_publisher(String, cmd_topic, 10)
        self.telemetry_pub = self.create_publisher(String, telemetry_topic, 10)

        # Timer to read serial
        self.create_timer(0.05, self.read_serial)  # <-- Adjust frequency if needed for faster/slower updates

    # -------------------------
    # Send commands over serial
    # -------------------------
    def send_command(self, msg):
        # msg is now a String message
        line = json.dumps({
            'type': 'demo',  # or 'cmd' if you want
            'data': msg.data
        }) + '\n'
        self.ser.write(line.encode())

    # -------------------------
    # Send telemetry over serial
    # -------------------------
    def send_telemetry(self, msg):
        # Customize this if your rover telemetry has a different format
        line = json.dumps({
            'type': 'telemetry',
            'data': msg.data
        }) + '\n'
        self.ser.write(line.encode())

    # -------------------------
    # Read incoming serial messages
    # -------------------------
    def read_serial(self):
        while self.ser.in_waiting:
            line = self.ser.readline().decode().strip()  # read one line
            if not line:
                continue
            try:
                data = json.loads(line)  # parse JSON
                if data.get('type') == 'demo':  # check the type
                    msg = String()
                    msg.data = data.get('data', '')  # get the string
                    self.cmd_pub.publish(msg)  # publish to ROS topic
                    self.get_logger().info(f"Received: {msg.data}")
            except Exception as e:
                self.get_logger().warn(f"Failed to parse: {line} | {e}")

def main(args=None):
    rclpy.init(args=args)
    node = SerialBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
