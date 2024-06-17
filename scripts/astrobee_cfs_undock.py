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
        msg.cmd_name = "undock"
        msg.cmd_id = "undock"
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing undock message')
        self.timer.cancel()
        


def main(args=None):
    rclpy.init(args=args)

    cfs_publisher = CfsPublisher()

    rclpy.spin(cfs_publisher)

    cfs_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
