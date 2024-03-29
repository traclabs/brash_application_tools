
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable, LaunchConfiguration, PathJoinSubstitution


def generate_launch_description():
    # Directories
    pkg_clearpath_gz = get_package_share_directory(
        'clearpath_gz')

    # Paths
    gazebo_sim_launch = PathJoinSubstitution(
        [get_package_share_directory("rover_demo"), 'launch', 'flight_husky_simulation.launch.py'])
    twist_odom_convert_launch = PathJoinSubstitution(
        [get_package_share_directory("rover_demo"), 'launch', 'flight_twist_odom_convert_husky.launch.py'])

        
    gazebo_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([gazebo_sim_launch])
    )

    twist_odom_convert = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([twist_odom_convert_launch])
    )


    # Create launch description and add actions
    ld = LaunchDescription()
    ld.add_action(gazebo_sim)
    ld.add_action(twist_odom_convert)
    return ld
