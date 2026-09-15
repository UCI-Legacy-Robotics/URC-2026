"""
Autonomous Nav tab.

Composes the Autonomous Nav Mission's controls: a plain completion
checklist (ChecklistWidget, see checklist_widget.py) listing the 7
required targets the rules fix in advance -- 2 GNSS-only locations, 2
posts, 3 objects -- so operators can track at a glance what's left
regardless of the order they're visited in, plus a GNSS waypoint form
that's simultaneously the entry point for the mission's one navigation
sequence: per the rules, every GNSS coordinate entered IS the start of
an autonomous traverse to it, there's no separate "just record a
coordinate" action. The checklist and the waypoint form are
independent -- ticking a checklist box is a manual "yes, that one's
done" note, separate from the pass/fail state the status box/store
track for whatever's actually in flight.

Unlike ScienceTabWidget/EquipmentServicingWidget there's only ever one
navigation attempt in flight, so this widget owns the sequence
handling directly rather than delegating to a per-instance
ScienceSequenceWidget-style card -- there's nothing to configure
per-instance when there's only one instance.

Data flow:
  - Submitting the form calls AutonomousNavStore.add_waypoint() (same
    "record everything, tagged, to disk" motivation as
    ScienceDataStore -- see that module's docstring), emits
    waypoint_added (MainWindow wires this to GnssMapWidget.add_pin so
    the coordinate actually shows up on the map, per the mission's own
    request) and launch_requested (MainWindow wires this to
    DataSource.send_autonomous_nav_command).
  - Status updates come back tagged by waypoint_id via set_status(),
    called from bind_data_source's autonomous_nav_status connection;
    each one is also recorded to the store, same as ScienceTabWidget
    recording every science_sequence_status into ScienceDataStore.
  - "ARRIVED" is rendered as a large, high-contrast banner (rather than
    reusing the small message box RUNNING/etc. use) -- the mission
    rules explicitly require "a large and obvious message... for the
    C2 station judge to observe" when the rover signals it has reached
    a target, distinct from STOPPED (control handed back to
    teleoperation, ready for the next instruction).

No subsystem-launch gating here (unlike Science/Equipment Servicing):
Autonomous Nav maps to subsystem mode "NONE" in
_SUBSYSTEM_MODE_BY_MISSION_STATE (main_window.py) -- there's no
separate subsystem process this mission needs confirmed running first,
so the normal mission-tab-lock (only this tab is enabled while
Autonomous Nav is the active mission) is gating enough, same as
Delivery.
"""

from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QDoubleSpinBox, QPushButton, QListWidget, QListWidgetItem, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal

from widgets.checklist_widget import ChecklistWidget
from widgets.color_coded_label import ColorCodedLabel
from autonomous_nav_store import AutonomousNavStore

_DEFAULT_CHECKLIST_PATH = Path(__file__).resolve().parent.parent / "autonomous_nav_checklist.json"

_STATUS_COLORS = {
    "IDLE": "#3a3a3a",
    "STARTING": "#8a6d1a",
    "RUNNING": "#1b5e20",
    "ARRIVED": "#1b5e20",
    "STOPPING": "#8a6d1a",
    "STOPPED": "#3a3a3a",
    "ERROR": "#7a1f1f",
}
_RUNNING_LIKE_STATUSES = ("STARTING", "RUNNING")

# (display label, stored value) -- stored value is exactly the
# "accurate"/"object"/"post" vocabulary from the mission rules and from
# app.js's PIN_TYPE_COLORS.
_WAYPOINT_TYPES = [
    ("Accurate (GNSS-only)", "accurate"),
    ("Post (AR tag)", "post"),
    ("Object", "object"),
]
_TYPE_DISPLAY_BY_VALUE = {value: display for display, value in _WAYPOINT_TYPES}

_ENTRY_STYLE = (
    "QLineEdit, QComboBox, QDoubleSpinBox { font-size: 14px; color: #e0e0e0; "
    "background: #1a1a1a; border: 1px solid #555; border-radius: 4px; padding: 4px; } "
    "QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus { border: 1px solid #888; }"
)
_BUTTON_STYLE = (
    "QPushButton { font-size: 14px; font-weight: bold; color: #e0e0e0; "
    "background: #1e1e1e; border: 1px solid #555; border-radius: 4px; padding: 8px; } "
    "QPushButton:hover { background: #2a2a2a; border: 1px solid #777; } "
    "QPushButton:pressed { background: #333; } "
    "QPushButton:disabled { color: #666; border: 1px solid #3a3a3a; }"
)
_ABORT_BUTTON_STYLE = (
    "QPushButton { font-size: 14px; font-weight: bold; color: #e0e0e0; "
    "background: #5a1f1f; border: 1px solid #7a1f1f; border-radius: 4px; padding: 8px; } "
    "QPushButton:hover { background: #6e2626; } "
    "QPushButton:pressed { background: #4a1919; } "
    "QPushButton:disabled { color: #666; background: #1e1e1e; border: 1px solid #3a3a3a; }"
)
_MESSAGE_BOX_STYLE = (
    "color: #ccc; font-size: 12px; background: #161616; "
    "border: 1px solid #2a2a2a; border-radius: 4px; padding: 4px;"
)
_ARRIVED_BANNER_STYLE = (
    "color: #ffffff; font-size: 22px; font-weight: bold; background: #1b8a3a; "
    "border: 2px solid #3ba33b; border-radius: 6px; padding: 10px;"
)


class AutonomousNavWidget(QWidget):

    waypoint_added = pyqtSignal(str, float, float, str, str)    # (waypoint_id, lat, lon, label, waypoint_type)
    launch_requested = pyqtSignal(str, float, float, str, str)  # (waypoint_id, lat, lon, label, waypoint_type)
    stop_requested = pyqtSignal(str)                            # (waypoint_id)

    def __init__(self, checklist_path=None, store=None, parent=None):
        super().__init__(parent)
        self._store = store or AutonomousNavStore()
        self._active_waypoint_id = None  # the one in-flight navigation attempt, if any
        self._status = "IDLE"
        self._list_items = {}  # waypoint_id -> QListWidgetItem

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(8)

        self.checklist = ChecklistWidget(checklist_path or _DEFAULT_CHECKLIST_PATH)
        layout.addWidget(self.checklist, 1)

        right_column = QVBoxLayout()
        right_column.setSpacing(8)
        right_column.addWidget(self._build_entry_form())
        right_column.addWidget(self._build_status_card())
        right_column.addWidget(self._build_waypoint_list())
        layout.addLayout(right_column, 1)

        self._refresh_form()

    def bind_data_source(self, data_source):
        data_source.signals.autonomous_nav_status.connect(self._on_autonomous_nav_status)

    # -- construction -------------------------------------------------------

    def _build_entry_form(self) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet(_ENTRY_STYLE)
        form_layout = QVBoxLayout(frame)

        title = QLabel("GNSS Waypoint")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        form_layout.addWidget(title)

        self._label_edit = QLineEdit()
        self._label_edit.setPlaceholderText("Label (e.g. \"GNSS Point 1\", \"Post A\")")
        self._label_edit.textChanged.connect(self._refresh_form)
        form_layout.addWidget(self._label_edit)

        self._type_combo = QComboBox()
        for display, _value in _WAYPOINT_TYPES:
            self._type_combo.addItem(display)
        form_layout.addWidget(self._type_combo)

        coord_row = QHBoxLayout()
        self._lat_spin = QDoubleSpinBox()
        self._lat_spin.setRange(-90.0, 90.0)
        self._lat_spin.setDecimals(6)
        self._lat_spin.setPrefix("lat ")
        self._lon_spin = QDoubleSpinBox()
        self._lon_spin.setRange(-180.0, 180.0)
        self._lon_spin.setDecimals(6)
        self._lon_spin.setPrefix("lon ")
        coord_row.addWidget(self._lat_spin)
        coord_row.addWidget(self._lon_spin)
        form_layout.addLayout(coord_row)

        self._send_button = QPushButton("Send Waypoint && Launch")
        self._send_button.setStyleSheet(_BUTTON_STYLE)
        self._send_button.clicked.connect(self._on_send_clicked)
        form_layout.addWidget(self._send_button)

        return frame

    def _build_status_card(self) -> QFrame:
        frame = QFrame()
        form_layout = QVBoxLayout(frame)

        self._status_label = ColorCodedLabel()
        form_layout.addWidget(self._status_label)

        self._message_label = QLabel()
        self._message_label.setWordWrap(True)
        self._message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._message_label.setFixedHeight(44)
        self._message_label.setStyleSheet(_MESSAGE_BOX_STYLE)
        form_layout.addWidget(self._message_label)

        self._abort_button = QPushButton("Abort")
        self._abort_button.setStyleSheet(_ABORT_BUTTON_STYLE)
        self._abort_button.clicked.connect(self._on_abort_clicked)
        form_layout.addWidget(self._abort_button)

        self._refresh_status_display()
        return frame

    def _build_waypoint_list(self) -> QFrame:
        frame = QFrame()
        layout = QVBoxLayout(frame)

        title = QLabel("Waypoints Sent")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)

        self._waypoint_list = QListWidget()
        layout.addWidget(self._waypoint_list)

        return frame

    # -- public API, called by MainWindow ------------------------------------

    def set_status(self, waypoint_id: str, status: str, message: str = ""):
        if waypoint_id != self._active_waypoint_id:
            return
        self._status = status
        self._refresh_status_display(message)
        self._refresh_form()
        self._update_list_item(waypoint_id, status)
        if status == "STOPPED":
            self._active_waypoint_id = None

    # -- internal -------------------------------------------------------

    def _on_autonomous_nav_status(self, waypoint_id: str, status: str, message: str):
        self._store.record_status(waypoint_id, status, message)
        self.set_status(waypoint_id, status, message)

    def _on_send_clicked(self):
        label = self._label_edit.text().strip()
        if not label or self._active_waypoint_id is not None:
            return
        waypoint_type = _WAYPOINT_TYPES[self._type_combo.currentIndex()][1]
        lat = self._lat_spin.value()
        lon = self._lon_spin.value()

        waypoint = self._store.add_waypoint(label, waypoint_type, lat, lon)
        waypoint_id = waypoint["id"]
        self._active_waypoint_id = waypoint_id

        self._add_list_item(waypoint_id, label, waypoint_type, lat, lon)
        self.waypoint_added.emit(waypoint_id, lat, lon, label, waypoint_type)
        self.launch_requested.emit(waypoint_id, lat, lon, label, waypoint_type)

        self._label_edit.clear()
        self._status = "STARTING"
        self._refresh_status_display("")
        self._refresh_form()

    def _on_abort_clicked(self):
        if self._active_waypoint_id is not None:
            self.stop_requested.emit(self._active_waypoint_id)

    def _refresh_form(self):
        has_label = bool(self._label_edit.text().strip())
        idle = self._active_waypoint_id is None
        self._send_button.setEnabled(has_label and idle)
        self._abort_button.setEnabled(not idle and self._status in _RUNNING_LIKE_STATUSES)

    def _refresh_status_display(self, message: str = ""):
        color = _STATUS_COLORS.get(self._status, _STATUS_COLORS["IDLE"])
        self._status_label.set_state(self._status, color)

        if self._status == "ARRIVED":
            # Large, high-contrast banner -- the mission rules require
            # "a large and obvious message... for the C2 station judge
            # to observe" on arrival, which the small message box the
            # other statuses use wouldn't satisfy.
            self._message_label.setFixedHeight(64)
            self._message_label.setStyleSheet(_ARRIVED_BANNER_STYLE)
            self._message_label.setText(message or "ARRIVED AT TARGET")
        else:
            self._message_label.setFixedHeight(44)
            self._message_label.setStyleSheet(_MESSAGE_BOX_STYLE)
            self._message_label.setText(message)

    def _add_list_item(self, waypoint_id: str, label: str, waypoint_type: str, lat: float, lon: float):
        type_display = _TYPE_DISPLAY_BY_VALUE.get(waypoint_type, waypoint_type)
        item = QListWidgetItem(f"{label} ({type_display}) — {lat:.6f}, {lon:.6f} — STARTING")
        self._waypoint_list.addItem(item)
        self._list_items[waypoint_id] = (item, label, type_display, lat, lon)

    def _update_list_item(self, waypoint_id: str, status: str):
        entry = self._list_items.get(waypoint_id)
        if entry is None:
            return
        item, label, type_display, lat, lon = entry
        item.setText(f"{label} ({type_display}) — {lat:.6f}, {lon:.6f} — {status}")
