#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.time import Duration

from control_msgs.action import FollowJointTrajectory
from control_msgs.msg import JointTolerance
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState

from cfe_msgs.msg import CanadarmAppRobotStatet, CanadarmAppRobotCommandt

class SendMotionCommand(Node):
    """
    Send motion command
    """
    def __init__(self):
        super().__init__('send_motion_command')
        self._action_client = ActionClient(self, FollowJointTrajectory, '/canadarm_joint_trajectory_controller/follow_joint_trajectory')
        self._publish_state = self.create_publisher(CanadarmAppRobotStatet, "/flightsystem/canadarm_app_robot_state", 10)

        self._subscribe_command = self.create_subscription(CanadarmAppRobotCommandt, "/flightsystem/canadarm_app_robot_command", self.command_cb, 10)
        self._subscribe_js = self.create_subscription(JointState, "/joint_states", self.js_cb, 10)
        
        self._joint_names = ["Base_Joint", "Shoulder_Roll", "Shoulder_Yaw", "Elbow_Pitch", "Wrist_Pitch", "Wrist_Yaw", "Wrist_Roll"]
        self._js = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self._is_robot_moving = False

    def js_cb(self, msg):
        self._js = [] 
        
        for item in msg.position:
          self._js.append(float(item))
    
        print(self._js)
        st = CanadarmAppRobotStatet()
        st.cmd_header.sec.function_code = 1
        st.state.joint_0 = self._js[0]
        st.state.joint_1 = self._js[1]
        st.state.joint_2 = self._js[2]
        st.state.joint_3 = self._js[3]
        st.state.joint_4 = self._js[4]
        st.state.joint_5 = self._js[5]
        st.state.joint_6 = self._js[6]
        st.is_robot_moving = self._is_robot_moving
        self._publish_state.publish(st)

    def command_cb(self, msg):
        self.get_logger().info("Got command for canadarm in flight side!")
        joints = [msg.goal.joint_0, msg.goal.joint_1, msg.goal.joint_2, msg.goal.joint_3, msg.goal.joint_4, msg.goal.joint_5, msg.goal.joint_6]
        self.send_goal(joints)

    def send_goal(self, joint_values):
        print(joint_values)
        goal_msg = FollowJointTrajectory.Goal()
        
        traj = JointTrajectory()
        traj.joint_names = self._joint_names

        point = JointTrajectoryPoint()
        point.positions = joint_values
                  
        #point.velocities = []
        #point.accelerations = []
        point.time_from_start = Duration(seconds=90.0).to_msg()  
        traj.points = [point]
        
        goal_msg.goal_tolerance = self.getTolerances(0.2)
        goal_msg.goal_time_tolerance = Duration(seconds=30.0).to_msg()
        
        goal_msg.trajectory = traj
        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback = self.feedback_callback )
        self._send_goal_future.add_done_callback(self.goal_response_callback)
        self._is_robot_moving = True

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
        self._is_robot_moving = False

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
    rclpy.spin(action_client)
    
if __name__ == '__main__':
    main()
