"""
Mission State Machine widget — top-left of the top strip.

Owns the single MissionStateMachine instance for the app (MainWindow reads
`.state_machine` off this widget to wire tab locking, etc. — there is
exactly one mission in progress at a time, no reason for multiple owners).
Embeds MissionTimerWidget for the countdown: entering a mission state
auto-starts the timer at a per-mission default duration, but that default
is just a starting point in an editable spinbox — some missions have
judge-set/variable time limits in the field (see timer_widget.py), so the
duration is never hardcoded past that.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QSpinBox, QMessageBox
)
from PyQt6.QtCore import Qt

from state_machine import MissionState, MissionStateMachine, InvalidTransitionError
from widgets.timer_widget import MissionTimerWidget


# Sensible starting duration per mission, in seconds — operator-editable
# via the spinbox before/while a mission runs. Not authoritative time
# limits; those are judge-set/variable at the competition.
_DEFAULT_DURATIONS_SECONDS = {
    MissionState.SCIENCE: 25 * 60,
    MissionState.DELIVERY: 45 * 60,
    MissionState.EQUIPMENT_SERVICING: 30 * 60,
    MissionState.AUTONOMOUS_NAV: 30 * 60,
}

_STATE_LABELS = {
    MissionState.IDLE: "Idle",
    MissionState.DIAGNOSTICS: "Diagnostics",
    MissionState.SCIENCE: "Science",
    MissionState.DELIVERY: "Delivery",
    MissionState.EQUIPMENT_SERVICING: "Equipment Servicing",
    MissionState.AUTONOMOUS_NAV: "Autonomous Nav",
}


class MissionSmWidget(QWidget):
    """State label + timer + timer controls + next-state transition
    controls, all wired to a single owned MissionStateMachine."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.state_machine = MissionStateMachine()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(4)

        self._state_label = QLabel()
        self._state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._state_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self._state_label)

        self.timer_widget = MissionTimerWidget()
        layout.addWidget(self.timer_widget)

        duration_row = QHBoxLayout()
        duration_row.addWidget(QLabel("Duration:"))
        self._duration_spin = QSpinBox()
        self._duration_spin.setRange(1, 180)
        self._duration_spin.setSuffix(" min")
        self._duration_spin.setValue(25)
        duration_row.addWidget(self._duration_spin)
        layout.addLayout(duration_row)

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

        next_state_row = QHBoxLayout()
        self._next_state_combo = QComboBox()
        for state in MissionState:
            self._next_state_combo.addItem(_STATE_LABELS[state], state)
        self._confirm_button = QPushButton("Go")
        self._confirm_button.clicked.connect(self._on_confirm_transition)
        next_state_row.addWidget(self._next_state_combo)
        next_state_row.addWidget(self._confirm_button)
        layout.addLayout(next_state_row)

        self.state_machine.state_changed.connect(self._on_state_changed)
        self.state_machine.mission_started.connect(self._on_mission_started)

        self._refresh_state_label()

    # -- internal -----------------------------------------------------

    def _on_start_clicked(self):
        if self.timer_widget.remaining_seconds() > 0 and not self.timer_widget.is_running():
            self.timer_widget.resume()
        else:
            self.timer_widget.start(self._duration_spin.value() * 60)

    def _on_pause_clicked(self):
        self.timer_widget.pause()

    def _on_confirm_transition(self):
        to_state = self._next_state_combo.currentData()
        try:
            self.state_machine.transition_to(to_state)
        except InvalidTransitionError as exc:
            QMessageBox.warning(self, "Invalid transition", str(exc))

    def _on_state_changed(self, old_state, new_state):
        self._refresh_state_label()

    def _on_mission_started(self, mission_state):
        default_seconds = _DEFAULT_DURATIONS_SECONDS.get(mission_state, 30 * 60)
        self._duration_spin.setValue(default_seconds // 60)
        self.timer_widget.start(default_seconds)

    def _refresh_state_label(self):
        self._state_label.setText(_STATE_LABELS[self.state_machine.state])
