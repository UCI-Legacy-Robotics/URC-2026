"""
Mission State Machine widget

Owns the single MissionStateMachine instance for the app (MainWindow reads
`.state_machine` off this widget to wire tab locking, subsystem-launch
auto-selection, etc. — there is exactly one mission in progress at a
time, no reason for multiple owners).

Mission transitions are driven by a single "Next" button that walks a
fixed cycle (IDLE -> SCIENCE -> IDLE -> DELIVERY -> IDLE ->
EQUIPMENT_SERVICING -> IDLE -> AUTONOMOUS_NAV -> IDLE -> ...) rather than
a free-form dropdown, since that's the actual competition run order and
picking-then-confirming every time was pure friction. Diagnostics is not
part of this cycle at all — it's a plain always-available tab with no
ties to MissionStateMachine (see MainWindow's tab-lock exemption).

Embeds MissionTimerWidget for the countdown: entering a mission state
auto-starts the timer at a per-mission default duration (editable via the
"Set Durations..." dialog rather than inline, so the always-visible strip
doesn't grow a control per mission). Those defaults are just starting
points, never hardcoded past that — some missions have judge-set/variable
time limits in the field (see timer_widget.py). Leaving a mission back to
IDLE resets the timer, since a stale countdown from the last mission has
no meaning once you're no longer in it.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QSpinBox, QMessageBox, QDialog, QDialogButtonBox, QFormLayout
)

from state_machine import MissionState, MissionStateMachine, InvalidTransitionError
from widgets.timer_widget import MissionTimerWidget
from widgets.color_coded_label import ColorCodedLabel


# Sensible starting duration per mission, in seconds. Editable at runtime
# via the durations dialog; these are just the initial values, not
# authoritative time limits (those are judge-set/variable at the
# competition).
_DEFAULT_DURATIONS_SECONDS = {
    MissionState.SCIENCE: 25 * 60,
    MissionState.DELIVERY: 45 * 60,
    MissionState.EQUIPMENT_SERVICING: 30 * 60,
    MissionState.AUTONOMOUS_NAV: 30 * 60,
}

_STATE_LABELS = {
    MissionState.IDLE: "Idle",
    MissionState.SCIENCE: "Science",
    MissionState.DELIVERY: "Delivery",
    MissionState.EQUIPMENT_SERVICING: "Equipment Servicing",
    MissionState.AUTONOMOUS_NAV: "Autonomous Nav",
}

# Box color behind the state label, keyed by category rather than exact
# state — every mission state reads the same "in progress" green.
_COLOR_IDLE = "#3a3a3a"
_COLOR_MISSION = "#1b5e20"

# Fixed run-order cycle the "Next" button walks. IDLE reappears between
# every mission on purpose (matches MissionStateMachine's rule that
# missions can only return to IDLE, never jump to another mission
# directly) — the button always targets the next entry in this list and
# only advances its index after a successful transition, so a detour
# through Diagnostics (which starts and ends at IDLE) never desyncs it.
_MISSION_CYCLE = [
    MissionState.SCIENCE,
    MissionState.IDLE,
    MissionState.DELIVERY,
    MissionState.IDLE,
    MissionState.EQUIPMENT_SERVICING,
    MissionState.IDLE,
    MissionState.AUTONOMOUS_NAV,
    MissionState.IDLE,
]


class _DurationsDialog(QDialog):
    """Modal for editing per-mission default durations, in minutes."""

    _EDITABLE_STATES = (
        MissionState.SCIENCE,
        MissionState.DELIVERY,
        MissionState.EQUIPMENT_SERVICING,
        MissionState.AUTONOMOUS_NAV,
    )

    def __init__(self, current_durations_seconds: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mission Durations")

        layout = QFormLayout(self)

        self._spins = {}
        for state in self._EDITABLE_STATES:
            spin = QSpinBox()
            spin.setRange(1, 180)
            spin.setSuffix(" min")
            spin.setValue(current_durations_seconds[state] // 60)
            self._spins[state] = spin
            layout.addRow(f"{_STATE_LABELS[state]}:", spin)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def result_durations_seconds(self) -> dict:
        return {state: spin.value() * 60 for state, spin in self._spins.items()}


class MissionSmWidget(QWidget):
    """State label + timer + timer controls + mission-cycle controls,
    all wired to a single owned MissionStateMachine."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.state_machine = MissionStateMachine()
        self._durations = dict(_DEFAULT_DURATIONS_SECONDS)
        self._cycle_index = 0

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(4)

        self._state_label = ColorCodedLabel()
        layout.addWidget(self._state_label)

        self.timer_widget = MissionTimerWidget()
        layout.addWidget(self.timer_widget)

        timer_controls = QHBoxLayout()
        self._start_button = QPushButton("Start")
        self._pause_button = QPushButton("Pause")
        self._reset_button = QPushButton("Reset")
        self._start_button.clicked.connect(self._on_start_clicked)
        self._pause_button.clicked.connect(self._on_pause_clicked)
        self._reset_button.clicked.connect(self.timer_widget.reset)
        timer_controls.addWidget(self._start_button)
        timer_controls.addWidget(self._pause_button)
        timer_controls.addWidget(self._reset_button)
        layout.addLayout(timer_controls)

        self._durations_button = QPushButton("Set Durations...")
        self._durations_button.clicked.connect(self._on_edit_durations)
        layout.addWidget(self._durations_button)

        mission_controls = QHBoxLayout()
        self._next_button = QPushButton()
        # Fixed width so the row doesn't reflow every click — this button's
        # text changes length with the target state name ("Next: Science"
        # vs "Next: Equipment Servicing"), sized to fit the longest one.
        self._next_button.setFixedWidth(190)
        self._next_button.clicked.connect(self._on_next_clicked)
        self._mission_reset_button = QPushButton("Reset Mission")
        self._mission_reset_button.setFixedWidth(110)
        self._mission_reset_button.clicked.connect(self._on_mission_reset_clicked)
        mission_controls.addWidget(self._next_button)
        mission_controls.addWidget(self._mission_reset_button)
        layout.addLayout(mission_controls)

        self.state_machine.state_changed.connect(self._on_state_changed)
        self.state_machine.mission_started.connect(self._on_mission_started)
        self.state_machine.mission_ended.connect(self._on_mission_ended)

        self._refresh_state_label()
        self._update_controls()

    # -- internal -----------------------------------------------------

    def _on_start_clicked(self):
        if self.timer_widget.remaining_seconds() > 0 and not self.timer_widget.is_running():
            self.timer_widget.resume()
        elif self.state_machine.is_mission_active():
            self.timer_widget.start(self._durations.get(self.state_machine.state, 30 * 60))

    def _on_pause_clicked(self):
        self.timer_widget.pause()

    def _on_edit_durations(self):
        dialog = _DurationsDialog(self._durations, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._durations = dialog.result_durations_seconds()

    def _on_next_clicked(self):
        target = _MISSION_CYCLE[self._cycle_index]
        try:
            self.state_machine.transition_to(target)
        except InvalidTransitionError as exc:
            QMessageBox.warning(self, "Invalid transition", str(exc))
            return
        self._cycle_index = (self._cycle_index + 1) % len(_MISSION_CYCLE)
        self._update_controls()

    def _on_mission_reset_clicked(self):
        """Force back to IDLE and restart the mission cycle from the top
        (next click on "Next" goes to Science) — an abort/restart control,
        distinct from the timer's own Reset button above."""
        if self.state_machine.state != MissionState.IDLE:
            try:
                self.state_machine.transition_to(MissionState.IDLE)
            except InvalidTransitionError as exc:
                QMessageBox.warning(self, "Invalid transition", str(exc))
                return
        self._cycle_index = 0
        self.timer_widget.reset()
        self._update_controls()

    def _on_state_changed(self, old_state, new_state):
        self._refresh_state_label()
        self._update_controls()

    def _on_mission_started(self, mission_state):
        default_seconds = self._durations.get(mission_state, 30 * 60)
        self.timer_widget.start(default_seconds)

    def _on_mission_ended(self, ended_state):
        self.timer_widget.reset()

    def _refresh_state_label(self):
        state = self.state_machine.state
        bg = _COLOR_IDLE if state == MissionState.IDLE else _COLOR_MISSION
        self._state_label.set_state(_STATE_LABELS[state], bg)

    def _update_controls(self):
        next_target = _MISSION_CYCLE[self._cycle_index]
        self._next_button.setText(f"Next: {_STATE_LABELS[next_target]}")
