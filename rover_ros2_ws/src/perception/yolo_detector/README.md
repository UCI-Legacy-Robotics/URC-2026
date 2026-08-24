# yolo_detector

ROS 2 wrapper for the URC YOLO detector API in
`UCI-Legacy-Robotics/yolo-object-factory`.

The node subscribes to a `sensor_msgs/msg/Image`, converts the frame to BGR,
runs `object_detection.detector_api.Detector.detect(frame)`, and publishes:

- `/yolo/detections` as `vision_msgs/msg/Detection2DArray`
- `/yolo/detections_json` as `std_msgs/msg/String`
- `/yolo/debug_image` as `sensor_msgs/msg/Image` when enabled

## Runtime Setup

Install the YOLO API repo into the same Python environment used by ROS:

```bash
git clone https://github.com/UCI-Legacy-Robotics/yolo-object-factory.git
python3 -m pip install -e yolo-object-factory
```

Install ROS dependencies if they are not already present:

```bash
sudo apt install ros-${ROS_DISTRO}-cv-bridge ros-${ROS_DISTRO}-vision-msgs
```

## Build

```bash
cd rover_ros2_ws
colcon build --packages-select yolo_detector
source install/setup.bash
```

## Run

```bash
ros2 launch yolo_detector yolo_detector.launch.py \
  model_path:=/path/to/best.engine \
  image_topic:=/camera1/image_raw
```

For a ZED camera, set `image_topic` to the RGB image topic published by the ZED
wrapper, for example the camera's `rgb/image_rect_color` topic.
