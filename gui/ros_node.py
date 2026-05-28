import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from PyQt6.QtCore import QObject, pyqtSignal

from sensor_msgs.msg import Image, NavSatFix, BatteryState, Imu
from diagnostic_msgs.msg import DiagnosticArray


class RosSignals(QObject):
    """Qt signal carrier — QObject only, no ROS inheritance."""
    camera_frame       = pyqtSignal(object)
    gnss_fix           = pyqtSignal(float, float)
    battery_update     = pyqtSignal(float)
    imu_update         = pyqtSignal(object)
    diagnostics_update = pyqtSignal(object)


class BaseStationNode(Node):
    """Pure ROS2 node — no Qt inheritance."""

    def __init__(self):
        super().__init__('base_station_gui')
        self.signals = RosSignals()

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
