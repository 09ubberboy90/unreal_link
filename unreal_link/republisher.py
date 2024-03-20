import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool
from example_interfaces.msg import Bool as EBool
from sensor_msgs.msg import JointState


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('republisher')
        self.publisher_ = self.create_publisher(Bool, 'right_hand/trigger', 10)
        self.sub_ = self.create_subscription(EBool, 'bp/baxter/right_hand/trigger',self.listener_callback, 10)
        self.publisher2_ = self.create_publisher(Bool, 'left_hand/trigger', 10)
        self.sub2_ = self.create_subscription(EBool, 'bp/baxter/left_hand/trigger',self.listener_callback2, 10)
        print("Republisher started")

    def listener_callback(self, msg):
        new = Bool()
        new.data = msg.data
        self.publisher_.publish(new) 

    def listener_callback2(self, msg):
        new = Bool()
        new.data = msg.data
        self.publisher2_.publish(new) 
        
def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()