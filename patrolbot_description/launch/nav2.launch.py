import os
from os.path import join
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_patrolbot = get_package_share_directory('patrolbot_description')
    pkg_nav2 = get_package_share_directory('nav2_bringup')

    # 1. Launch Configurations
    use_sim_time = LaunchConfiguration('use_sim_time')
    params_file = LaunchConfiguration('params_file')

    # 2. Path to your custom config inside fastbot_description
    default_params_file = join(pkg_patrolbot, 'config', 'nav2_params.yaml')

    # 3. Declare Launch Arguments
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation clock if true'
    )

    declare_params_file_cmd = DeclareLaunchArgument(
        'params_file',
        default_value=default_params_file,
        description='Full path to the ROS 2 parameters file to use for Nav2'
    )

    # 4. Include Nav2 and pass 'params_file' directly in launch_arguments
    start_nav2_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            join(pkg_nav2, 'launch', 'navigation_launch.py')  # or bringup_launch.py
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'params_file': params_file, # <--- Here is where your custom params are forwarded
            'autostart': 'true'
        }.items()
    )

    return LaunchDescription([
        declare_use_sim_time_cmd,
        declare_params_file_cmd,
        start_nav2_cmd
    ])