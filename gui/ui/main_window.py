"""
Main window layout skeleton.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from qfluentwidgets import CaptionLabel

from ui import theme
from widgets.shared.controls import SectionCard
from core.state_machine import MissionState, HealthStateMachine
from core.comms_health_controller import CommsHealthController
from widgets.status.mission_sm_widget import MissionSmWidget
from widgets.status.subsystem_launch_widget import SubsystemLaunchWidget
from widgets.status.control_mode_widget import ControlModeWidget
from widgets.status.joystick_mode_widget import JoystickModeWidget
from widgets.status.electrical_health_cluster import ElectricalHealthCluster
from widgets.status.software_enable_widget import SoftwareEnableWidget
from widgets.status.estop_widget import EstopWidget
from widgets.status.gnss_map_widget import GnssMapWidget
from widgets.missions.science_tab_widget import ScienceTabWidget
from widgets.missions.delivery_checklist_widget import DeliveryChecklistWidget
from widgets.missions.equipment_servicing_widget import EquipmentServicingWidget
from widgets.missions.autonomous_nav_widget import AutonomousNavWidget


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


# Tab icons in addTab() order -- indices must match
# _TAB_INDEX_BY_MISSION_STATE/_DIAGNOSTICS_TAB_INDEX above.
_TAB_ICONS = (
    "mdi6.flask-outline",
    "mdi6.package-variant-closed",
    "mdi6.wrench",
    "mdi6.navigation-variant",
    "mdi6.stethoscope",
)


def _placeholder_box(title: str) -> SectionCard:
    """Labeled placeholder card, so the layout skeleton is legible
    before real widgets exist."""
    card = SectionCard()
    label = CaptionLabel(title)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setWordWrap(True)
    card.body.addWidget(label)
    return card


def _wrap_in_card(widget: QWidget, title: str, icon_name: str) -> SectionCard:
    card = SectionCard(title, icon_name)
    card.body.addWidget(widget, 1)
    return card


class TopStrip(QWidget):
    """Always-visible strip, three sections left-to-right:
      1. Mission State Machine (state, timer, controls)
      2. Subsystem Launch (Science / Arm / None)
      3. Electrical health cluster, pushed to the top-right corner
    E-stop and software enable/disable live in the sidebar now, not here.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(200)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 0)
        layout.setSpacing(8)

        self.mission_sm_widget = MissionSmWidget()
        self.mission_sm_widget.setMinimumWidth(320)
        self.subsystem_launch = SubsystemLaunchWidget()
        self.subsystem_launch.setMinimumWidth(200)
        self.electrical_cluster = ElectricalHealthCluster()

        layout.addWidget(_wrap_in_card(self.mission_sm_widget, "Mission", "mdi6.flag-checkered"))
        layout.addWidget(_wrap_in_card(self.subsystem_launch, "Subsystem Launch", "mdi6.rocket-launch"))
        layout.addWidget(
            _wrap_in_card(self.electrical_cluster, "Electrical Health", "mdi6.lightning-bolt"), 1
        )


class Sidebar(QWidget):
    """Right-hand column: GNSS map fills most of the space. E-stop and
    the software enable/disable toggle are pinned to the bottom-right
    corner, always visible regardless of active tab."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(340)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.gnss_map = GnssMapWidget()
        self.gnss_map.setMinimumHeight(220)
        map_card = _wrap_in_card(self.gnss_map, "GNSS", "mdi6.map")
        map_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(map_card, 1)

        modes_card = SectionCard("Rover Mode", "mdi6.gamepad-variant")
        self.control_mode = ControlModeWidget()
        self.joystick_mode = JoystickModeWidget()
        modes_card.body.addWidget(self.control_mode)
        modes_card.body.addWidget(self.joystick_mode)
        layout.addWidget(modes_card)

        safety_card = SectionCard("Safety", "mdi6.shield-alert-outline")
        self.software_toggle = SoftwareEnableWidget()
        self.software_toggle.setMinimumHeight(100)
        self.estop_button = EstopWidget()
        self.estop_button.setMinimumHeight(110)
        safety_card.body.addWidget(self.software_toggle)
        safety_card.body.addWidget(self.estop_button)
        layout.addWidget(safety_card)


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
        content_layout.setContentsMargins(8, 8, 8, 8)
        content_layout.setSpacing(8)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setIconSize(QSize(18, 18))
        self.science_tab = ScienceTabWidget()
        self.science_tab.launch_requested.connect(self._on_science_launch_requested)
        self.science_tab.stop_requested.connect(self._on_science_stop_requested)
        self.equipment_tab = EquipmentServicingWidget()
        self.equipment_tab.launch_requested.connect(self._on_equipment_launch_requested)
        self.equipment_tab.stop_requested.connect(self._on_equipment_stop_requested)

        self.autonomous_nav_tab = AutonomousNavWidget()
        self.autonomous_nav_tab.launch_requested.connect(self._on_autonomous_nav_launch_requested)
        self.autonomous_nav_tab.stop_requested.connect(self._on_autonomous_nav_stop_requested)

        self.tabs.addTab(self.science_tab, "Science")
        self.tabs.addTab(DeliveryChecklistWidget(), "Delivery")
        self.tabs.addTab(self.equipment_tab, "Equipment Servicing")
        self.tabs.addTab(self.autonomous_nav_tab, "Autonomous Nav")
        self.tabs.addTab(_placeholder_tab("Diagnostics"), "Diagnostics")
        for index, icon_name in enumerate(_TAB_ICONS):
            self.tabs.setTabIcon(index, theme.icon(icon_name))

        self.tabs.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.sidebar = Sidebar()

        # Pure GUI-to-GUI wiring, independent of data_source -- a waypoint
        # entered on the Autonomous Nav tab should show up on the map
        # whether or not a real/sim telemetry feed is attached.
        self.autonomous_nav_tab.waypoint_added.connect(
            lambda waypoint_id, lat, lon, label, waypoint_type:
                self.sidebar.gnss_map.add_pin(waypoint_id, lat, lon, label, waypoint_type)
        )

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
            self.equipment_tab.bind_data_source(self.data_source)
            self.data_source.signals.subsystem_status_update.connect(
                self.equipment_tab.set_equipment_subsystem_status
            )
            self.autonomous_nav_tab.bind_data_source(self.data_source)
            self.data_source.signals.rover_control_mode.connect(
                self.sidebar.control_mode.set_mode
            )
            self.data_source.signals.joystick_mode.connect(
                self.sidebar.joystick_mode.set_mode
            )

        content_layout.addWidget(self.tabs)
        content_layout.addWidget(self.sidebar)

        root_layout.addWidget(content)

    def _on_mission_state_changed(self, old_state, new_state):
        # Control mode is NOT derived from mission state -- the rover can
        # be teleoperated by the game controller whether or not a mission
        # is even active, and self-drives specific maneuvers (e.g.
        # Panorama's rotation) independent of which mission is running.
        # It's sourced entirely from DataSource.signals.rover_control_mode
        # (see main_window.py's connection below and control_mode_widget.py).

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
        self.equipment_tab.set_mission_active(new_state == MissionState.EQUIPMENT_SERVICING)

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

    def _on_equipment_launch_requested(self, sequence, key):
        if self.data_source is not None:
            self.data_source.send_equipment_sequence_command(sequence, "launch", key)

    def _on_equipment_stop_requested(self, sequence):
        if self.data_source is not None:
            self.data_source.send_equipment_sequence_command(sequence, "stop")

    def _on_autonomous_nav_launch_requested(self, waypoint_id, lat, lon, label, waypoint_type):
        if self.data_source is not None:
            self.data_source.send_autonomous_nav_command(
                waypoint_id, "launch", lat, lon, label, waypoint_type
            )

    def _on_autonomous_nav_stop_requested(self, waypoint_id):
        if self.data_source is not None:
            self.data_source.send_autonomous_nav_command(waypoint_id, "stop")

    def _on_health_state_changed(self, old_state, new_state):
        self.top_strip.electrical_cluster.comms_health.set_health_state(new_state)

    def _on_software_enable_requested(self, enabled):
        if self.data_source is not None:
            self.data_source.send_software_enable_command(enabled)

    def _on_estop_requested(self):
        if self.data_source is not None:
            self.data_source.send_estop_request()