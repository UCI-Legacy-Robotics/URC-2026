import rclpy
from rclpy.node import Node

from yellowjacket_can.msg import ControlMessage
from drive_teleop.msg import DriveControlMessage

class DriveNode(Node):
    def __init__(self):
        super().__init__('drive_manager_node')
        self.get_logger().info(f"Started drive manager node")
        # Init yellowjacket control stuff
        self.fl_pub = self.create_publisher(ControlMessage, 'drive_fl/control_message', 10)
        self.fr_pub = self.create_publisher(ControlMessage, 'drive_fr/control_message', 10)
        self.ml_pub = self.create_publisher(ControlMessage, 'drive_ml/control_message', 10)
        self.mr_pub = self.create_publisher(ControlMessage, 'drive_mr/control_message', 10)
        self.bl_pub = self.create_publisher(ControlMessage, 'drive_bl/control_message', 10)
        self.br_pub = self.create_publisher(ControlMessage, 'drive_br/control_message', 10)
        
        # For other stuff like base station to control
        self.drive_sub = self.create_subscription(DriveControlMessage, "drive_teleop_node/command", self.subscriber_callback, 10)
        
    def subscriber_callback(self, msg):
        new_msg = ControlMessage()
        new_msg.control_mode = 5
        new_msg.input_mode = 1 # Duty cycle control, change to 0 for velocity control
        
        new_msg.input_vel = msg.left_input_pwm
        self.fl_pub.publish(new_msg)
        self.ml_pub.publish(new_msg)
        self.bl_pub.publish(new_msg)
        
        new_msg.input_vel = msg.right_input_pwm        
        self.fr_pub.publish(new_msg)
        self.mr_pub.publish(new_msg)
        self.br_pub.publish(new_msg)
        
        self.get_logger().info(f"Sent duty cycle of {msg.left_input_pwm} to left drive motors!")
        self.get_logger().info(f"Sent duty cycle of {msg.right_input_pwm} to right drive motors!")



def main(args=None):
    rclpy.init(args=args)
    drive_node = DriveNode()
    rclpy.spin(drive_node)
    drive_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()