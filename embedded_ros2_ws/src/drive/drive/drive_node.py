import rclpy
from rclpy.node import Node

from yellowjacket_can.msg import ControlMessage


from std_msgs.msg import Int32

class DriveNode(Node):
    def __init__(self):
        super().__init__('drive_pub')
        self.fl_pub = self.create_publisher(ControlMessage, 'drive_fl/control_message', 10)
        self.fr_pub = self.create_publisher(ControlMessage, 'drive_fr/control_message', 10)
        self.ml_pub = self.create_publisher(ControlMessage, 'drive_ml/control_message', 10)
        self.mr_pub = self.create_publisher(ControlMessage, 'drive_mr/control_message', 10)
        
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.drive_forward)
        
    def drive_forward(self):
        try:
            vel = int(input())
        except Exception as e:
            vel = 0
            self.get_logger().info("IDIOT, NOT AN INTEGER")
            
        msg = ControlMessage()
        msg.control_mode = 5
        msg.input_mode = 1
        msg.input_vel = vel
        
        self.fl_pub.publish(msg)
        self.fr_pub.publish(msg)
        self.ml_pub.publish(msg)
        self.mr_pub.publish(msg)
        self.get_logger().info(f"Sent velocity of {vel} to drive motors!")



def main(args=None):
    rclpy.init(args=args)
    drive_node = DriveNode()
    rclpy.spin(drive_node)
    drive_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
