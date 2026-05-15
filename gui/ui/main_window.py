from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget
)
from widgets.camera_widget import CameraWidget
from widgets.telemetry_widget import TelemetryWidget
from widgets.gnss_widget import GnssWidget
from widgets.status_widget import StatusWidget


class MainWindow(QMainWindow):
    def __init__(self, node):
        super().__init__()
        self.node = node

        self.setWindowTitle('Rover Base Station')
        self.setMinimumSize(1280, 800)

        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        layout.setContentsMargins(8, 8, 8, 8)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self._build_tabs()

    def _build_tabs(self):
        operator_tab = QWidget()
        operator_layout = QHBoxLayout(operator_tab)

        self.camera_widget = CameraWidget()
        self.gnss_widget = GnssWidget()

        operator_layout.addWidget(self.camera_widget, stretch=2)
        operator_layout.addWidget(self.gnss_widget, stretch=1)

        self.tabs.addTab(operator_tab, 'Operator')

        self.telemetry_widget = TelemetryWidget()
        self.tabs.addTab(self.telemetry_widget, 'Telemetry')

        self.status_widget = StatusWidget()
        self.tabs.addTab(self.status_widget, 'Status')

        self.node.camera_frame.connect(self.camera_widget.on_frame)
        self.node.gnss_fix.connect(self.gnss_widget.on_gnss_fix)
        self.node.imu_update.connect(self.telemetry_widget.on_imu)
        self.node.battery_update.connect(self.telemetry_widget.on_battery)
        self.node.diagnostics_update.connect(self.status_widget.on_diagnostics)
