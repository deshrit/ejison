FROM ros:jazzy

RUN apt update \
    && apt install -y ros-jazzy-demo-nodes-cpp \
                    ros-jazzy-demo-nodes-py \
                    vim
