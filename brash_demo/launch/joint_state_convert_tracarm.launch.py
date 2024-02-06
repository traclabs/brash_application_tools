import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

#####################################
def generate_launch_description():

  js_convert = Node(
          package='brash_demo',
          executable='joint_state_convert',
          name='joint_state_convert',
          output='screen',
          parameters=[
            {"joint_names": ["joint0", "joint1", "joint2", "joint3", "joint4", "joint5", "joint6"]} 
          ]) 

  return LaunchDescription(
      [
       js_convert
      ]
  )
  

