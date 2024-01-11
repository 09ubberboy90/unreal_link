import rclpy
from rclpy.node import Node
import os
from geometry_msgs.msg import Pose


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('pose_saver')
        self.sub_ = self.create_subscription(Pose, 'bp/right_hand/pose',self.listener_callback, 10)
        self.declare_parameter('uuid', "111111")
        self.participant_id = self.get_parameter('uuid').get_parameter_value().string_value
        try:
            os.mkdir(f"/home/ubb/Documents/Baxter_isaac/ROS2/src/experiment_recorder/data/ur/{self.participant_id}")
        except Exception as e:
            print(e)
        try:
            os.remove(f"/home/ubb/Documents/Baxter_isaac/ROS2/src/experiment_recorder/data/ur/{self.participant_id}/right_hand_pose.csv")
        except Exception as e:
            print(e)
        # self.sub2_ = self.create_subscription(JointState, 'joint_states_sim_right',self.joint_callback, 10)
        # self.publisher2_ = self.create_publisher(JointState, 'gripper_states_sim', 10)

    def listener_callback(self, msg:Pose):
        with open(f"/home/ubb/Documents/Baxter_isaac/ROS2/src/experiment_recorder/data/ur/{self.participant_id}/right_hand_pose.csv", "a") as f:
            sec, nsec = self.get_clock().now().seconds_nanoseconds()
            ros_start_time = f"{sec}.{nsec:09d}"
            f.write(f"{ros_start_time},{msg.position.x},{msg.position.y},{msg.position.z},{msg.orientation.x},{msg.orientation.y},{msg.orientation.z},{msg.orientation.w}\n")



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