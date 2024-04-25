import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.time import Duration

from control_msgs.action import FollowJointTrajectory
from control_msgs.msg import JointTolerance
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState


class SendMotionCommand(Node):
    """
    Send motion command
    """
    def __init__(self):
        super().__init__('send_motion_command')
        self._action_client = ActionClient(self, FollowJointTrajectory, '/canadarm_joint_trajectory_controller/follow_joint_trajectory')
        self._joint_names = ["Base_Joint", "Shoulder_Roll", "Shoulder_Yaw", "Elbow_Pitch", "Wrist_Pitch", "Wrist_Yaw", "Wrist_Roll"]

    # 0: open 1: close 2: random
    def send_goal(self, mode):
        self.get_logger().info("Send goal start ...")
    
        goal_msg = FollowJointTrajectory.Goal()
        
        traj = JointTrajectory()
        traj.joint_names = self._joint_names

        point = JointTrajectoryPoint()
        
        if mode == 0:
          point.positions = [0.0, 0.0, 0.0, -3.1416, 0.0, 0.0, 0.0]
        elif mode == 1:
          point.positions =  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        elif mode == 2:
          point.positions = [1.0, -1.5, 2.0, -3.2, 0.8, 0.5, -1.0]  
          
        #point.velocities = []
        #point.accelerations = []
        point.time_from_start = Duration(seconds=90.0).to_msg()  
        traj.points = [point]
        
        goal_msg.goal_tolerance = self.getTolerances(0.2)
        goal_msg.goal_time_tolerance = Duration(seconds=30.0).to_msg()
        
        goal_msg.trajectory = traj
        self._action_client.wait_for_server()
        self.get_logger().info('Sending goal now for real!')

        self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback = self.feedback_callback )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result.error_string))

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback


    def getTolerances(self, dj):
        
        tolerances = []
        for ji in self._joint_names:
          jti = JointTolerance()
          jti.name = ji
          jti.position = dj 
        
          tolerances.append(jti)
        return tolerances
        
#########################
def main(args=None):

    rclpy.init(args=args)
 
    action_client = SendMotionCommand()
    action_client.send_goal(0)
    action_client.get_logger().info("Start spinning")
    rclpy.spin(action_client)
    action_client.get_logger().info("End spinning")
    
if __name__ == '__main__':
    main()
