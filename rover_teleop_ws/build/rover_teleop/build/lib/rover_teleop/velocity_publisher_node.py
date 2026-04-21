import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class Velocity_Publisher(Node):
    def __init__(self):
        #names the node velocity publisher node
        super().__init__('velocity_publisher_node')
        #makes a node that publishes to drive_control topic w/ queue of 15 messages
        self.publisher_ = self.create_publisher(Int32, 'drive_control', 15)
        #makes a timer that calls a function every second
        self.timer = self.create_timer(0.5, self.publish_vel)
        
    def publish_vel(self):
        #publishes int data
        try:
            vel=int(input())
        except:
            vel=0
        msg=Int32()
        msg.data= vel
        self.publisher_.publish(msg)
        self.get_logger().info(f'Velocity: {msg.data}')
        
def main(args= None):
    rclpy.init(args=args)
    node=Velocity_Publisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
        
if __name__=='__main__':
    main()