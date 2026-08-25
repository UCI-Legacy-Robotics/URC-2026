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
Python environment ROS runs in. Pin NumPy in the same command: Ultralytics
accepts anything `>=1.23`, so pip will otherwise pull NumPy 2.x, which breaks
`cv_bridge` and the message packages built against the apt NumPy 1.x (see
Troubleshooting):

```bash
python3 -m pip install ultralytics "numpy<2"
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

## Where models live

There is one models directory and no second copy:

| | |
|---|---|
| Source | `models/` in this package |
| Installed | `share/yolo_detector/models/` |
| Selected by | `model_path` (empty = bundled `yolo11s.pt`) |

Drop new `.pt`, `.onnx`, or `.engine` files into `models/` and rebuild to have
them installed, or leave a trained model outside the workspace and point
`model_path` at it with an absolute path. Do not add model files anywhere else
in the package — nothing will look for them there.

## Troubleshooting

**`Permission denied` / `Read-only file system` mentioning a model directory.**
`model_path` pointed at a file that does not exist. Ultralytics reads an
unresolvable path as the *name* of a model to download and tries to create the
parent directory to download into, so a bad path fails as a permission error on
that directory rather than as a missing file. A hardcoded `/yolo/yolo11s.pt`
caused exactly this: `/yolo` is at the filesystem root, which a non-root user
cannot create. The node now checks the file exists and is readable before
handing it to Ultralytics, so this surfaces as `Model file not found: <path>`.

Relative paths are a common source of this — the node's working directory under
`ros2 launch` is not the package directory. Use an absolute path, or leave
`model_path` empty.

**`Permission denied` writing an Ultralytics settings or font file.** Ultralytics
keeps a config dir at `~/.config/Ultralytics`. Recent versions fall back to
`/tmp` when that is not writable; if the Jetson's version does not, set
`YOLO_CONFIG_DIR` to a writable directory before launching.

**`AttributeError: _ARRAY_API not found`, usually with a wall of NumPy text
about modules compiled against NumPy 1.x.** Two NumPy major versions are in
play. `cv_bridge` and the message packages are C extensions built against the
apt NumPy that ROS was packaged with (1.x); `pip install ultralytics` pulls
NumPy 2.x into `~/.local/lib/python3.*/site-packages`, which comes *before*
`/usr/lib/python3/dist-packages` on `sys.path`. The extension then loads under
the wrong ABI and fails.

Pin NumPy to match the ROS build. Ultralytics only requires `numpy>=1.23`, so
it keeps working:

```bash
python3 -m pip install "numpy<2"
```

Then confirm exactly one NumPy is visible to the interpreter ROS uses:

```bash
python3 -c "import numpy; print(numpy.__version__, numpy.__file__)"
```

It should print a `1.x` version. If it still prints `2.x` from `~/.local`, that
copy is shadowing the apt one — remove it with
`python3 -m pip uninstall numpy` and reinstall with the pin above.

The node detects this case and raises the explanation instead of the raw
`AttributeError`, but the fix is environmental: no code change makes a NumPy
1.x extension load under NumPy 2.x.
