import os
import yaml
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch_ros.substitutions import FindPackageShare
import xacro

#####################################
def generate_launch_description():

  
  # rosbridge_server for openmct
  bridge_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
          PathJoinSubstitution(
        [get_package_share_directory("brash_application_tools"), 'launch', 'rosbridge_websocket.launch.py'])
        ]),
        launch_arguments = {
          'port': '9080',
          'address': '10.5.0.2'          
        }.items()
    )

  # Run openmct
  openmct_node = ExecuteProcess( 
    cmd = ['npm', 'start', '--prefix', "/code/openmct_ros"],
    shell = True
    )  
    
  
  return LaunchDescription(
      [
       bridge_server,
       openmct_node
      ]
  )
