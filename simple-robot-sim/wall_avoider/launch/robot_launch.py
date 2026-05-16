import os
from launch import LaunchDescription
from launch_ros.actions import Node
from webots_ros2_driver.webots_controller import WebotsController


def generate_launch_description():
    # Our own minimal URDF — uses Ros2Epuck plugin, no ros2_control
    epuck_urdf = '/ros2_ws/src/wall_avoider/resource/epuck_simple.urdf'

    epuck_driver = WebotsController(
        robot_name='e-puck',
        parameters=[
            {
                'robot_description': epuck_urdf,
                'use_sim_time': True,
            },
        ],
        respawn=True,
    )

    wall_avoider_node = Node(
        package='wall_avoider',
        executable='wall_avoider_node',
        output='screen',
    )

    return LaunchDescription([
        epuck_driver,
        wall_avoider_node,
    ])
