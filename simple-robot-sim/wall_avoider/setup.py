from setuptools import setup
import os
from glob import glob

package_name = 'wall_avoider'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Register launch files
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),
        # Register resource files (URDF)
        (os.path.join('share', package_name, 'resource'),
            glob('resource/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user@example.com',
    description='Wall avoider robot using Webots + ROS2',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'wall_avoider_node = wall_avoider.wall_avoider_node:main',
        ],
    },
)
