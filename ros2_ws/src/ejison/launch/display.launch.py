import os
import xacro
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

package_name = "ejison"
xacro_model_relative = "model/robot.urdf.xacro"
rviz_config_relative = "config/default.rviz"


def generate_launch_description():
    pkg_path = FindPackageShare(package=package_name).find(package_name)
    xacro_model_path = os.path.join(pkg_path, xacro_model_relative)
    robot_des_xml = xacro.process_file(xacro_model_path).toxml()
    params = {
        "robot_description": robot_des_xml,
    }

    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            "gui",
            default_value="true",
            description="Start RViz2 automatically with this launch file.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "use_mock_hardware",
            default_value="false",
            description="Start robot with mock hardware mirroring command to its states.",
        )
    )

    # joint_state_publisher_gui = Node(
    #     package="joint_state_publisher_gui",
    #     executable="joint_state_publisher_gui",
    # )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[params],
    )

    controller_yaml = PathJoinSubstitution(
        [FindPackageShare("ejison"), "config", "controller.yaml"]
    )

    controller_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[controller_yaml],
    )

    joint_state_broadcaster_node = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    robot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_drive_controller"],
    )

    rviz_config_path = os.path.join(pkg_path, rviz_config_relative)
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", rviz_config_path],
    )

    # gz_desc = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         [FindPackageShare("ros_gz_sim"), "/launch/gz_sim.launch.py"],
    #     ),
    #     launch_arguments=[("gz_args", "empty.sdf")],
    # )

    return LaunchDescription(
        [
            robot_state_publisher_node,
            robot_controller_spawner,
            joint_state_broadcaster_node,
            controller_node,
            rviz_node,
        ]
    )
