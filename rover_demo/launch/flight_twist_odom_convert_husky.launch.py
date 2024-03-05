import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

#####################################
def generate_launch_description():

  toc_convert = Node(
          package='rover_demo',
          executable='flight_twist_odom_convert',
          name='flight_twist_odom_convert',
          output='screen',
          parameters=[
            {"twist_out_cfs": "rover_app_send_robot_command"},
            {"odom_in_cfs": "rover_app_get_robot_odom"},
            {"odom_in": "/w200_0000/platform/odom"},
            {"twist_out": "/w200_0000/cmd_vel"} 
          ]) 
          
  return LaunchDescription(
      [
       toc_convert
      ]
  )
  

