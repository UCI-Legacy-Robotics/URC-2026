"""
Equipment Servicing tab.

Composes the Equipment Servicing Mission's controls: the plain
completion checklist (ChecklistWidget, no scoring -- see
checklist_widget.py) for the manual/teleoperated sub-tasks (cache into the lander
drawer, the hinged panel latch, the fuel hose/cam-lock, the 1/4-turn
valve, buttons/switches/knobs), plus two launch/stop sequence cards for
the two sub-tasks that aren't a single checkbox:

  - Autonomous Typing: the rover autonomously types a pre-programmed
    3-6 letter launch key on a mounted keyboard. Same launch/stop/
    status round trip as a Science sequence (ScienceSequenceWidget),
    plus a text field to program the key before launch. Per the rules,
    operator intervention is allowed only to exit autonomous mode and
    abort/restart from the beginning -- that maps onto Stop, same as
    every other stoppable sequence; there's no separate "abort" verb.
  - USB Read: insert a USB-C cable connected to a memory card and read
    GNSS coordinates off a text file on it. Same launch/stop/status
    shape, with a GNSS readout instead of a key field.

Deliberately a new, self-contained sequence card (_EquipmentSequenceCard
below) rather than reusing ScienceSequenceWidget directly -- these two
sequences need a key-entry field ScienceSequenceWidget has no slot for,
and Equipment Servicing has none of Science's site-bar/store/payload-
lowered gating baggage to inherit. Same "each mission owns its widgets"
split as DeliveryChecklistWidget already being separate from Science's.

Gating: both sequence cards are blocked until the ARM subsystem (which
Equipment Servicing launches, same as Delivery -- see
_SUBSYSTEM_MODE_BY_MISSION_STATE in main_window.py) is confirmed
RUNNING, mirroring how ScienceTabWidget gates its sequences on the
SCIENCE subsystem. The checklist itself is not gated -- like Delivery,
it's just a running tally an operator ticks off by hand, not telemetry.
"""

from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
)
from PyQt6.QtGui import QValidator
from PyQt6.QtCore import Qt, pyqtSignal

from widgets.checklist_widget import ChecklistWidget
from widgets.mode_badge_widget import ModeBadgeWidget
from widgets.color_coded_label import ColorCodedLabel

_DEFAULT_CHECKLIST_PATH = Path(__file__).resolve().parent.parent / "equipment_servicing_checklist.json"

_STATUS_COLORS = {
    "IDLE": "#3a3a3a",
    "STARTING": "#8a6d1a",
    "RUNNING": "#1b5e20",
    "STOPPING": "#8a6d1a",
    "STOPPED": "#3a3a3a",
    "ERROR": "#7a1f1f",
}
_RUNNING_LIKE_STATUSES = ("STARTING", "RUNNING")
_SEQUENCE_BADGE_COLORS = {"ACTIVE": "#1b5e20"}

_MESSAGE_BOX_HEIGHT = 44
_DATA_BOX_HEIGHT = 40
_DATA_BOX_FONT_SIZE = 16

_MIN_KEY_LENGTH = 3
_MAX_KEY_LENGTH = 6

_KEY_INPUT_STYLE = (
    "QLineEdit { font-size: 18px; font-weight: bold; letter-spacing: 4px; "
    "color: #e0e0e0; background: #1a1a1a; border: 1px solid #555; "
    "border-radius: 4px; padding: 6px; } "
    "QLineEdit:focus { border: 1px solid #888; }"
)
_STEP_BUTTON_STYLE = (
    "QPushButton { font-size: 14px; font-weight: bold; color: #e0e0e0; "
    "background: #1e1e1e; border: 1px solid #555; border-radius: 4px; padding: 8px; } "
    "QPushButton:hover { background: #2a2a2a; border: 1px solid #777; } "
    "QPushButton:pressed { background: #333; } "
    "QPushButton:disabled { color: #666; border: 1px solid #3a3a3a; }"
)


def _fixed_text_box(height: int, font_size: int) -> QLabel:
    label = QLabel()
    label.setWordWrap(True)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setFixedHeight(height)
    label.setStyleSheet(
        f"color: #ccc; font-size: {font_size}px; background: #161616; "
        "border: 1px solid #2a2a2a; border-radius: 4px; padding: 2px;"
    )
    return label


class _LaunchKeyValidator(QValidator):
    """Uppercases as you type and rejects anything but letters -- the
    launch key is always alphabetic per the rules ("3-6 letter launch
    key"), so this catches a stray digit/symbol at entry time rather
    than letting the Launch button's length check be the only guard."""

    def validate(self, text: str, pos: int):
        upper = text.upper()
        if upper != text:
            return (QValidator.State.Intermediate, upper, pos)
        if text and not text.isalpha():
            return (QValidator.State.Invalid, text, pos)
        if len(text) > _MAX_KEY_LENGTH:
            return (QValidator.State.Invalid, text, pos)
        return (QValidator.State.Acceptable, text, pos)


class _EquipmentSequenceCard(QWidget):
    """One Equipment Servicing sequence (Autonomous Typing or USB Read)
    -- generic over which one it is, same "one widget class, configured
    per instance" shape ScienceSequenceWidget uses. launch_requested/
    stop_requested only request; only a status update round-tripping
    back through set_status() ever flips the button/label, same
    pending-confirmation pattern as SubsystemLaunchWidget."""

    launch_requested = pyqtSignal(str, str)  # (sequence, key -- "" if key_input wasn't given)
    stop_requested = pyqtSignal(str)         # (sequence)

    def __init__(self, sequence: str, title: str, key_input: bool = False,
                 show_gnss: bool = False, parent=None):
        super().__init__(parent)
        self.sequence = sequence
        self._status = "IDLE"
        self._blocked = False
        self._blocked_reason = ""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self._title_badge = ModeBadgeWidget(
            title=title.upper(), colors=_SEQUENCE_BADGE_COLORS, default_mode="ACTIVE"
        )
        layout.addWidget(self._title_badge)

        self._status_label = ColorCodedLabel()
        layout.addWidget(self._status_label)

        self._message_label = _fixed_text_box(_MESSAGE_BOX_HEIGHT, font_size=12)
        layout.addWidget(self._message_label)

        self._key_input = None
        if key_input:
            key_row = QHBoxLayout()
            key_label = QLabel("Launch key:")
            key_row.addWidget(key_label)
            self._key_input = QLineEdit()
            self._key_input.setPlaceholderText("3-6 letters")
            self._key_input.setMaxLength(_MAX_KEY_LENGTH)
            self._key_input.setValidator(_LaunchKeyValidator(self))
            self._key_input.setStyleSheet(_KEY_INPUT_STYLE)
            self._key_input.textChanged.connect(lambda _: self._refresh_button())
            key_row.addWidget(self._key_input, 1)
            layout.addLayout(key_row)

        self._launch_button = QPushButton()
        self._launch_button.setStyleSheet(_STEP_BUTTON_STYLE)
        self._launch_button.clicked.connect(self._on_button_clicked)
        layout.addWidget(self._launch_button)

        self._gnss_label = None
        if show_gnss:
            self._gnss_label = _fixed_text_box(_DATA_BOX_HEIGHT, font_size=_DATA_BOX_FONT_SIZE)
            self._gnss_label.setText("GNSS: --")
            layout.addWidget(self._gnss_label)

        layout.addStretch()

        self._refresh_status_label()
        self._refresh_button()

    # -- public API, called by EquipmentServicingWidget --------------------

    def set_status(self, sequence: str, status: str, message: str = ""):
        if sequence != self.sequence:
            return
        self._status = status
        self._refresh_status_label(message)
        self._refresh_button()

    def set_blocked(self, blocked: bool, reason: str = ""):
        self._blocked = blocked
        self._blocked_reason = reason
        self._refresh_button()

    def set_gnss(self, lat: float, lon: float):
        if self._gnss_label is not None:
            self._gnss_label.setText(f"GNSS: {lat:.6f}, {lon:.6f}")

    # -- internal -----------------------------------------------------------

    def _current_key(self) -> str:
        return self._key_input.text() if self._key_input is not None else ""

    def _on_button_clicked(self):
        if self._status in _RUNNING_LIKE_STATUSES:
            self.stop_requested.emit(self.sequence)
        else:
            self.launch_requested.emit(self.sequence, self._current_key())

    def _refresh_status_label(self, message: str = ""):
        color = _STATUS_COLORS.get(self._status, _STATUS_COLORS["IDLE"])
        self._status_label.set_state(self._status, color)
        self._message_label.setText(message)

    def _refresh_button(self):
        if self._blocked:
            self._launch_button.setEnabled(False)
            self._launch_button.setToolTip(self._blocked_reason)
            self._launch_button.setText("Blocked")
            return

        self._launch_button.setToolTip("")

        if self._status == "STOPPING":
            self._launch_button.setEnabled(False)
            self._launch_button.setText("Stopping...")
        elif self._status in _RUNNING_LIKE_STATUSES:
            self._launch_button.setEnabled(True)
            self._launch_button.setText("Stop")
        else:
            key_ready = self._key_input is None or len(self._current_key()) >= _MIN_KEY_LENGTH
            self._launch_button.setEnabled(key_ready)
            self._launch_button.setText("Launch")
            if self._key_input is not None and not key_ready:
                self._launch_button.setToolTip(f"Program a {_MIN_KEY_LENGTH}-{_MAX_KEY_LENGTH} letter launch key first")


class EquipmentServicingWidget(QWidget):

    launch_requested = pyqtSignal(str, str)  # (sequence, key -- "" if the sequence has none)
    stop_requested = pyqtSignal(str)         # (sequence)

    def __init__(self, checklist_path=None, parent=None):
        super().__init__(parent)
        self._data_source = None
        self._sequence_cards = {}
        self._mission_is_equipment_servicing = False
        self._arm_subsystem_running = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(8)

        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        self.checklist = ChecklistWidget(checklist_path or _DEFAULT_CHECKLIST_PATH)
        top_row.addWidget(self.checklist, 1)

        sequences_column = QVBoxLayout()
        sequences_column.setSpacing(8)

        launch_key_card = _EquipmentSequenceCard(
            sequence="LAUNCH_KEY", title="Autonomous Typing", key_input=True,
        )
        self._register_sequence_card(launch_key_card)
        sequences_column.addWidget(launch_key_card)

        usb_read_card = _EquipmentSequenceCard(
            sequence="USB_READ", title="USB Read", show_gnss=True,
        )
        self._register_sequence_card(usb_read_card)
        sequences_column.addWidget(usb_read_card)

        sequences_column.addStretch()
        top_row.addLayout(sequences_column, 1)

        layout.addLayout(top_row)

        self._refresh_gating()  # everything starts blocked -- no subsystem confirmation yet

    def bind_data_source(self, data_source):
        self._data_source = data_source
        data_source.signals.equipment_sequence_status.connect(self._on_equipment_status)
        data_source.signals.equipment_gnss_fix.connect(self._on_equipment_gnss)

    # -- public API, called by MainWindow ----------------------------------

    def set_mission_active(self, active: bool):
        """Mirrors ScienceTabWidget.set_subsystem_mode(), but takes
        whether THIS mission is the active one directly rather than the
        subsystem name -- Delivery also drives the ARM subsystem (see
        _SUBSYSTEM_MODE_BY_MISSION_STATE in main_window.py), so "ARM" on
        its own can't tell the two missions apart the way "SCIENCE"
        uniquely identifies Science for ScienceTabWidget. MainWindow
        passes new_state == MissionState.EQUIPMENT_SERVICING. Resetting
        the tracked RUNNING flag whenever this mission isn't active is
        what stops a stale confirmation from Delivery (or a previous
        Equipment Servicing run) from leaking into this tab's gating."""
        self._mission_is_equipment_servicing = active
        if not active:
            self._arm_subsystem_running = False
        self._refresh_gating()

    def set_equipment_subsystem_status(self, subsystem: str, status: str):
        """Wire to DataSource.signals.subsystem_status_update. Ignored
        for any subsystem but ARM."""
        if subsystem != "ARM":
            return
        self._arm_subsystem_running = (status == "RUNNING")
        self._refresh_gating()

    # -- internal ---------------------------------------------------------

    def _register_sequence_card(self, card: _EquipmentSequenceCard):
        self._sequence_cards[card.sequence] = card
        card.launch_requested.connect(self.launch_requested)
        card.stop_requested.connect(self.stop_requested)

    def _on_equipment_status(self, sequence: str, status: str, message: str):
        card = self._sequence_cards.get(sequence)
        if card is not None:
            card.set_status(sequence, status, message)

    def _on_equipment_gnss(self, sequence: str, lat: float, lon: float):
        card = self._sequence_cards.get(sequence)
        if card is not None:
            card.set_gnss(lat, lon)

    def _refresh_gating(self):
        ready = self._mission_is_equipment_servicing and self._arm_subsystem_running
        for card in self._sequence_cards.values():
            card.set_blocked(not ready, "" if ready else "ARM subsystem not launched")
