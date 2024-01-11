import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool
from example_interfaces.msg import Bool as EBool
from sensor_msgs.msg import JointState


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('republisher')
        self.publisher_ = self.create_publisher(Bool, 'right_hand/trigger', 10)
        self.sub_ = self.create_subscription(EBool, 'bp/right_hand/trigger',self.listener_callback, 10)
        # self.sub2_ = self.create_subscription(JointState, 'joint_states_sim_right',self.joint_callback, 10)
        # self.publisher2_ = self.create_publisher(JointState, 'gripper_states_sim', 10)
        self.gripper_joints = [
            "finger_joint",
            "left_inner_knuckle_joint",
            "right_inner_knuckle_joint",
            "right_outer_knuckle_joint",
            "left_inner_finger_joint",
            "right_inner_finger_joint",
        ]
    def listener_callback(self, msg):
        new = Bool()
        new.data = msg.data
        self.publisher_.publish(new) 
    def joint_callback(self, msg):
        idxs = {}
        for idx, name in enumerate(msg.name):
            if name in self.gripper_joints:
                idxs[name]= idx
        pos = []
        for name in self.gripper_joints:
            pos.append(msg.position[idxs[name]])
        new = JointState()
        new.header = msg.header
        new.name = self.gripper_joints
        new.position = pos
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