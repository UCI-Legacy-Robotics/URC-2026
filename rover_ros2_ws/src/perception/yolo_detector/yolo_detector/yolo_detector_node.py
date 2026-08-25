import json
import os
from pathlib import Path
from typing import Any, Iterable, Optional

# cv_bridge and the message packages are C extensions built against the NumPy
# that ROS was packaged with. Importing them under a different NumPy major
# version fails deep inside the extension with "AttributeError: _ARRAY_API not
# found", which says nothing about the actual problem, so translate it here.
try:
    import rclpy
    from ament_index_python.packages import (
        PackageNotFoundError,
        get_package_share_directory,
    )
    from cv_bridge import CvBridge, CvBridgeError
    from rclpy.node import Node
    from rclpy.qos import qos_profile_sensor_data
    from sensor_msgs.msg import Image
    from std_msgs.msg import String
    from vision_msgs.msg import (
        Detection2D,
        Detection2DArray,
        ObjectHypothesisWithPose,
    )

    from yolo_detector.detector_api import Detection, Detector
except (ImportError, AttributeError) as exc:
    _reason = str(exc)
    if '_ARRAY_API' not in _reason and 'numpy' not in _reason.lower():
        raise
    try:
        import numpy

        _loaded = f'{numpy.__version__} from {numpy.__file__}'
    except Exception:  # noqa: BLE001 - numpy is what is broken here.
        _loaded = 'unknown'
    raise ImportError(
        'NumPy ABI mismatch. A ROS C extension (cv_bridge or a message '
        'package) was compiled against a different NumPy major version than '
        f'the one being loaded: {_loaded}. This usually means pip installed '
        'NumPy 2.x into ~/.local while ROS was built against the apt NumPy '
        '1.x, and ~/.local takes priority on sys.path. Pin NumPy to match '
        'the ROS build:\n'
        '    python3 -m pip install "numpy<2"\n'
        'Ultralytics only requires numpy>=1.23, so it is unaffected. Then '
        'check that one NumPy is visible:\n'
        '    python3 -c "import numpy; print(numpy.__version__, numpy.__file__)"'
    ) from exc

PACKAGE_NAME = 'yolo_detector'

# Models live in exactly one place: models/ in the source package, installed to
# share/yolo_detector/models/. There is no second copy anywhere, and nothing
# resolves a model relative to the working directory.
MODELS_DIR_NAME = 'models'
DEFAULT_MODEL_FILE = 'yolo11s.pt'


class YoloDetectorNode(Node):
    def __init__(self) -> None:
        super().__init__('yolo_detector_node')

        self._declare_parameters()
        self.bridge = CvBridge()
        self.detector = self._create_detector()
        self._last_inference_time: Optional[float] = None
        self._cv2 = None
        self._warned_debug_import = False

        image_topic = self._str_param('image_topic')
        self.detections_pub = self.create_publisher(
            Detection2DArray,
            self._str_param('detections_topic'),
            10,
        )

        self.publish_json = self._bool_param('publish_json')
        self.json_pub = None
        if self.publish_json:
            self.json_pub = self.create_publisher(
                String,
                self._str_param('detections_json_topic'),
                10,
            )

        self.publish_debug_image = self._bool_param('publish_debug_image')
        self.debug_image_pub = None
        if self.publish_debug_image:
            self.debug_image_pub = self.create_publisher(
                Image,
                self._str_param('debug_image_topic'),
                10,
            )

        self.image_sub = self.create_subscription(
            Image,
            image_topic,
            self._image_callback,
            qos_profile_sensor_data,
        )

        self.get_logger().info(
            f"YOLO detector subscribed to {image_topic} and publishing "
            f"{self._str_param('detections_topic')}"
        )

    def _declare_parameters(self) -> None:
        self.declare_parameter('image_topic', '/camera1/image_raw')
        self.declare_parameter('detections_topic', '/yolo/detections')
        self.declare_parameter('detections_json_topic', '/yolo/detections_json')
        self.declare_parameter('debug_image_topic', '/yolo/debug_image')
        self.declare_parameter('model_path', '')
        self.declare_parameter('confidence_threshold', 0.25)
        self.declare_parameter('imgsz', 640)
        self.declare_parameter('device', '0')
        self.declare_parameter('image_encoding', 'bgr8')
        self.declare_parameter('max_fps', 10.0)
        self.declare_parameter('publish_json', True)
        self.declare_parameter('publish_debug_image', False)

    def _create_detector(self) -> Detector:
        model_path = self._resolve_model_path()
        device = self._parse_device(self._str_param('device'))
        self.get_logger().info(
            f"Loading YOLO model {model_path} with conf="
            f"{self._float_param('confidence_threshold')}, "
            f"imgsz={self._int_param('imgsz')}, device={device}"
        )
        try:
            return Detector(
                model_path=model_path,
                conf=self._float_param('confidence_threshold'),
                imgsz=self._int_param('imgsz'),
                device=device,
            )
        except ImportError as exc:
            # Detector imports Ultralytics lazily, so a missing dependency
            # surfaces here rather than at import time.
            raise RuntimeError(
                'Could not load the YOLO model. Install Ultralytics into the '
                'Python environment ROS runs in: python3 -m pip install '
                'ultralytics'
            ) from exc

    def _image_callback(self, msg: Image) -> None:
        if self._should_skip_frame():
            return

        try:
            frame = self.bridge.imgmsg_to_cv2(
                msg,
                desired_encoding=self._str_param('image_encoding'),
            )
        except CvBridgeError as exc:
            self.get_logger().error(f"Failed to convert image: {exc}")
            return

        try:
            detections = self.detector.detect(frame)
        except Exception as exc:  # noqa: BLE001 - keep ROS callback alive.
            self.get_logger().error(f"YOLO inference failed: {exc}")
            return

        self.detections_pub.publish(self._to_detection_array(msg, detections))

        if self.json_pub is not None:
            self.json_pub.publish(self._to_json_message(msg, detections))

        if self.debug_image_pub is not None:
            self._publish_debug_image(msg, frame, detections)

    def _should_skip_frame(self) -> bool:
        max_fps = self._float_param('max_fps')
        if max_fps <= 0.0:
            return False

        now = self.get_clock().now().nanoseconds / 1_000_000_000.0
        if self._last_inference_time is None:
            self._last_inference_time = now
            return False

        min_period = 1.0 / max_fps
        if now - self._last_inference_time < min_period:
            return True

        self._last_inference_time = now
        return False

    def _to_detection_array(
        self,
        image_msg: Image,
        detections: Iterable[Detection],
    ) -> Detection2DArray:
        array_msg = Detection2DArray()
        array_msg.header = image_msg.header
        array_msg.detections = [
            self._to_detection_msg(image_msg, detection)
            for detection in detections
        ]
        return array_msg

    def _to_detection_msg(
        self,
        image_msg: Image,
        detection: Detection,
    ) -> Detection2D:
        x1, y1, x2, y2 = detection.bbox
        width = max(0.0, float(x2 - x1))
        height = max(0.0, float(y2 - y1))

        detection_msg = Detection2D()
        if hasattr(detection_msg, 'header'):
            detection_msg.header = image_msg.header

        hypothesis = ObjectHypothesisWithPose()
        if hasattr(hypothesis.hypothesis, 'class_id'):
            hypothesis.hypothesis.class_id = str(detection.class_name)
        elif hasattr(hypothesis.hypothesis, 'id'):
            hypothesis.hypothesis.id = int(detection.class_id)
        hypothesis.hypothesis.score = float(detection.confidence)
        detection_msg.results.append(hypothesis)

        center = detection_msg.bbox.center
        center_x = float(x1) + width / 2.0
        center_y = float(y1) + height / 2.0
        if hasattr(center, 'position'):
            center.position.x = center_x
            center.position.y = center_y
            if hasattr(center, 'theta'):
                center.theta = 0.0
        else:
            center.x = center_x
            center.y = center_y
            center.theta = 0.0

        detection_msg.bbox.size_x = width
        detection_msg.bbox.size_y = height
        return detection_msg

    def _to_json_message(
        self,
        image_msg: Image,
        detections: Iterable[Detection],
    ) -> String:
        payload = {
            'stamp': {
                'sec': image_msg.header.stamp.sec,
                'nanosec': image_msg.header.stamp.nanosec,
            },
            'frame_id': image_msg.header.frame_id,
            'detections': [
                {
                    'class_name': detection.class_name,
                    'class_id': int(detection.class_id),
                    'confidence': float(detection.confidence),
                    'bbox': [int(value) for value in detection.bbox],
                }
                for detection in detections
            ],
        }
        msg = String()
        msg.data = json.dumps(payload, separators=(',', ':'))
        return msg

    def _publish_debug_image(
        self,
        image_msg: Image,
        frame: Any,
        detections: Iterable[Detection],
    ) -> None:
        cv2 = self._load_cv2()
        if cv2 is None:
            return

        annotated = frame.copy()
        for detection in detections:
            x1, y1, x2, y2 = (int(value) for value in detection.bbox)
            label = f"{detection.class_name} {detection.confidence:.2f}"
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                annotated,
                label,
                (x1, max(0, y1 - 8)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1,
                cv2.LINE_AA,
            )

        debug_msg = self.bridge.cv2_to_imgmsg(
            annotated,
            encoding=self._str_param('image_encoding'),
        )
        debug_msg.header = image_msg.header
        self.debug_image_pub.publish(debug_msg)

    def _load_cv2(self) -> Optional[Any]:
        if self._cv2 is not None:
            return self._cv2

        try:
            import cv2
        except ImportError:
            if not self._warned_debug_import:
                self.get_logger().warn(
                    'publish_debug_image is enabled, but cv2 is unavailable.'
                )
                self._warned_debug_import = True
            return None

        self._cv2 = cv2
        return self._cv2

    def _resolve_model_path(self) -> str:
        """Resolve the one model file this node will load.

        There are exactly two sources, in priority order: an explicit
        model_path parameter, or the checkpoint bundled in this package's
        share directory. The result is always an absolute path to a file that
        exists and is readable.

        That last guarantee is the point. Ultralytics interprets a path it
        cannot find as the *name* of a downloadable asset and tries to create
        the parent directory to download into, so a wrong model_path surfaces
        as "Permission denied: /yolo" from deep inside Ultralytics rather than
        as a missing-file error. Failing here keeps the message actionable.
        """
        configured = self._str_param('model_path').strip()
        if configured:
            path = Path(os.path.expandvars(configured)).expanduser()
            source = 'the model_path parameter'
        else:
            path = self._bundled_model_path()
            source = f'the bundled {DEFAULT_MODEL_FILE}'

        # Absolute, so the model never depends on the node's working
        # directory - which under ros2 launch is not the package directory.
        path = path.absolute()

        if not path.is_file():
            raise RuntimeError(
                f"Model file not found: {path} (from {source}). Set model_path "
                f"to a .pt, .onnx, or .engine file, or leave it empty to use "
                f"the bundled {DEFAULT_MODEL_FILE}."
            )
        if not os.access(path, os.R_OK):
            raise RuntimeError(
                f"Model file is not readable: {path} ({self._describe_perms(path)}). "
                f"Fix the file's permissions, or run the node as a user that "
                f"can read it."
            )

        self.get_logger().info(f"Using model {path} (from {source})")
        return str(path)

    @staticmethod
    def _bundled_model_path() -> Path:
        """Path to the checkpoint installed alongside this package."""
        try:
            share_dir = get_package_share_directory(PACKAGE_NAME)
        except PackageNotFoundError as exc:
            raise RuntimeError(
                f"Package '{PACKAGE_NAME}' is not on the ament index, so the "
                f"bundled {DEFAULT_MODEL_FILE} cannot be located. Source the "
                f"workspace's install/setup.bash, or set model_path explicitly."
            ) from exc
        return Path(share_dir) / MODELS_DIR_NAME / DEFAULT_MODEL_FILE

    @staticmethod
    def _describe_perms(path: Path) -> str:
        """Owner and mode of a path, to make a permission failure diagnosable."""
        try:
            info = path.stat()
        except OSError as exc:
            return f'could not stat: {exc}'
        return (
            f'mode {info.st_mode & 0o777:o}, owner uid {info.st_uid}; '
            f'node runs as uid {os.getuid()}'
        )

    @staticmethod
    def _parse_device(device: str) -> Any:
        try:
            return int(device)
        except ValueError:
            return device

    def _str_param(self, name: str) -> str:
        return str(self.get_parameter(name).value)

    def _int_param(self, name: str) -> int:
        return int(self.get_parameter(name).value)

    def _float_param(self, name: str) -> float:
        return float(self.get_parameter(name).value)

    def _bool_param(self, name: str) -> bool:
        value = self.get_parameter(name).value
        if isinstance(value, bool):
            return value
        return str(value).lower() in ('1', 'true', 'yes', 'on')


def main(args=None) -> None:
    rclpy.init(args=args)
    node = None
    try:
        node = YoloDetectorNode()
        rclpy.spin(node)
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
