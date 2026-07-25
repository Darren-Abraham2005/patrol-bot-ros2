import os
from os.path import join
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():

    # Package paths
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    pkg_ros_gz_rbot = get_package_share_directory('patrolbot_description')

    # Add the resource path mapping so Gazebo Harmonic can resolve 'package://'
    # It extracts the parent directory of your shared package folder (the workspace 'install' folder)
    package_share_parent = os.path.dirname(pkg_ros_gz_rbot)
    if "GZ_SIM_RESOURCE_PATH" in os.environ:
        os.environ["GZ_SIM_RESOURCE_PATH"] += os.pathsep + package_share_parent
    else:
        os.environ["GZ_SIM_RESOURCE_PATH"] = package_share_parent

    # File paths
    robot_description_file = join(pkg_ros_gz_rbot, 'urdf', 'patrolbot.xacro')
    ros_gz_bridge_config = join(pkg_ros_gz_rbot, 'config', 'ros_gz_bridge_gazebo.yaml')
    world = join(pkg_ros_gz_rbot, 'worlds', 'obstacles.sdf')

    # Parse URDF / Xacro
    robot_description_config = xacro.process_file(robot_description_file)
    robot_description = {'robot_description': robot_description_config.toxml()}

    # Launch Arguments
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use Gazebo Simulation time'
    )
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Nodes and Actions
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            robot_description,
            {'use_sim_time': use_sim_time}
        ],
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(join(pkg_ros_gz_sim, "launch", "gz_sim.launch.py")),
        launch_arguments={"gz_args": f"-r -v 4 '{world}'"}.items()
    )

    spawn_robot = TimerAction(
        period=5.0,  # Increased to 5 seconds to ensure the Gazebo environment finishes booting
        actions=[Node(
            package='ros_gz_sim',
            executable='create',
            name='patrolbot_spawner',
            arguments=[
                "-world", "empty",  # CRITICAL: Targets your world backend name seen in the logs
                "-topic", "/robot_description",
                "-name", "patrolbot",
                "-allow_renaming", "false",
                "-x", "0.0",
                "-y", "0.0",
                "-z", "0.32",
                "-Y", "0.0"
            ],
            output='screen'
        )]
    )

    ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[
            {'config_file': ros_gz_bridge_config},
            {'use_sim_time': use_sim_time}
        ],
        output='screen'
    )

    return LaunchDescription([
        use_sim_time_arg,
        gazebo,
        robot_state_publisher,
        spawn_robot,
        ros_gz_bridge,
    ])
