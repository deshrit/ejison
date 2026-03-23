# Ejison [WIP]

A monocular SLAM implementation robot with Raspberry Pi and Arduino Uno board with
28BYJ48 stepper motors.

## Hardware

![ejison-image](assets/imgs/ejison-detailed.png)

The main computer of the robot is Raspberry Pi 4B. Two independent stepper motors
28BYJ-48 with ULN2003AN driver is used to drive the robot. The motors are 5V variant
and they are powered directly through the 1000mAh power bank which weight approx. 
around 200gm. At first I was also skeptical if these motor could carry robot's weight 
with accurate steps but upon testing they seems to perform pretty well. The motors are
driven by Arduino Uno board which is serially connected to the Raspberry Pi through
the USB port and commands are first send by the computer to the Arduino board. To
test driving the motors study the readme of [arduino_comm](/arduino_comm) sub-project.

The camera is connected to the computer through USB. It is an old Pelomax 
(PCW-380) with USB 1.1 and VGA (640x480) resolution that I had laying around.

## Setup and Run ROS2

```bash
UID=$(id -u) GID=$(id -g) docker compose up -d
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

## Clean up

```bash
UID=$(id -u) GID=$(id -g) docker compose down
```

## Rebuild container image

```bash
UID=$(id -u) GID=$(id -g) docker compose up --build -d
```