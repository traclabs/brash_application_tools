import rclpy
from rclpy.node import Node

from sensor_msgs.msg import JointState
from cfs_msgs.msg import ROBOTSIMHKTlm
from cfs_msgs.msg import RobotSimCmd


class JointStateConverter(Node):

    def __init__(self):
        super().__init__('joint_state_convert')
        self.js_publisher = self.create_publisher(JointState, 'joint_states', 10)
        self.jc_publisher = self.create_publisher(RobotSimCmd, '/robot_sim_cmd', 10)
        self.js_subscription = self.create_subscription(
            ROBOTSIMHKTlm,
            'cfe_robot_sim_hk_tlm',
            self.cfs_callback,
            10)

        self.jc_subscription = self.create_subscription(
            JointState,
            'joint_command',
            self.jc_callback,
            10)

        self.js_subscription  # prevent unused variable warning
        self.jc_subscription  # prevent unused variable warning

    def cfs_callback(self, msg):
        self.get_logger().info('got new cFS joint telemetry')
        # self.get_logger().info(msg)
        print(msg)
        js = JointState()
        js.header.stamp = self.get_clock().now().to_msg()
        # js.header.frame_id = "iss"
        js.name.append("joint0")
        js.name.append("joint1")
        js.name.append("joint2")
        js.name.append("joint3")
        js.name.append("joint4")
        js.name.append("joint5")
        js.name.append("joint6")
        js.position.append(msg.joint0)
        js.position.append(msg.joint1)
        js.position.append(msg.joint2)
        js.position.append(msg.joint3)
        js.position.append(msg.joint4)
        js.position.append(msg.joint5)
        js.position.append(msg.joint6)

        print(js)
        # self.get_logger().info(js)
        self.js_publisher.publish(js)

    def jc_callback(self, msg):
        self.get_logger().info('got new cFS joint command')

        cmd = RobotSimCmd()
        cmd.cmd_id = 1
        cmd.robot_sim_set_joints_cc.joint0 = msg.position[0]
        cmd.robot_sim_set_joints_cc.joint1 = msg.position[1]
        cmd.robot_sim_set_joints_cc.joint2 = msg.position[2]
        cmd.robot_sim_set_joints_cc.joint3 = msg.position[3]
        cmd.robot_sim_set_joints_cc.joint4 = msg.position[4]
        cmd.robot_sim_set_joints_cc.joint5 = msg.position[5]
        cmd.robot_sim_set_joints_cc.joint6 = msg.position[6]

        self.jc_publisher.publish(cmd)


def main(args=None):

    rclpy.init(args=args)

    jsc = JointStateConverter()
    rclpy.spin(jsc)

    bridge.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()