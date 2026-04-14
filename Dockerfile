# FROM arm64v8/ros:jazzy-ros-base
FROM ros:jazzy-ros-base


RUN apt update && apt install -y --no-install-recommends \
    python3-opencv \
    python3-serial \
    vim \
    && rm -rf /var/lib/apt/lists/*

RUN apt update && apt install -y \
    ros-jazzy-demo-nodes-cpp \
    ros-jazzy-cv-bridge \
    ros-jazzy-image-transport-plugins \
    && rm -rf /var/lib/apt/lists/*

