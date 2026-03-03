import os
import xacro
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

from ament_index_python.packages import get_package_share_directory

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

    joint_state_publisher_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[params],
    )

    rviz_config_path = os.path.join(pkg_path, rviz_config_relative)
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", rviz_config_path],
    )

    gz_desc = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                FindPackageShare("ros_gz_sim"), 
                "/launch/gz_sim.launch.py"
            ],
        ),
        launch_arguments=[("gz_args", "empty.sdf")],
    )

    return LaunchDescription([
        joint_state_publisher_node,
        robot_state_publisher_node,
        rviz_node,
        # gz_desc,
    ])
