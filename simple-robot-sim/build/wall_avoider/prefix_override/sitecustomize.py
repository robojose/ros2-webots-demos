import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/ros2-webots-demos/simple-robot-sim/install/wall_avoider'
