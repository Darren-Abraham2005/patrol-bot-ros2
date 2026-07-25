import os
from os.path import join
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Package paths
    pkg_patrolbot = get_package_share_directory('patrolbot_description')
    pkg_slam_toolbox = get_package_share_directory('slam_toolbox')

    # Launch Configurations
    use_sim_time = LaunchConfiguration('use_sim_time')

    # File paths
    rviz_config_file = join(pkg_patrolbot, 'rviz', 'slam.rviz')

    # Launch Arguments
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true',
    )

    # 1. Include official SLAM Toolbox launch file (uses default params automatically)
    start_slam_toolbox_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            join(pkg_slam_toolbox, 'launch', 'online_async_launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
        }.items()
    )

    # 2. RViz Node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    return LaunchDescription([
        declare_use_sim_time_cmd,
        start_slam_toolbox_cmd,
        rviz_node
    ])