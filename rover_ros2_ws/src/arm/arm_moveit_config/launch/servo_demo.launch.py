"""
Copied and modified from servo_example.launch.py in moveit_servo launch directory
in official MoveIt2 humble repo.
"""



import os
import yaml
from launch import LaunchDescription
from launch_ros.actions import Node, ComposableNodeContainer
from ament_index_python.packages import get_package_share_directory
from moveit_configs_utils import MoveItConfigsBuilder
from launch.actions import DeclareLaunchArgument, ExecuteProcess, RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch.substitutions import LaunchConfiguration
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
    # Setup launch arguments
    use_fake_hardware_arg = DeclareLaunchArgument(
        "use_fake_hardware",
        default_value="true",
        description="Use fake ros2_control hardware"
    )
    
    use_fake_hardware = LaunchConfiguration("use_fake_hardware")
    
    # Setup configs
    # Note how we are passing in the launch arg into the robot description file
    moveit_config = (
        MoveItConfigsBuilder("arm", package_name="arm_moveit_config")
        .robot_description(file_path="config/arm.urdf.xacro", mappings={"use_fake_hardware": use_fake_hardware})
        .robot_description_semantic(file_path="config/arm.srdf")
        .robot_description_kinematics(file_path="config/kinematics.yaml")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .planning_scene_monitor(publish_robot_description=True)
        .to_moveit_configs()
    )
    
    if not use_fake_hardware:
        # Create arm hardware nodes
        base_node = Node(
            package="odrive_can",
            executable="odrive_can_node",
            name="base_can_node",
            namespace="base",
            parameters=[{"node_id": 16, "interface": "can0"}]
        )
        
        shoulder_node = Node(
            package="cubemars_can",
            executable="cubemars_can_node",
            name="shoulder_can_node",
            namespace="shoulder",
            parameters=[{"node_id": 17, "interface": "can0", "pole_pairs": 14}]
        )
        
        elbow_node = Node(
            package="cubemars_can",
            executable="cubemars_can_node",
            name="elbow_can_node",
            namespace="elbow",
            parameters=[{"node_id": 18, "interface": "can0", "pole_pairs": 14}]
        )
        
        wrist_pitch_node = Node(
            package="cubemars_can",
            executable="cubemars_can_node",
            name="wrist_pitch_can_node",
            namespace="wrist_pitch",
            parameters=[{"node_id": 19, "interface": "can0", "pole_pairs": 14}]
        )
        
        wrist_roll_node = Node(
            package="servo",
            executable="servo_node",
            name="wrist_roll_node",
            namespace="wrist_roll",
            parameters=[{"channel_id": 0, 
                         "initial_angle_deg": 135,
                         "min_angle_deg": 0,
                         "max_angle_deg": 270,
                         "min_pwm_micro_s": 500,
                         "max_pwm_micro_s": 2500}]
        )
        
        solenoid_actuator_node = Node(
            package="stepper_can",
            executable="stepper_can_node",
            name="solenoid_actuator_node",
            namespace="solenoid",
            parameters=[{"node_id": 20, "interface": "can0"}]
        )
        
        gripper_node = Node(
            package="servo",
            executable="servo_node",
            name="gripper_node",
            namespace="gripper",
            parameters=[{"channel_id": 1, 
                         "initial_angle_deg": 135,
                         "min_angle_deg": 0,
                         "max_angle_deg": 270,
                         "min_pwm_micro_s": 500,
                         "max_pwm_micro_s": 2500}]
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
    
    # Arm driver node
    arm_driver_node = Node(
        package="arm_hardware_interface",
        executable="arm_driver_node",
        name="arm_driver_node",
    )

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

    # Only include hardware nodes if using real hardware
    if use_fake_hardware:
        return LaunchDescription(
            [ 
                use_fake_hardware_arg,
                rviz_node, 
                arm_driver_node,
                ros2_control_node,
                container,
                move_group_node,
                joint_state_broadcaster_spawner,
                arm_controller_spawner,
                gripper_controller_spawner,
                servo_node,
                gamepad_node,
                on_servo_start
            ]
        )
    else:
        return LaunchDescription(
            [ 
                use_fake_hardware_arg,
                rviz_node, 
                arm_driver_node,
                ros2_control_node,
                container,
                move_group_node,
                joint_state_broadcaster_spawner,
                arm_controller_spawner,
                gripper_controller_spawner,
                servo_node,
                gamepad_node,
                on_servo_start,
                base_node,
                shoulder_node,
                elbow_node,
                wrist_pitch_node,
                wrist_roll_node,
                solenoid_actuator_node,
                gripper_node
            ]
        )