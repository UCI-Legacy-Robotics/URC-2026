import rclpy
from rclpy.node import Node

from yellowjacket_can.msg import ControlMessage
from drive_teleop.msg import DriveControlMessage

class DriveNode(Node):
    def __init__(self):
        super().__init__('drive_manager_node')
        self.get_logger().info(f"Started drive manager node")
        # Init yellowjacket control stuff
        self.fl_pub = self.create_publisher(ControlMessage, '/drive_fl/control_message', 10)
        self.fr_pub = self.create_publisher(ControlMessage, '/drive_fr/control_message', 10)
        self.ml_pub = self.create_publisher(ControlMessage, '/drive_ml/control_message', 10)
        self.mr_pub = self.create_publisher(ControlMessage, '/drive_mr/control_message', 10)
        self.bl_pub = self.create_publisher(ControlMessage, '/drive_bl/control_message', 10)
        self.br_pub = self.create_publisher(ControlMessage, '/drive_br/control_message', 10)

        self.fls_pub = self.create_publisher(ControlMessage, '/steer_fl/control_message', 10)
        self.frs_pub = self.create_publisher(ControlMessage, '/steer_fr/control_message', 10)
        
        # For other stuff like base station to control
        self.drive_sub = self.create_subscription(DriveControlMessage, "/drive_teleop_node/command", self.subscriber_callback, 10)
        
    def subscriber_callback(self, msg):
        new_msg = ControlMessage()
        new_msg.control_mode = 5
        new_msg.input_mode = 1 # Duty cycle control, change to 0 for velocity control
        
        new_msg.input_vel = msg.drive_input_pwm
        self.fl_pub.publish(new_msg)
        self.ml_pub.publish(new_msg)
        self.bl_pub.publish(new_msg)
        self.fr_pub.publish(new_msg)
        self.mr_pub.publish(new_msg)
        self.br_pub.publish(new_msg)
        
        new_msg.input_vel = msg.steer_input_pwm    
        self.fls_pub.publish(new_msg)
        self.frs_pub.publish(new_msg)    
        
        
        self.get_logger().info(f"Sent duty cycle of {msg.drive_input_pwm} to drive motors!")
        self.get_logger().info(f"Sent duty cycle of {msg.steer_input_pwm} to steer motors!")



def main(args=None):
    rclpy.init(args=args)
    drive_node = DriveNode()
    rclpy.spin(drive_node)
    drive_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()