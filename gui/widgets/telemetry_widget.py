import math
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout


class TelemetryWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        title = QLabel('Telemetry')
        title.setStyleSheet('font-size: 18px; font-weight: bold;')
        layout.addWidget(title)

        grid = QGridLayout()
        layout.addLayout(grid)

        grid.addWidget(QLabel('Battery Voltage:'), 0, 0)
        self.battery_label = QLabel('-- V')
        grid.addWidget(self.battery_label, 0, 1)

        grid.addWidget(QLabel('IMU Roll:'), 1, 0)
        self.roll_label = QLabel('-- °')
        grid.addWidget(self.roll_label, 1, 1)

        grid.addWidget(QLabel('IMU Pitch:'), 2, 0)
        self.pitch_label = QLabel('-- °')
        grid.addWidget(self.pitch_label, 2, 1)

        grid.addWidget(QLabel('IMU Yaw:'), 3, 0)
        self.yaw_label = QLabel('-- °')
        grid.addWidget(self.yaw_label, 3, 1)

        layout.addStretch()

    def on_battery(self, voltage: float):
        self.battery_label.setText(f'{voltage:.2f} V')

    def on_imu(self, msg):
        self.roll_label.setText(f'{math.degrees(msg.orientation.x):.1f} °')
        self.pitch_label.setText(f'{math.degrees(msg.orientation.y):.1f} °')
        self.yaw_label.setText(f'{math.degrees(msg.orientation.z):.1f} °')
