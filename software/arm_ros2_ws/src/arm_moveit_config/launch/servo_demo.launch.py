"""
Copied and modified from servo_example.launch.py in moveit_servo launch directory
in official MoveIt2 humble repo.
"""



import os
import yaml
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from moveit_configs_utils import MoveItConfigsBuilder
from launch_ros.actions import ComposableNodeContainer
from launch.actions import ExecuteProcess, RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch_ros.descriptions import ComposableNode
from launch_param_builder import ParameterBuilder


# Util function to safely read from file within package
def load_file(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)

    try:
        with open(absolute_file_path, "r") as file:
            return file.read()
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        return None


# Util function to safely load yaml within package
def load_yaml(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)

    try:
        with open(absolute_file_path, "r") as file:
            return yaml.safe_load(file)
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        return None


def generate_launch_description():
    # Setup configs
    moveit_config = (
        MoveItConfigsBuilder("arm", package_name="arm_moveit_config")
        .robot_description(file_path="config/arm.urdf.xacro")
        .robot_description_semantic(file_path="config/arm.srdf")
        .robot_description_kinematics(file_path="config/kinematics.yaml")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .planning_scene_monitor(publish_robot_description=True)
        .to_moveit_configs()
    )

    # Get parameters for the Servo node
    # servo_yaml_path = os.path.join(
    #   get_package_share_directory("arm_moveit_config"),
    #   "config",
    #   "servo_settings.yaml"
    # )
    servo_yaml = load_yaml("arm_moveit_config", "config/servo_settings.yaml")
    servo_params = {"moveit_servo": servo_yaml}
    
    # Define nodes below

    # ros2_control using FakeSystem as hardware
    ros2_controllers_path = os.path.join(
        get_package_share_directory("arm_moveit_config"),
        "config",
        "ros2_controllers.yaml"
    )
    ros2_control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[moveit_config.robot_description, ros2_controllers_path],
        output="screen"
    )
    
    # Move group
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_config.to_dict()
        ]
    )
    
    # RViz
    # Only if we want to define custom rviz settings
    # rviz_config_file = (
    #     get_package_share_directory("arm_moveit_config") + "/config/demo_rviz_config.rviz"
    # )
    
    # Note we are using default moveit.rviz config file below
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", 
                   os.path.join(
                     moveit_config.package_path,
                     "config",
                     "moveit.rviz"
                   )
        ],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
        ]
    )

    # Define joint state broadcaster (for physical components)
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager-timeout",
            "300",
            "--controller-manager",
            "/controller_manager",
        ],
    )

    # Define controller spawners
    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["arm_controller", "-c", "/controller_manager"],
    )
    
    gripper_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["gripper_controller", "-c", "/controller_manager"],
    )
    
    container = ComposableNodeContainer(
        name="moveit_servo_demo_container",
        namespace="/",
        package="rclcpp_components",
        executable="component_container",
        composable_node_descriptions=[
            ComposableNode(
                package="robot_state_publisher",
                plugin="robot_state_publisher::RobotStatePublisher",
                name="robot_state_publisher",
                parameters=[moveit_config.robot_description],
            ),
            ComposableNode(
                package="tf2_ros",
                plugin="tf2_ros::StaticTransformBroadcasterNode",
                name="static_tf2_broadcaster",
                parameters=[{"child_frame_id": "/base_dummy", "frame_id": "/world"}],
            ),
            ComposableNode(
                package="joy",
                plugin="joy::Joy",
                name="joy_node",
                # extra_arguments=[{"use_intra_process_comms": True}],
            )
        ],
        output="screen",
    )
    
    # Servo node (IMPORTANT THAT IT GOES LATER SINCE IT RELIES ON OTHER THINGS)
    servo_node = Node(
        package="moveit_servo",
        executable="servo_node_main",
        name="servo_node",
        output="screen",
        parameters=[
            servo_params,
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics
        ]
    )
    
    # Gamepad node
    gamepad_node = Node(
        package="arm_gamepad_teleop",
        executable="arm_teleop",
        name="arm_teleop",
        output="screen",
    )
    
    # Automatically force start servo
    start_servo_service_call = ExecuteProcess(
        cmd=['ros2', 'service', 'call', '/servo_node/start_servo', 'std_srvs/srv/Trigger', '{}'],
        output='screen'
    )

    # Register an event handler to call the service once the servo_node has started
    # This ensures the service call happens only after the service server is active
    on_servo_start = RegisterEventHandler(
        OnProcessStart(
            target_action=servo_node,
            on_start=[start_servo_service_call],
        )
    )

    return LaunchDescription(
        [ 
            rviz_node, 
            ros2_control_node,
            container,
            move_group_node,
            joint_state_broadcaster_spawner,
            arm_controller_spawner,
            gripper_controller_spawner,
            servo_node,
            gamepad_node, # Not running for now since I want to control separately
            on_servo_start
        ]
    )