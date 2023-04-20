import json
import os
import yaml

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    KEY_DEBUG_TOPICS = "debug_topics"
    KEY_TOPIC_PATH_DEPTH = "topic_path_depth"

    declared_arguments = []

    declared_arguments.append(
        DeclareLaunchArgument(
            KEY_DEBUG_TOPICS, default_value="true",
            description="If true, graspable objects will be published as a ROS topic.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            KEY_TOPIC_PATH_DEPTH, default_value="/head_camera/depth_registered/points",
            description="Path of pointcloud topic from which graspable objects will be found.",
        )
    )
    # Convert "true" (str) to "True" (bool). Ref. https://stackoverflow.com/a/54684248/577001
    val_debug_topics = json.loads(LaunchConfiguration(KEY_DEBUG_TOPICS))
    val_topic_path_depth = LaunchConfiguration(KEY_TOPIC_PATH_DEPTH)

    # Graspable objs finder
    graspable_objs_finder = Node(
        #name="Graspable objs finder",
        package="simple_grasping",
        executable="basic_grasping_perception_node",
        output="screen",
        parameters=[{KEY_DEBUG_TOPICS: val_debug_topics},
                    {KEY_TOPIC_PATH_DEPTH: val_topic_path_depth}],
    )
    return LaunchDescription(declared_arguments + graspable_objs_finder)
