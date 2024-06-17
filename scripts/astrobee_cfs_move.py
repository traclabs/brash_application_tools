#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from cfe_msgs.msg import AstrobeeAppCmdt

class CfsPublisher(Node):

    def __init__(self):
        super().__init__('cfs_publisher')
        self.publisher_ = self.create_publisher(AstrobeeAppCmdt, '/groundsystem/astrobee_app_cmd', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = AstrobeeAppCmdt()
        msg.cmd_name = "simpleMove6DOF"
        msg.cmd_id = "simpleMove6DOF"
        msg.frame = "world"
        msg.x = 10.743
        msg.y = -4.581
        msg.z = 4.300
        msg.qx = 0.0 
        msg.qy = 0.0
        msg.qz = 1.0
        msg.qw = 0.0
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing move message')
        self.timer.cancel()
        


def main(args=None):
    rclpy.init(args=args)

    cfs_publisher = CfsPublisher()

    rclpy.spin(cfs_publisher)

    cfs_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
