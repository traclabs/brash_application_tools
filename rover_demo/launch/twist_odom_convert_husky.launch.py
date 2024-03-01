import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

#####################################
def generate_launch_description():

  toc_convert = Node(
          package='rover_demo',
          executable='twist_odom_convert',
          name='twist_odom_convert',
          output='screen',
          parameters=[
            {"twist_cmd_cfs": "rover_app_cmd"},
            {"odom_tlm_cfs": "rover_app_hk_tlm"},
            {"odom_out": "/odom"},
            {"twist_in": "/cmd_vel"} 
          ]) 
          
  return LaunchDescription(
      [
       toc_convert
      ]
  )
  

