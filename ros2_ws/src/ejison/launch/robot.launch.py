from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    motor_driver = Node(package="ejison", executable="motor_driver")
    serial_bridge = Node(
        package="ejison",
        executable="serial_bridge",
    )
    return LaunchDescription(
        [
            motor_driver,
            serial_bridge,
        ]
    )
