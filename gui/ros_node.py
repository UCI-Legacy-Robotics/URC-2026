from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from sensor_msgs.msg import Image, NavSatFix, BatteryState, Imu
from diagnostic_msgs.msg import DiagnosticArray

from data_source import DataSource, DataSourceSignals


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
        self.signals.diagnostics_update.emit(msg)


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
