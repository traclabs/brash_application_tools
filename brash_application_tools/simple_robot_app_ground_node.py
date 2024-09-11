import rclpy
from rclpy.node import Node
from rclpy.time import Duration

from cfe_msgs.msg import SimpleRobotAppCmdt, SimpleRobotAppTlmt, SimpleRobotAppJointConfigt

class SendCommand(Node):
    """
    Send motion command
    """
    def __init__(self):
        super().__init__('send_command')
        self._publish_cmd = self.create_publisher(SimpleRobotAppCmdt, "/groundsystem/simple_robot_app_cmd", 10)
        self._subscribe_tlm = self.create_subscription(SimpleRobotAppTlmt, "/groundsystem/simple_robot_app_tlm", self.tlm_cb, 10)
        
    def send_cmd(self, shoulder_pan, shoulder_lift, elbow, wrist_1, wrist_2, wrist_3):
        self.get_logger().info("Send command!: " + str(round(shoulder_pan, 3)) + ", " + str(round(shoulder_lift, 3)) + ", " + str(round(elbow, 3)) + ", " + str(round(wrist_1, 3)) + ", " + str(round(wrist_2, 3)) + ", " + str(round(wrist_3, 3)) )
        cmd = SimpleRobotAppCmdt()
        cmd.cmd_header.sec.function_code = 1 # CC code. 1 = Command. 0 = Noop

        cmd.joint_goal.shoulder_pan_joint = shoulder_pan 
        cmd.joint_goal.shoulder_lift_joint = shoulder_lift 
        cmd.joint_goal.elbow_joint = elbow 
        cmd.joint_goal.wrist_1_joint = wrist_1 
        cmd.joint_goal.wrist_2_joint = wrist_2 
        cmd.joint_goal.wrist_3_joint = wrist_3                 
                    
        self._publish_cmd.publish(cmd)
                    
    def tlm_cb(self, msg):
        jc =  msg.joint_state
        self.get_logger().info("Getting telemetry: (" + str(round(jc.shoulder_pan_joint, 3)) + ", " + str(round(jc.shoulder_lift_joint, 3))   + ", " + str(round(jc.elbow_joint, 3))  + ", " + str(round(jc.wrist_1_joint, 3))  + ", " + str(round(jc.wrist_2_joint, 3))  + ", " + str(round(jc.wrist_3_joint, 3)) + ")" )

        
#########################
def main(args=None):

    rclpy.init(args=args) 
    test_node = SendCommand()
    
    # Send command
    shoulder_pan = -0.6
    shoulder_lift = 1.5
    elbow = 0.2
    wrist_1 = 0.4
    wrist_2 = 0.3
    wrist_3 = 0.1

    test_node.send_cmd(shoulder_pan, shoulder_lift, elbow, wrist_1, wrist_2, wrist_3)
    
    # Spin and receive telemetry data 
    rclpy.spin(test_node)
    
if __name__ == '__main__':
    main()
