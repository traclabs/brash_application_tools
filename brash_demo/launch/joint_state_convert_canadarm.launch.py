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
            {"joint_names": ["Base_Joint", "Shoulder_Roll", "Shoulder_Yaw", "Elbow_Pitch", "Wrist_Pitch", "Wrist_Yaw", "Wrist_Roll"]} 
          ]) 

  return LaunchDescription(
      [
       js_convert
      ]
  )
  

