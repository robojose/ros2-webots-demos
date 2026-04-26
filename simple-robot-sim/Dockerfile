# Force amd64 for Webots Linux binary compatibility (runs via Rosetta on M2)
FROM --platform=linux/amd64 osrf/ros:humble-desktop

# Avoid interactive prompts during apt installs
ENV DEBIAN_FRONTEND=noninteractive
ENV USERNAME=user

# Virtual display + misc dependencies
RUN apt-get update && apt-get install -y \
    xvfb \
    x11-utils \
    wget \
    curl \
    libxkbcommon-x11-0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-xinerama0 \
    libxcb-xfixes0 \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    mesa-utils \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Webots R2025a (amd64 .deb from Cyberbotics)
RUN wget -q https://github.com/cyberbotics/webots/releases/download/R2025a/webots_2025a_amd64.deb -O /tmp/webots.deb \
    && apt-get update \
    && apt-get install -y /tmp/webots.deb \
    && rm /tmp/webots.deb \
    && rm -rf /var/lib/apt/lists/*

# Set Webots environment
ENV WEBOTS_HOME=/usr/local/webots
ENV PATH=$WEBOTS_HOME:$PATH
ENV LD_LIBRARY_PATH=$WEBOTS_HOME/lib/controller:$LD_LIBRARY_PATH

# Install webots_ros2 packages
RUN apt-get update && apt-get install -y \
    ros-humble-webots-ros2 \
    && rm -rf /var/lib/apt/lists/*

# Set up ROS2 workspace
ENV ROS_WS=/ros2_ws
RUN mkdir -p $ROS_WS/src

# Copy wall_avoider package into the workspace
COPY wall_avoider/ $ROS_WS/src/wall_avoider/

# Build the workspace
SHELL ["/bin/bash", "-c"]
RUN source /opt/ros/humble/setup.bash \
    && cd $ROS_WS \
    && colcon build \
    && rm -rf build log

# Copy the Webots world
COPY worlds/ /worlds/

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]