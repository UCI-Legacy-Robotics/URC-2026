import functools
import math
import time
from types import SimpleNamespace

from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from sensor_msgs.msg import Image, NavSatFix, BatteryState, Imu
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus
from std_msgs.msg import Empty

from data_source import DataSource, DataSourceSignals, CameraID

# TODO(camera-mux): placeholder topic names — none of these are confirmed
# with the team yet, including birds_eye (the old unconditional /image_raw
# subscription this replaced was only ever a dev-machine test webcam, not
# the real tower camera). Swap in real topics once known; nothing else
# about the subscribe/unsubscribe wiring below should need to change.
_CAMERA_TOPICS = {
    CameraID.SCIENCE_PAYLOAD.value: '/cameras/science_payload/image_raw',
    CameraID.ARM_CAM_1.value: '/cameras/arm_cam_1/image_raw',
    CameraID.ARM_CAM_2.value: '/cameras/arm_cam_2/image_raw',
    CameraID.BIRDS_EYE.value: '/cameras/birds_eye/image_raw',
}

# Translates ROS DiagnosticStatus.level (a byte) into the plain strings
# diagnostics_update carries — SimulationDataSource emits the same
# strings, so widget code never branches on which DataSource it's on.
_LEVEL_NAMES = {
    DiagnosticStatus.OK: "OK",
    DiagnosticStatus.WARN: "WARN",
    DiagnosticStatus.ERROR: "ERROR",
    DiagnosticStatus.STALE: "STALE",
}


class BaseStationNode(Node):
    """Pure ROS2 node — no Qt inheritance. Wrapped by RosDataSource below
    to conform to the DataSource interface; use RosDataSource from GUI
    code, not this class directly."""

    def __init__(self):
        super().__init__('base_station_gui')
        self.signals = DataSourceSignals()

        # All 4 cameras start disabled — no subscriptions until the MUX
        # panel calls enable_camera(), unlike the fixed subscriptions
        # below which are always live. Keyed by camera_id -> subscription
        # handle, so disable_camera() has something to destroy_subscription() on.
        self._camera_subs = {}

        self.create_subscription(
            NavSatFix, '/gnss/fix', self.on_gnss, 10)
        self.create_subscription(
            BatteryState, '/battery_state', self.on_battery, 10)
        self.create_subscription(
            Imu, '/imu/data', self.on_imu, qos_profile_sensor_data)
        self.create_subscription(
            DiagnosticArray, '/diagnostics', self.on_diagnostics, 10)
        self.create_subscription(
            Empty, '/heartbeat', self.on_heartbeat, 10)

        self.get_logger().info('Base station GUI node started')

    def enable_camera(self, camera_id: str):
        if camera_id in self._camera_subs:
            return  # already enabled
        topic = _CAMERA_TOPICS.get(camera_id)
        if topic is None:
            self.get_logger().warning(f'enable_camera: unknown camera_id {camera_id!r}')
            return
        # Depth 10, default (RELIABLE) QoS — matches the old /image_raw
        # subscription; BEST_EFFORT here silently drops a RELIABLE
        # publisher's data (see e6a2e64's WSL2 camera-feed fix).
        self._camera_subs[camera_id] = self.create_subscription(
            Image, topic, functools.partial(self._on_camera_frame, camera_id), 10)

    def disable_camera(self, camera_id: str):
        sub = self._camera_subs.pop(camera_id, None)
        if sub is not None:
            self.destroy_subscription(sub)

    def _on_camera_frame(self, camera_id, msg):
        # Normalized to SimpleNamespace(encoding, data, height, width),
        # matching what SimulationDataSource fakes — same convention as
        # imu_update/diagnostics_update above, so CameraFeedWidget's
        # decode code never touches a raw ROS message type.
        frame = SimpleNamespace(
            encoding=msg.encoding,
            data=bytes(msg.data),  # copy immediately, DDS can reclaim the buffer under us
            height=msg.height,
            width=msg.width,
        )
        self.signals.camera_frame.emit(camera_id, frame, len(frame.data), time.time())

    def on_gnss(self, msg):
        self.signals.gnss_fix.emit(msg.latitude, msg.longitude)

    def on_battery(self, msg):
        self.signals.battery_update.emit(msg.voltage)

    def on_imu(self, msg):
        # Normalized to SimpleNamespace(roll_deg, pitch_deg, yaw_deg),
        # matching what SimulationDataSource emits — never the raw ROS
        # quaternion, so widget code (e.g. the GNSS map's heading arrow)
        # has one shape to read regardless of source.
        q = msg.orientation
        yaw = math.atan2(2 * (q.w * q.z + q.x * q.y), 1 - 2 * (q.y * q.y + q.z * q.z))
        sin_pitch = max(-1.0, min(1.0, 2 * (q.w * q.y - q.z * q.x)))
        pitch = math.asin(sin_pitch)
        roll = math.atan2(2 * (q.w * q.x + q.y * q.z), 1 - 2 * (q.x * q.x + q.y * q.y))

        imu = SimpleNamespace(
            roll_deg=math.degrees(roll),
            pitch_deg=math.degrees(pitch),
            yaw_deg=math.degrees(yaw) % 360.0,
        )
        self.signals.imu_update.emit(imu)

    def on_diagnostics(self, msg):
        # Normalized to plain dicts (name/level/message/values), matching
        # what SimulationDataSource emits — never the raw ROS message, so
        # widget code has one shape to parse regardless of source.
        statuses = [
            {
                "name": status.name,
                "level": _LEVEL_NAMES.get(status.level, "ERROR"),
                "message": status.message,
                "values": {kv.key: kv.value for kv in status.values},
            }
            for status in msg.status
        ]
        self.signals.diagnostics_update.emit(statuses)

    def on_heartbeat(self, msg):
        self.signals.heartbeat.emit()


class RosDataSource(DataSource):
    """Adapts BaseStationNode to the DataSource interface used by the GUI.

    rclpy.init()/shutdown() and the spin thread are process-wide concerns
    (including the WSL2 Fast-DDS UDP-only workaround) and stay owned by
    main.py — this class only wraps the node's signals/lifecycle as far
    as the DataSource contract is concerned. The node must already exist
    (and be spinning) for signals to fire; start()/stop() here just track
    whether this source considers itself active.
    """

    def __init__(self, node: BaseStationNode = None):
        self.node = node or BaseStationNode()
        self.signals = self.node.signals

    def start(self):
        pass  # subscriptions are created at node construction; spinning is owned by main.py

    def stop(self):
        self.node.destroy_node()

    def enable_camera(self, camera_id: str):
        self.node.enable_camera(camera_id)

    def disable_camera(self, camera_id: str):
        self.node.disable_camera(camera_id)

    def send_subsystem_command(self, subsystem: str, action: str):
        # Real subsystem process management is out of scope for the GUI —
        # no launch topic/service exists yet, so just log for now.
        self.node.get_logger().info(f'subsystem command (no-op): {subsystem} -> {action}')

    def send_software_enable_command(self, enabled: bool):
        # No software-enable topic/service exists yet — log only, same as
        # subsystem commands above.
        self.node.get_logger().info(f'software enable command (no-op): {enabled}')

    def send_estop_request(self):
        # No E-Stop topic/service exists yet — log only; this is
        # deliberately never faked/auto-confirmed the way sim does, so a
        # missing real backend shows up as "no confirmation received"
        # rather than silently pretending to work.
        self.node.get_logger().info('estop request (no-op, NOT confirmed)')
