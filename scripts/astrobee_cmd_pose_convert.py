#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from ff_msgs.msg import CommandStamped
from ff_msgs.msg import CommandArg
from geometry_msgs.msg import PoseStamped

from cfe_msgs.msg import AstrobeeAppRobotCommandt 
from cfe_msgs.msg import AstrobeeAppRobotStatet


class AstrobeeCmdPoseConverter(Node):
    """
    This class receives the Odometry information from topic /groundsystem/rover_app_hk_tlm
    (cfe_msgs) and publishes them to /odom
    This class also subscribes to "/cmd_vel", and publishes the said command
    to /groundsystem/rover_app_cmd (cfe_msgs)
    """
    def __init__(self):
        super().__init__('twist_convert')

        self.declare_parameter('cmd_out_cfs',  "astrobee_app_robot_command")
        self.cmd_out_cfs = self.get_parameter('cmd_out_cfs').value

        self.declare_parameter('pose_in_cfs',  "astrobee_app_robot_state")
        self.pose_in_cfs = self.get_parameter('pose_in_cfs').value


        self.declare_parameter('pose_in',  "/bumble/loc/pose")
        self.pose_in = self.get_parameter('pose_in').value

        self.declare_parameter('cmd_out',  "/bumble/command")
        self.cmd_out = self.get_parameter('cmd_out').value

        # Subscribe to command from cfs
        self.cmd_subscription = self.create_subscription(
            AstrobeeAppRobotCommandt,
            '/flightsystem/' + self.cmd_out_cfs,
            self.cfs_callback,
            10)
        self.cmd_publisher = self.create_publisher(CommandStamped, self.cmd_out, 10)

        # Subscribe to odom from robot
        self.pose_subscription = self.create_subscription(
            PoseStamped,
            self.pose_in,
            self.pose_callback,
            10)
        # And publish it to a topic that cFS reads    
        self.state_publisher = self.create_publisher(AstrobeeAppRobotStatet, '/flightsystem/' + self.pose_in_cfs, 10)


        self.pose_subscription  # prevent unused variable warning
        self.cmd_subscription  # prevent unused variable warning

    # message of type cfe_msgs/msg/AstrobeeAppRobotCommandt
    def cfs_callback(self, msg):
        self.get_logger().info(f'Received new cFS astrobee cmd message!', throttle_duration_sec=1.0)
        self.get_logger().info(f'Received new cFS astrobee cmd message to send to robot {msg.command.cmd_name} with id: {msg.command.cmd_id}', throttle_duration_sec=1.0)
        self.get_logger().info(f'If move, pose: {msg.command.x}, {msg.command.y}, {msg.command.z}, and orientation: {msg.command.qx}, {msg.command.qy}, {msg.command.qz}, {msg.command.qw} ') 
        
        cmd = CommandStamped()
        cmd.subsys_name = "Astrobee"
        cmd.cmd_name = msg.command.cmd_name
        cmd.cmd_id = msg.command.cmd_id

        arg_0 = CommandArg()
        arg_0.data_type = 5 # String
        arg_0.s = msg.command.frame

        arg_1 = CommandArg()
        arg_1.data_type = 6 # Vec3d
        arg_1.vec3d = [msg.command.x, msg.command.y, msg.command.z]

        # Tolerance
        arg_2 = CommandArg()
        arg_2.data_type = 6 # Vec3d
        arg_2.vec3d = [0.0, 0.0, 0.0]

        # Orientation
        arg_3 = CommandArg()
        arg_3.data_type = 7 # Mat3d
        arg_3.mat33f = [msg.command.qx, msg.command.qy, msg.command.qz, msg.command.qw, 0.0, 0.0, 0.0, 0.0, 0.0]


        cmd.args.append(arg_0)
        cmd.args.append(arg_1)
        cmd.args.append(arg_2)
        cmd.args.append(arg_3)
                                        
        self.cmd_publisher.publish(cmd)

    def pose_callback(self, msg):
        #self.get_logger().info('Received new pose msg from robot to send to cFS', throttle_duration_sec=5.0)
        # self.get_logger().info(str(msg))

        st = AstrobeeAppRobotStatet()
        st.cmd_header.sec.function_code = 1 # CC code. 1 = Command. 0 = Noop
        st.state.frame = msg.header.frame_id
        st.state.x = msg.pose.position.x
        st.state.y = msg.pose.position.y
        st.state.z = msg.pose.position.z
        st.state.qx = msg.pose.orientation.x
        st.state.qy = msg.pose.orientation.y
        st.state.qz = msg.pose.orientation.z
        st.state.qw = msg.pose.orientation.w                
                
        self.state_publisher.publish(st)


def main(args=None):

    rclpy.init(args=args)

    toc = AstrobeeCmdPoseConverter()
    rclpy.spin(toc)

    toc.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
