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

  # rqt node - Send twist commands
  rqt_node = ExecuteProcess(
    cmd = ['rqt', '--perspective-file', os.path.join(get_package_share_directory("rover_demo"), "config", "rover_app_husky.perspective")],
    shell = True
    )

  # Rviz visualization of odometry
  rviz_base = os.path.join(get_package_share_directory("rover_demo"), "rviz")
  rviz_full_config = os.path.join(rviz_base, "husky_rover.rviz")
  rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_full_config]
  )

  # Start the twist_odom_converter
  launch_to_converter = IncludeLaunchDescription(
      PythonLaunchDescriptionSource(PathJoinSubstitution(
          [FindPackageShare('rover_demo'), 
              'launch', 'ground_twist_odom_convert_husky.launch.py']))
  )
  

  return LaunchDescription(
      [
       rqt_node,
       rviz_node,
       launch_to_converter,
      ]
  )
