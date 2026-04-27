import os
from launch import LaunchDescription
from launch_ros.actions import Node
from webots_ros2_driver.webots_controller import WebotsController
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    epuck_urdf = os.path.join(
        get_package_share_directory('webots_ros2_epuck'),
        'resource',
        'epuck_webots.urdf'
    )
    ros2_control_params = os.path.join(
        get_package_share_directory('webots_ros2_epuck'),
        'resource',
        'ros2_control.yml'
    )

    epuck_driver = WebotsController(
        robot_name='e-puck',
        parameters=[
            {'robot_description': epuck_urdf,
             'use_sim_time': True,
             'set_robot_state_publisher': True},
            ros2_control_params,
        ],
        respawn=False,
    )

    diffdrive_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['diffdrive_controller', '--controller-manager-timeout', '30'],
        output='screen',
    )

    joint_state_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', '--controller-manager-timeout', '30'],
        output='screen',
    )

    wall_avoider_node = Node(
        package='wall_avoider',
        executable='wall_avoider_node',
        output='screen',
    )

    return LaunchDescription([
        epuck_driver,
        diffdrive_spawner,
        joint_state_spawner,
        wall_avoider_node,
    ])
        
