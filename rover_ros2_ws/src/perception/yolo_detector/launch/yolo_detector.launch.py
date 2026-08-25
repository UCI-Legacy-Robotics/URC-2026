from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():
    config_file = LaunchConfiguration('config_file')
    image_topic = LaunchConfiguration('image_topic')
    detections_topic = LaunchConfiguration('detections_topic')
    detections_json_topic = LaunchConfiguration('detections_json_topic')
    debug_image_topic = LaunchConfiguration('debug_image_topic')
    model_path = LaunchConfiguration('model_path')
    confidence_threshold = LaunchConfiguration('confidence_threshold')
    imgsz = LaunchConfiguration('imgsz')
    device = LaunchConfiguration('device')
    image_encoding = LaunchConfiguration('image_encoding')
    max_fps = LaunchConfiguration('max_fps')
    publish_json = LaunchConfiguration('publish_json')
    publish_debug_image = LaunchConfiguration('publish_debug_image')

    return LaunchDescription([
        DeclareLaunchArgument(
            'config_file',
            default_value=PathJoinSubstitution([
                FindPackageShare('yolo_detector'),
                'config',
                'yolo_detector.yaml',
            ]),
            description='Path to a yolo_detector ROS parameter file.',
        ),
        DeclareLaunchArgument(
            'image_topic',
            default_value='/camera1/image_raw',
            description='Input sensor_msgs/Image topic.',
        ),
        DeclareLaunchArgument(
            'detections_topic',
            default_value='/yolo/detections',
            description='Output vision_msgs/Detection2DArray topic.',
        ),
        DeclareLaunchArgument(
            'detections_json_topic',
            default_value='/yolo/detections_json',
            description='Output std_msgs/String JSON detection topic.',
        ),
        DeclareLaunchArgument(
            'debug_image_topic',
            default_value='/yolo/debug_image',
            description='Output annotated image topic.',
        ),
        DeclareLaunchArgument(
            'model_path',
            default_value='',
            description='Path to a YOLO .pt, .onnx, or .engine model. Empty '
                        'uses the bundled yolo11s.pt.',
        ),
        DeclareLaunchArgument(
            'confidence_threshold',
            default_value='0.25',
            description='YOLO confidence threshold.',
        ),
        DeclareLaunchArgument(
            'imgsz',
            default_value='640',
            description='YOLO inference image size.',
        ),
        DeclareLaunchArgument(
            'device',
            default_value='0',
            description='YOLO runtime device, e.g. 0, cuda:0, cpu, or mps.',
        ),
        DeclareLaunchArgument(
            'image_encoding',
            default_value='bgr8',
            description='cv_bridge desired encoding for incoming frames.',
        ),
        DeclareLaunchArgument(
            'max_fps',
            default_value='10.0',
            description='Maximum inference rate. Set 0.0 for no throttling.',
        ),
        DeclareLaunchArgument(
            'publish_json',
            default_value='true',
            description='Whether to publish JSON detections.',
        ),
        DeclareLaunchArgument(
            'publish_debug_image',
            default_value='false',
            description='Whether to publish annotated debug images.',
        ),
        Node(
            package='yolo_detector',
            executable='yolo_detector_node',
            name='yolo_detector_node',
            output='screen',
            parameters=[
                config_file,
                {
                    'image_topic': image_topic,
                    'detections_topic': detections_topic,
                    'detections_json_topic': detections_json_topic,
                    'debug_image_topic': debug_image_topic,
                    'model_path': model_path,
                    'confidence_threshold': ParameterValue(
                        confidence_threshold,
                        value_type=float,
                    ),
                    'imgsz': ParameterValue(imgsz, value_type=int),
                    'device': device,
                    'image_encoding': image_encoding,
                    'max_fps': ParameterValue(max_fps, value_type=float),
                    'publish_json': ParameterValue(
                        publish_json,
                        value_type=bool,
                    ),
                    'publish_debug_image': ParameterValue(
                        publish_debug_image,
                        value_type=bool,
                    ),
                },
            ],
        ),
    ])
