from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg = get_package_share_directory('patrolbot_description')
    nav2_params_yaml = os.path.join(pkg, 'config', 'amcl_params.yaml')
    map_params_yaml = os.path.join(pkg,'maps','patrolbot_map.yaml')
    rviz_config_file = os.path.join(pkg,'rviz','nav2.rviz')



    map_server_node = Node(
                     package ='nav2_map_server',
                     executable='map_server',
                     name = 'map_server',
                     output = 'screen',
                     parameters=[{"yaml_filename":map_params_yaml},
                                 {"use_sim_time":True}],
                        emulate_tty = True)


    amcl_node = Node(
     package='nav2_amcl',
     executable='amcl',
     name='amcl',
     output='screen',
     parameters=[nav2_params_yaml,
                 {"use_sim_time":True}],
     )
    
    lifecycle_node = Node(
         package='nav2_lifecycle_manager',
         executable='lifecycle_manager',
         name = 'lifecycle_localization',
         output = 'screen',
         arguments=['--ros-args','--log-level','info'],
         parameters=[{'use_sim_time':True},
                     {'autostart':True},
                     {'node_names':['map_server','amcl']}]
                     )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': True}]
    )



    return LaunchDescription([amcl_node,map_server_node,lifecycle_node,rviz_node])