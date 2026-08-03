from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from sensor_msgs.msg import Image, NavSatFix, BatteryState, Imu
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus
from std_msgs.msg import Empty

from data_source import DataSource, DataSourceSignals

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

        self.create_subscription(
            Image, '/image_raw', self.on_camera, 10)
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

    def on_camera(self, msg):
        self.signals.camera_frame.emit(msg)

    def on_gnss(self, msg):
        self.signals.gnss_fix.emit(msg.latitude, msg.longitude)

    def on_battery(self, msg):
        self.signals.battery_update.emit(msg.voltage)

    def on_imu(self, msg):
        self.signals.imu_update.emit(msg)

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
