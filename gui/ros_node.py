import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from PyQt6.QtCore import QObject, pyqtSignal

from sensor_msgs.msg import Image, NavSatFix, BatteryState, Imu
from diagnostic_msgs.msg import DiagnosticArray


class BaseStationNode(Node, QObject):
    camera_frame       = pyqtSignal(object)
    gnss_fix           = pyqtSignal(float, float)
    battery_update     = pyqtSignal(float)
    imu_update         = pyqtSignal(object)
    diagnostics_update = pyqtSignal(object)

    def __init__(self):
        Node.__init__(self, 'base_station_gui')
        QObject.__init__(self)

        self.create_subscription(
            Image, '/image_raw', self.on_camera, qos_profile_sensor_data)
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
        self.camera_frame.emit(msg)

    def on_gnss(self, msg):
        self.gnss_fix.emit(msg.latitude, msg.longitude)

    def on_battery(self, msg):
        self.battery_update.emit(msg.voltage)

    def on_imu(self, msg):
        self.imu_update.emit(msg)

    def on_diagnostics(self, msg):
        self.diagnostics_update.emit(msg)
