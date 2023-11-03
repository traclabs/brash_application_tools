import os
import yaml
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch_ros.substitutions import FindPackageShare

#####################################
def generate_launch_description():

  # Launch tracarm 
  launch_tracarm = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(PathJoinSubstitution(
      [FindPackageShare("tracarm_description"), 'launch', 'bringup_tracarm.launch.py'])))



  rviz_base = os.path.join(get_package_share_directory("brash_demo"), "rviz")
  rviz_full_config = os.path.join(rviz_base, "tracarm.rviz")
  rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_full_config]
  )

    
  # Joint State publisher
  joint_publisher = Node(
      package='joint_state_publisher_gui',
      executable='joint_state_publisher_gui',
      name='joint_state_publisher_gui',
      remappings={('joint_states', "joint_command")},
      output='screen')

  # rqt node
  rqt_node = ExecuteProcess(
    cmd = ['rqt', '--perspective-file', os.path.join(get_package_share_directory("brash_demo"), "config", "robot_sim_tracarm.perspective")],
    shell = True
    )
  

  return LaunchDescription(
      [
       launch_tracarm,
       rviz_node,
       joint_publisher,
       rqt_node
      ]
  )
