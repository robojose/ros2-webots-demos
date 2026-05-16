FROM osrf/ros:humble-desktop

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    xvfb x11vnc x11-utils wget curl git \
    libxkbcommon-x11-0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
    libxcb-randr0 libxcb-render-util0 libxcb-xinerama0 libxcb-xfixes0 \
    libgl1-mesa-glx libgl1-mesa-dri mesa-utils python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q https://github.com/cyberbotics/webots/releases/download/R2025a/webots_2025a_amd64.deb -O /tmp/webots.deb \
    && apt-get update \
    && apt-get install -y /tmp/webots.deb \
    && rm /tmp/webots.deb \
    && rm -rf /var/lib/apt/lists/*

ENV WEBOTS_HOME=/usr/local/webots
ENV PATH=$WEBOTS_HOME:$PATH
ENV LD_LIBRARY_PATH=/usr/local/webots/lib/controller

RUN apt-get update && apt-get install -y \
    ros-humble-webots-ros2 \
    ros-humble-diff-drive-controller \
    ros-humble-joint-state-broadcaster \
    && rm -rf /var/lib/apt/lists/*

ENV ROS_WS=/ros2_ws
RUN mkdir -p $ROS_WS/src

COPY wall_avoider/ $ROS_WS/src/wall_avoider/

SHELL ["/bin/bash", "-c"]
RUN source /opt/ros/humble/setup.bash \
    && cd $ROS_WS \
    && colcon build \
    && rm -rf build log

COPY worlds/ /worlds/
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]