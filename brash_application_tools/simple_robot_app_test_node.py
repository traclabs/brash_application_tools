import rclpy
from rclpy.node import Node
from rclpy.time import Duration

from cfe_msgs.msg import SimpleRobotAppCmdt, SimpleRobotAppTlmt

class SendCommand(Node):
    """
    Send motion command
    """
    def __init__(self):
        super().__init__('send_command')
        self._publish_cmd = self.create_publisher(SimpleRobotAppCmdt, "/groundsystem/simple_robot_app_cmd", 10)
        self._subscribe_tlm = self.create_subscription(SimpleRobotAppTlmt, "/groundsystem/simple_robot_app_tlm", self.tlm_cb, 10)
        

    def tlm_cb(self, msg):
        self.get_logger().info("Getting telemetry!: " + str(msg.joint_state.shoulder_pan_joint) + ", " + str(msg.joint_state.shoulder_lift_joint) )

    def send_goal(self, joint_values):
        print(joint_values)
        goal_msg = FollowJointTrajectory.Goal()
        
        traj = JointTrajectory()
        traj.joint_names = self._joint_names

        point = JointTrajectoryPoint()
        point.positions = joint_values
                  
        point.time_from_start = Duration(seconds=90.0).to_msg()  
        traj.points = [point]
        
        goal_msg.goal_tolerance = self.getTolerances(0.2)
        goal_msg.goal_time_tolerance = Duration(seconds=30.0).to_msg()
        
        goal_msg.trajectory = traj
        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback = self.feedback_callback )
        self._send_goal_future.add_done_callback(self.goal_response_callback)
        self._is_robot_moving = True

        
#########################
def main(args=None):

    rclpy.init(args=args)
 
    action_client = SendCommand()
    rclpy.spin(action_client)
    
if __name__ == '__main__':
    main()
