"""
Main window layout skeleton.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QSizePolicy
)
from PyQt6.QtCore import Qt

from ui.mission_sm_widget import MissionSmWidget


def _placeholder_box(title: str, min_width: int = 0, min_height: int = 0) -> QFrame:
    """Small helper to make a labeled placeholder box with a visible border,
    so the layout skeleton is legible before real widgets exist."""
    frame = QFrame()
    frame.setFrameShape(QFrame.Shape.StyledPanel)
    frame.setStyleSheet(
        "QFrame { border: 1px dashed #3a3a3a; border-radius: 4px; background: #111; }"
    )
    if min_width:
        frame.setMinimumWidth(min_width)
    if min_height:
        frame.setMinimumHeight(min_height)

    label = QLabel(title)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet("color: #666; font-size: 11px; border: none;")
    label.setWordWrap(True)

    layout = QVBoxLayout(frame)
    layout.addWidget(label)
    return frame


class ElectricalHealthCluster(QWidget):
    """Single row of electrical/safety indicators, stretched to fill all
    remaining width in the top strip (from the right edge of Subsystem
    Launch to the right edge of the window). Thermal now lives here at
    mission-critical visibility per team decision, rather than being
    buried in the Diagnostics tab."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.fault_latched = _placeholder_box("FAULT\nLATCHED", min_height=60)
        self.contactor_status = _placeholder_box("CONTACTOR\ncmd vs actual", min_height=60)
        self.current_limiter_fault = _placeholder_box("I_LIMITER\nFAULT", min_height=60)
        self.precharge_state = _placeholder_box("PRECHARGE\nSTATE", min_height=60)
        self.battery_voltage = _placeholder_box("BATTERY\nV / SOC", min_height=60)
        self.comms_health = _placeholder_box("COMMS\nHEALTH", min_height=60)
        self.thermal = _placeholder_box("THERMAL\n(THERM1-3)", min_height=60)

        for w in (
            self.fault_latched,
            self.contactor_status,
            self.current_limiter_fault,
            self.precharge_state,
            self.battery_voltage,
            self.comms_health,
            self.thermal,
        ):
            w.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            layout.addWidget(w, 1)


class TopStrip(QWidget):
    """Always-visible strip, three sections left-to-right:
      1. Mission State Machine (state, timer, controls)
      2. Subsystem Launch (Science / Arm / None)
      3. Electrical health cluster, pushed to the top-right corner
    E-stop and software enable/disable live in the sidebar now, not here.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(170)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(12)

        self.mission_sm_widget = MissionSmWidget()
        self.mission_sm_widget.setMinimumWidth(280)
        self.subsystem_launch = _placeholder_box(
            "SUBSYSTEM LAUNCH\n(Science / Arm / None)",
            min_width=220,
        )
        self.electrical_cluster = ElectricalHealthCluster()

        layout.addWidget(self.mission_sm_widget)
        layout.addWidget(self.subsystem_launch)
        layout.addWidget(self.electrical_cluster, 1)


class Sidebar(QWidget):
    """Right-hand column: GNSS map fills most of the space. E-stop and
    the software enable/disable toggle are pinned to the bottom-right
    corner, always visible regardless of active tab."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(340)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(8)

        self.gnss_map = _placeholder_box(
            "GNSS MAP\n(offline tiles, heading arrow, manual pin entry)",
            min_height=320,
        )
        self.gnss_map.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        layout.addWidget(self.gnss_map)
        layout.addStretch()

        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(8)

        self.software_toggle = _placeholder_box("SOFTWARE\nENABLE/DISABLE", min_width=140, min_height=70)
        self.estop_button = _placeholder_box("E-STOP", min_width=140, min_height=70)
        self.estop_button.setStyleSheet(
            "QFrame { border: 2px solid #ff4a4a; border-radius: 4px; background: #1a0a0a; }"
        )

        bottom_row.addWidget(self.software_toggle)
        bottom_row.addWidget(self.estop_button)
        layout.addLayout(bottom_row)


def _placeholder_tab(title: str) -> QWidget:
    tab = QWidget()
    layout = QVBoxLayout(tab)
    layout.addWidget(_placeholder_box(f"{title} TAB CONTENTS"))
    return tab


class MainWindow(QMainWindow):

    def __init__(self, data_source=None):
        super().__init__()
        self.data_source = data_source  # unused for now, wired in step 2

        self.setWindowTitle("Rover Base Station")

        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # -- top strip --------------------------------------------------
        self.top_strip = TopStrip()
        root_layout.addWidget(self.top_strip)

        # -- main content: tabs (left) + sidebar (right) ----------------
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(6, 6, 6, 6)
        content_layout.setSpacing(6)

        self.tabs = QTabWidget()
        self.tabs.addTab(_placeholder_tab("Science"), "Science")
        self.tabs.addTab(_placeholder_tab("Delivery"), "Delivery")
        self.tabs.addTab(_placeholder_tab("Equipment Servicing"), "Equipment Servicing")
        self.tabs.addTab(_placeholder_tab("Autonomous Nav"), "Autonomous Nav")
        self.tabs.addTab(_placeholder_tab("Diagnostics"), "Diagnostics")

        self.tabs.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.sidebar = Sidebar()

        content_layout.addWidget(self.tabs)
        content_layout.addWidget(self.sidebar)

        root_layout.addWidget(content)