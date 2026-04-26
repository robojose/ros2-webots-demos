#!/bin/bash
set -e

echo "🖥️  Starting virtual display (Xvfb)..."
Xvfb :99 -screen 0 1280x1024x24 &
export DISPLAY=:99
sleep 2

echo "🤖 Sourcing ROS2 environment..."
source /opt/ros/humble/setup.bash
source /ros2_ws/install/setup.bash

export WEBOTS_HOME=/usr/local/webots
export PYTHONPATH=/usr/local/webots/lib/controller/python:$PYTHONPATH
export LD_LIBRARY_PATH=/usr/local/webots/lib/controller:$LD_LIBRARY_PATH

echo "🌍 Launching Webots with simple_room world..."
webots --stdout --stderr --batch /worlds/simple_room.wbt &
WEBOTS_PID=$!

echo "⏳ Waiting for Webots socket..."
for i in $(seq 1 30); do
    if [ -d /tmp/webots/user ]; then
        echo "✅ Webots socket ready after ${i}s"
        break
    fi
    sleep 1
done

echo "🚀 Launching ROS2 driver + wall_avoider node..."
ros2 launch wall_avoider robot_launch.py &
NODE_PID=$!

echo "✅ Everything running. Press Ctrl+C to stop."

trap "echo 'Shutting down...'; kill $NODE_PID $WEBOTS_PID 2>/dev/null; exit 0" SIGINT SIGTERM

wait $WEBOTS_PID || sleep infinity
