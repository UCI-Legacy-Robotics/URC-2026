import math
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QFrame
)
from PyQt6.QtCore import Qt
from widgets.camera_widget import CameraWidget
from widgets.telemetry_widget import TelemetryWidget
from widgets.gnss_widget import GnssWidget
from widgets.status_widget import StatusWidget


class _OperatorTelemetryBar(QWidget):
    """Compact telemetry strip pinned to the bottom of the Operator tab."""

    _LABEL_STYLE = 'color: #cccccc; font-size: 14px; font-family: monospace;'
    _KEY_STYLE   = 'color: #555555; font-size: 11px; font-family: monospace;'

    def __init__(self):
        super().__init__()
        self.setFixedHeight(52)
        self.setStyleSheet('background: #111111; border-top: 1px solid #2a2a2a;')

        layout = QHBoxLayout(self)
        layout.setContentsMargins(32, 0, 32, 0)
        layout.setSpacing(0)

        self._battery = self._field('BATTERY', '-- V')
        self._roll    = self._field('ROLL',    '--°')
        self._pitch   = self._field('PITCH',   '--°')
        self._yaw     = self._field('YAW',     '--°')

        fields = [self._battery, self._roll, self._pitch, self._yaw]
        for i, (key_lbl, val_lbl) in enumerate(fields):
            if i > 0:
                sep = QFrame()
                sep.setFrameShape(QFrame.Shape.VLine)
                sep.setStyleSheet('color: #2a2a2a;')
                layout.addWidget(sep)
            cell = QWidget()
            cell_layout = QVBoxLayout(cell)
            cell_layout.setContentsMargins(0, 6, 0, 6)
            cell_layout.setSpacing(1)
            cell_layout.addWidget(key_lbl)
            cell_layout.addWidget(val_lbl)
            layout.addWidget(cell, stretch=1)

    def _field(self, key: str, default: str):
        key_lbl = QLabel(key)
        key_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        key_lbl.setStyleSheet(self._KEY_STYLE)

        val_lbl = QLabel(default)
        val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        val_lbl.setStyleSheet(self._LABEL_STYLE)

        return key_lbl, val_lbl

    def on_battery(self, voltage: float):
        self._battery[1].setText(f'{voltage:.1f} V')

    def on_imu(self, msg):
        self._roll[1].setText(f'{math.degrees(msg.orientation.x):.1f}°')
        self._pitch[1].setText(f'{math.degrees(msg.orientation.y):.1f}°')
        self._yaw[1].setText(f'{math.degrees(msg.orientation.z):.1f}°')


class MainWindow(QMainWindow):
    def __init__(self, node):
        super().__init__()
        self.node = node
        self.setWindowTitle('Rover Base Station')

        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        layout.addWidget(self.tabs)

        self._build_tabs()

    def _build_tabs(self):
        # --- Operator tab ---
        operator_tab = QWidget()
        op_layout = QVBoxLayout(operator_tab)
        op_layout.setContentsMargins(0, 0, 0, 0)
        op_layout.setSpacing(0)

        top = QWidget()
        top_layout = QHBoxLayout(top)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(1)

        self.camera_widget = CameraWidget()
        self.gnss_widget = GnssWidget()

        top_layout.addWidget(self.camera_widget, stretch=2)
        top_layout.addWidget(self.gnss_widget, stretch=3)

        op_layout.addWidget(top, stretch=1)

        self.operator_bar = _OperatorTelemetryBar()
        op_layout.addWidget(self.operator_bar)

        self.tabs.addTab(operator_tab, 'Operator')

        # --- Telemetry tab ---
        self.telemetry_widget = TelemetryWidget()
        self.tabs.addTab(self.telemetry_widget, 'Telemetry')

        # --- Status tab ---
        self.status_widget = StatusWidget()
        self.tabs.addTab(self.status_widget, 'Status')

        # --- Signal wiring ---
        self.node.camera_frame.connect(self.camera_widget.on_frame)
        self.node.gnss_fix.connect(self.gnss_widget.on_gnss_fix)

        self.node.battery_update.connect(self.operator_bar.on_battery)
        self.node.imu_update.connect(self.operator_bar.on_imu)

        self.node.imu_update.connect(self.telemetry_widget.on_imu)
        self.node.battery_update.connect(self.telemetry_widget.on_battery)

        self.node.diagnostics_update.connect(self.status_widget.on_diagnostics)
