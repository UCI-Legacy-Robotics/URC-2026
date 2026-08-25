# yolo_detector

ROS 2 wrapper around a YOLO object detector.

The node subscribes to a `sensor_msgs/msg/Image`, converts the frame to BGR,
runs `yolo_detector.detector_api.Detector.detect(frame)`, and publishes:

- `/yolo/detections` as `vision_msgs/msg/Detection2DArray`
- `/yolo/detections_json` as `std_msgs/msg/String`
- `/yolo/debug_image` as `sensor_msgs/msg/Image` when enabled

`yolo_detector/detector_api.py` is vendored from
`UCI-Legacy-Robotics/yolo-object-factory` (`object_detection/detector_api.py`),
so this package builds and runs without that repo installed. Keep the copy in
sync when the upstream API changes.

## Runtime Setup

The detector loads Ultralytics lazily, so it must be installed in the same
Python environment ROS runs in:

```bash
python3 -m pip install ultralytics
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
  image_topic:=/camera1/image_raw
```

With `model_path` unset the node loads the bundled `models/yolo11s.pt`, which
is installed to `share/yolo_detector/models/`. That is the stock COCO
checkpoint, useful for bring-up but not trained on URC targets. Point at a
trained model to override it:

```bash
ros2 launch yolo_detector yolo_detector.launch.py \
  model_path:=/path/to/best.engine \
  image_topic:=/camera1/image_raw
```

`model_path` accepts a `.pt`, `.onnx`, or `.engine` file; Ultralytics picks the
runtime from the extension. On the Jetson prefer an `.engine` exported at the
same `imgsz` the node is configured with.

For a ZED camera, set `image_topic` to the RGB image topic published by the ZED
wrapper, for example the camera's `rgb/image_rect_color` topic.
