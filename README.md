# Ejison

A monocular SLAM implementation robot with Raspberry Pi and Arduino Uno board with
28BYJ48 stepper motors.

## Setup and Run ROS2

```bash
docker compose up -d
```

Exec into the container:

```bash
docker exec -it ejison bash
```

Check setup within the container:

```bash
source /opt/ros/jazzy/setup.bash

echo $ROS_DISTRO
```

## Rebuild container image

```bash
docker compose up --build -d
```