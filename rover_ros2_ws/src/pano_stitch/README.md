# pano_stitch_ros2

ROS2 (Humble) node that wraps the panoramic stitching pipeline (cylindrical
warp -> SIFT + RANSAC homography chaining -> weighted blend -> hole
inpainting -> crop) as an on-demand service, so it can run live against a
ZED2 camera feed instead of a folder of saved images.

## How it works

- Subscribes to `image_topic` (default: `/zed2/zed_node/left/image_rect_color`)
  and keeps a rolling buffer of the last `max_buffer_size` frames (default 8).
- `~/clear_buffer` (std_srvs/Trigger) empties the buffer — call this before
  panning so old frames don't get mixed in.
- `~/stitch` (std_srvs/Trigger) stitches whatever is currently buffered and
  publishes the result on `~/panorama` (sensor_msgs/Image).

This matches an "operator pans the rover, then triggers a stitch" workflow
rather than stitching every incoming frame continuously.

## Build

```bash
# copy/symlink this package into your workspace's src/ folder, then:
cd ~/ros2_ws
colcon build --packages-select pano_stitch_ros2
source install/setup.bash
```

## Run

```bash
ros2 launch pano_stitch_ros2 pano_stitch.launch.py
```

Or with a different topic/buffer size:

```bash
ros2 run pano_stitch_ros2 pano_stitch_node --ros-args \
  -p image_topic:=/zed2/zed_node/left/image_rect_color \
  -p max_buffer_size:=10
```

## Trigger a stitch

```bash
# reset the buffer before a new pan
ros2 service call /pano_stitch_node/clear_buffer std_srvs/srv/Trigger {}

# ...pan the camera...

# stitch whatever was collected
ros2 service call /pano_stitch_node/stitch std_srvs/srv/Trigger {}

# view the result
ros2 run rqt_image_view rqt_image_view /pano_stitch_node/panorama
```

## Notes / things worth knowing before you demo this

- **Not build-tested in this environment** (no ROS2 install / no network
  access in this sandbox) — double check the `cv_bridge` include against
  your exact Humble patch version. Most Humble installs use
  `cv_bridge/cv_bridge.h`; a few newer patched installs use `.hpp`. If the
  build fails on that include, that's the first thing to swap.
- The blend step averages overlapping pixels rather than using a seam mask,
  so anything that moved between frames (leaves, people, camera translation
  instead of pure rotation) will show up as ghosting — this is a known
  limitation of the current pipeline, not a bug introduced here.
- Good metrics to log/report from this node for write-ups or a resume bullet:
  number of frames successfully stitched, RANSAC inlier ratio per pair
  (already computed in `computeHomography`, just needs an `RCLCPP_INFO` line
  added if you want it in the node logs), and stitch success/failure rate
  across trigger calls.
