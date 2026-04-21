import rclpy
from rclpy.node import Node
from drive_teleop.msg import DriveControlMessage
import serial
import json

class SerialPublisher(Node):
    def __init__(self):
        super().__init__('serial_publisher')
        
        self.declare_parameter('serial_port', '/dev/ttyUSB0')
        self.declare_parameter('topic', '/drive_manager/drive_teleop_node/command')
        self.declare_parameter('baud_rate', 57600)
        self.declare_parameter('update_rate_hz', 50)
        
        port = self.get_parameter('serial_port').get_parameter_value().string_value
        topic = self.get_parameter('topic').get_parameter_value().string_value
        baud = self.get_parameter('baud_rate').get_parameter_value().integer_value
        update_rate = self.get_parameter('update_rate_hz').get_parameter_value().integer_value

        self.ser = serial.Serial(port, baud, timeout=0.1)
        self.pub = self.create_publisher(DriveControlMessage, topic, 10)
        self.create_timer(1/update_rate, self.read_serial) # Run really fast at 200 Hz for continuous updates

    def read_serial(self):
        #ser in waiting is the bytes in the serial buffer 
        if self.ser.in_waiting:
            #read the line from serial (stops when it finds the \n)
            line = self.ser.readline().decode().strip()
            if not line:
                #if empty line, dont do anything
                return
            try:
                #converts string named line into python dict  
                data = json.loads(line)
                #if correct data type, convert data to string
                if data.get('type') == 'drive_cmd':
                    drive_input = data.get('data', 0).split(" ") # drive cmd data in format of "left_pwm right_pwm"
                    msg = DriveControlMessage()
                    msg.left_input_pwm = int(drive_input[0])
                    msg.right_input_pwm = int(drive_input[1])
                    # send mssage to yellowjackets
                    self.pub.publish(msg)
                    #print out message
                    self.get_logger().info(f"Published: {msg}")
            except Exception as e:
                self.get_logger().warn(f"Failed to parse serial: {line} | {e}")

def main(args=None):
    rclpy.init(args=args)
    node = SerialPublisher()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
