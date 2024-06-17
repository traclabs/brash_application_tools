import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

#####################################
def generate_launch_description():

  # Start the twist_odom_converter
  launch_astrobee = IncludeLaunchDescription(
      PythonLaunchDescriptionSource([
          PathJoinSubstitution([
              get_package_share_directory('astrobee_craftsman_support'), 
              'launch', 'bumble_demo.launch.py'
          ])
      ]),      
      launch_arguments={
        'rosbridge': 'False',
      }.items()              
  )
  
  # Converter
  astrobee_convert_node = Node(
          package='brash_application_tools',
          executable='astrobee_cmd_pose_convert.py',
          name='astrobee_cmd_pose_convert',
          output='screen',
          ) 
          
  ld = LaunchDescription()
  ld.add_action(launch_astrobee)
  ld.add_action(astrobee_convert_node)
  return ld
  

