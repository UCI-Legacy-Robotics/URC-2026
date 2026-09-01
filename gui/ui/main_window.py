"""
Main window layout skeleton.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QSizePolicy
)
from PyQt6.QtCore import Qt

from state_machine import MissionState, HealthStateMachine
from comms_health_controller import CommsHealthController
from widgets.mission_sm_widget import MissionSmWidget
from widgets.subsystem_launch_widget import SubsystemLaunchWidget
from widgets.control_mode_widget import ControlModeWidget
from widgets.electrical_health_cluster import ElectricalHealthCluster
from widgets.software_enable_widget import SoftwareEnableWidget
from widgets.estop_widget import EstopWidget
from widgets.gnss_map_widget import GnssMapWidget
from widgets.science_tab_widget import ScienceTabWidget


# Which subsystem is implied by which mission — MainWindow applies this
# automatically on mission state changes so operators don't have to pick
# it manually.
_SUBSYSTEM_MODE_BY_MISSION_STATE = {
    MissionState.SCIENCE: "SCIENCE",
    MissionState.DELIVERY: "ARM",
    MissionState.EQUIPMENT_SERVICING: "ARM",
    MissionState.AUTONOMOUS_NAV: "NONE",
    MissionState.IDLE: "NONE",
}

# Tab indices, matching the addTab() order below — used to lock tab
# switching to whichever mission is active. Diagnostics has no entry
# here and no ties to MissionStateMachine at all; it's exempted from
# the lock below by index so it stays reachable at all times.
_TAB_INDEX_BY_MISSION_STATE = {
    MissionState.SCIENCE: 0,
    MissionState.DELIVERY: 1,
    MissionState.EQUIPMENT_SERVICING: 2,
    MissionState.AUTONOMOUS_NAV: 3,
}
_DIAGNOSTICS_TAB_INDEX = 4

# Rover control mode implied by mission state — only Autonomous Nav
# drives itself, every other active mission is teleoperated, and there's
# no drive mode at all outside a mission.
_CONTROL_MODE_BY_MISSION_STATE = {
    MissionState.SCIENCE: "TELEOPERATION",
    MissionState.DELIVERY: "TELEOPERATION",
    MissionState.EQUIPMENT_SERVICING: "TELEOPERATION",
    MissionState.AUTONOMOUS_NAV: "AUTONOMOUS",
    MissionState.IDLE: "STANDBY",
}


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
        self.subsystem_launch = SubsystemLaunchWidget()
        self.subsystem_launch.setMinimumWidth(220)
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

        self.gnss_map = GnssMapWidget()
        self.gnss_map.setMinimumHeight(220)
        self.gnss_map.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        layout.addWidget(self.gnss_map)
        layout.addStretch()

        self.control_mode = ControlModeWidget()
        self.control_mode.setMinimumHeight(60)
        layout.addWidget(self.control_mode)

        bottom_stack = QVBoxLayout()
        bottom_stack.setSpacing(8)

        self.software_toggle = SoftwareEnableWidget()
        self.software_toggle.setMinimumHeight(110)
        self.estop_button = EstopWidget()
        self.estop_button.setMinimumHeight(110)

        bottom_stack.addWidget(self.software_toggle)
        bottom_stack.addWidget(self.estop_button)
        layout.addLayout(bottom_stack)


def _placeholder_tab(title: str) -> QWidget:
    tab = QWidget()
    layout = QVBoxLayout(tab)
    layout.addWidget(_placeholder_box(f"{title} TAB CONTENTS"))
    return tab


class MainWindow(QMainWindow):

    def __init__(self, data_source=None):
        super().__init__()
        self.data_source = data_source

        self.setWindowTitle("Rover Base Station")

        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # -- top strip --------------------------------------------------
        self.top_strip = TopStrip()
        root_layout.addWidget(self.top_strip)

        state_machine = self.top_strip.mission_sm_widget.state_machine
        state_machine.state_changed.connect(self._on_mission_state_changed)
        state_machine.mission_started.connect(self._on_mission_started_lock_tabs)
        state_machine.mission_ended.connect(self._on_mission_ended_unlock_tabs)

        subsystem_launch = self.top_strip.subsystem_launch
        subsystem_launch.launch_requested.connect(self._on_subsystem_launch_requested)
        subsystem_launch.stop_requested.connect(self._on_subsystem_stop_requested)

        self.health_state_machine = HealthStateMachine()
        self.comms_health_controller = CommsHealthController(self.health_state_machine)
        self.health_state_machine.state_changed.connect(self._on_health_state_changed)

        if self.data_source is not None:
            self.data_source.signals.subsystem_status_update.connect(
                subsystem_launch.set_status
            )
            self.data_source.signals.heartbeat.connect(
                self.comms_health_controller.on_heartbeat
            )
            self.top_strip.electrical_cluster.bind_data_source(self.data_source)

        # -- main content: tabs (left) + sidebar (right) ----------------
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(6, 6, 6, 6)
        content_layout.setSpacing(6)

        self.tabs = QTabWidget()
        self.science_tab = ScienceTabWidget()
        self.science_tab.launch_requested.connect(self._on_science_launch_requested)
        self.science_tab.stop_requested.connect(self._on_science_stop_requested)
        self.tabs.addTab(self.science_tab, "Science")
        self.tabs.addTab(_placeholder_tab("Delivery"), "Delivery")
        self.tabs.addTab(_placeholder_tab("Equipment Servicing"), "Equipment Servicing")
        self.tabs.addTab(_placeholder_tab("Autonomous Nav"), "Autonomous Nav")
        self.tabs.addTab(_placeholder_tab("Diagnostics"), "Diagnostics")

        self.tabs.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.sidebar = Sidebar()

        software_toggle = self.sidebar.software_toggle
        software_toggle.enable_requested.connect(self._on_software_enable_requested)

        estop_button = self.sidebar.estop_button
        estop_button.estop_requested.connect(self._on_estop_requested)

        if self.data_source is not None:
            self.data_source.signals.software_enable_ack.connect(software_toggle.set_ack)
            self.data_source.signals.estop_confirmed.connect(estop_button.set_confirmed)
            self.sidebar.gnss_map.bind_data_source(self.data_source)
            self.science_tab.bind_data_source(self.data_source)
            self.data_source.signals.subsystem_status_update.connect(
                self.science_tab.set_science_subsystem_status
            )
            self.data_source.signals.rover_control_mode.connect(
                self.sidebar.control_mode.set_mode
            )

        content_layout.addWidget(self.tabs)
        content_layout.addWidget(self.sidebar)

        root_layout.addWidget(content)

    def _on_mission_state_changed(self, old_state, new_state):
        self.sidebar.control_mode.set_mode(
            _CONTROL_MODE_BY_MISSION_STATE.get(new_state, "STANDBY")
        )

        # Stop whatever subsystem the OLD mission had running (bug fix:
        # set_mode() below only resets the widget's own displayed status
        # to IDLE — it never actually stops anything, so a mission reset
        # while its subsystem was RUNNING left it running for real, and
        # anything gated on subsystem_status_update, like the camera
        # MUX, never saw it stop). Must run before set_mode() below,
        # since that's what overwrites the status this check reads.
        self.top_strip.subsystem_launch.stop_if_running()

        mode = _SUBSYSTEM_MODE_BY_MISSION_STATE.get(new_state, "NONE")
        self.top_strip.subsystem_launch.set_mode(mode)
        self.science_tab.set_subsystem_mode(mode)

    def _on_mission_started_lock_tabs(self, mission_state):
        active_index = _TAB_INDEX_BY_MISSION_STATE.get(mission_state)
        if active_index is None:
            return
        self.tabs.setCurrentIndex(active_index)
        for i in range(self.tabs.count()):
            self.tabs.setTabEnabled(i, i == active_index or i == _DIAGNOSTICS_TAB_INDEX)

    def _on_mission_ended_unlock_tabs(self, ended_state):
        for i in range(self.tabs.count()):
            self.tabs.setTabEnabled(i, True)

    def _on_subsystem_launch_requested(self, subsystem):
        if self.data_source is not None:
            self.data_source.send_subsystem_command(subsystem, "launch")

    def _on_subsystem_stop_requested(self, subsystem):
        if self.data_source is not None:
            self.data_source.send_subsystem_command(subsystem, "stop")

    def _on_science_launch_requested(self, sequence, mode):
        if self.data_source is not None:
            self.data_source.send_science_sequence_command(sequence, "launch", mode)

    def _on_science_stop_requested(self, sequence):
        if self.data_source is not None:
            self.data_source.send_science_sequence_command(sequence, "stop")

    def _on_health_state_changed(self, old_state, new_state):
        self.top_strip.electrical_cluster.comms_health.set_health_state(new_state)

    def _on_software_enable_requested(self, enabled):
        if self.data_source is not None:
            self.data_source.send_software_enable_command(enabled)

    def _on_estop_requested(self):
        if self.data_source is not None:
            self.data_source.send_estop_request()