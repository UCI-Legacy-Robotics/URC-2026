import math
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QGridLayout
)
from PyQt6.QtCore import Qt
from widgets.camera_widget import CameraWidget
from widgets.telemetry_widget import TelemetryWidget
from widgets.gnss_widget import GnssWidget
from widgets.status_widget import StatusWidget

_CELL_BG   = '#222222'
_KEY_STYLE = 'background: transparent; color: #555; font-size: 10px; font-family: monospace;'
_VAL_STYLE = 'background: transparent; color: #e0e0e0; font-size: 22px; font-family: monospace; font-weight: bold;'
_LBL_STYLE = 'background: transparent; color: #444; font-size: 10px; font-family: monospace; letter-spacing: 2px;'


def _labeled_widget(widget, text):
    """Wrap a widget with a small label in the top-left corner, outside the widget background."""
    wrapper = QWidget()
    vbox = QVBoxLayout(wrapper)
    vbox.setContentsMargins(0, 0, 0, 0)
    vbox.setSpacing(4)
    vbox.setAlignment(Qt.AlignmentFlag.AlignTop)

    lbl = QLabel(text)
    lbl.setFixedHeight(16)
    lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    lbl.setStyleSheet(_LBL_STYLE)

    vbox.addWidget(lbl)
    vbox.addWidget(widget)
    return wrapper


class _TelemetryPanel(QWidget):
    """Square 300×300 data panel shown on the Operator tab."""

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 300)
        self.setObjectName('telemetryPanel')
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet('#telemetryPanel { background-color: #1a1a1a; border-radius: 6px; }')

        grid = QGridLayout(self)
        grid.setContentsMargins(10, 10, 10, 10)
        grid.setSpacing(8)

        self._battery = self._cell(grid, 0, 0, 'BATTERY', '-- V')
        self._roll    = self._cell(grid, 0, 1, 'ROLL',    '--°')
        self._pitch   = self._cell(grid, 1, 0, 'PITCH',   '--°')
        self._yaw     = self._cell(grid, 1, 1, 'YAW',     '--°')

    def _cell(self, grid, row, col, key, default):
        cell = QWidget()
        cell.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        cell.setStyleSheet(f'background-color: {_CELL_BG}; border-radius: 4px;')

        layout = QVBoxLayout(cell)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(2)

        key_lbl = QLabel(key)
        key_lbl.setStyleSheet(_KEY_STYLE)

        val_lbl = QLabel(default)
        val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        val_lbl.setStyleSheet(_VAL_STYLE)

        layout.addWidget(key_lbl)
        layout.addWidget(val_lbl, stretch=1)

        grid.addWidget(cell, row, col)
        return val_lbl

    def on_battery(self, voltage: float):
        self._battery.setText(f'{voltage:.1f} V')

    def on_imu(self, msg):
        self._roll.setText(f'{math.degrees(msg.orientation.x):.1f}°')
        self._pitch.setText(f'{math.degrees(msg.orientation.y):.1f}°')
        self._yaw.setText(f'{math.degrees(msg.orientation.z):.1f}°')


class MainWindow(QMainWindow):
    def __init__(self, node):
        super().__init__()
        self.node = node
        self.setWindowTitle('Legacy Base Station')

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
        # --- Operator tab: centered, fixed-size widgets ---
        operator_tab = QWidget()
        op_layout = QVBoxLayout(operator_tab)
        op_layout.setContentsMargins(0, 0, 0, 0)

        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(12)
        row_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.camera_widget = CameraWidget()
        self.gnss_widget = GnssWidget()
        self.operator_panel = _TelemetryPanel()

        row_layout.addWidget(_labeled_widget(self.camera_widget,   'CAMERA'))
        row_layout.addWidget(_labeled_widget(self.gnss_widget,     'GNSS MAP'))
        row_layout.addWidget(_labeled_widget(self.operator_panel,  'TELEMETRY'))

        op_layout.addStretch()
        op_layout.addWidget(row, alignment=Qt.AlignmentFlag.AlignHCenter)
        op_layout.addStretch()
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

        self.node.battery_update.connect(self.operator_panel.on_battery)
        self.node.imu_update.connect(self.operator_panel.on_imu)

        self.node.imu_update.connect(self.telemetry_widget.on_imu)
        self.node.battery_update.connect(self.telemetry_widget.on_battery)

        self.node.diagnostics_update.connect(self.status_widget.on_diagnostics)
