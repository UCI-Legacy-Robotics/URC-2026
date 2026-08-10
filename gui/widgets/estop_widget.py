"""
E-Stop widget — sidebar, bottom row. The most safety-critical widget in
the app.

estop_requested (GUI -> rover) and its confirmation
(DataSource.signals.estop_confirmed, rover -> GUI) are DISTINCT events —
never collapse them. Pressing the button only *requests* an E-Stop; the
UI never claims the rover is stopped until confirmation says so. If
confirmation doesn't arrive within a timeout, that's flagged explicitly
("NO CONFIRMATION RECEIVED") rather than left ambiguous — an operator
assuming the rover stopped when it didn't is a safety hazard, so silence
is never treated as success here.

Distinct from the Software Enable/Disable toggle (software_enable_widget.py):
E-Stop is a hardware-equivalent kill of power/comms, and is
one-directional from the GUI's side — there's no "un-estop" request here,
only detecting a hardware reset if the rover reports
estop_confirmed(False).
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QTimer, pyqtSignal

from widgets.color_coded_label import ColorCodedLabel

_COLOR_READY = "#1a0a0a"
_COLOR_PENDING = "#8a6d1a"
_COLOR_CONFIRMED = "#d32f2f"
_COLOR_NO_CONFIRMATION = "#e65100"

# Placeholder — real threshold TBD with systems/electrical.
_NO_CONFIRMATION_TIMEOUT_MS = 3000


class EstopWidget(QWidget):

    estop_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pending = False
        self._confirmed = False
        self._timed_out = False

        self._timeout_timer = QTimer(self)
        self._timeout_timer.setSingleShot(True)
        self._timeout_timer.setInterval(_NO_CONFIRMATION_TIMEOUT_MS)
        self._timeout_timer.timeout.connect(self._on_no_confirmation_timeout)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)

        title_label = QLabel("E-STOP")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #888; font-size: 10px;")
        layout.addWidget(title_label)

        self._status_label = ColorCodedLabel()
        layout.addWidget(self._status_label)

        self._button = QPushButton("E-STOP")
        self._button.setMinimumHeight(48)
        self._button.setStyleSheet(
            "QPushButton { font-weight: bold; font-size: 16px; } "
            "QPushButton:enabled { border: 2px solid #ff4a4a; }"
        )
        self._button.clicked.connect(self._on_button_clicked)
        layout.addWidget(self._button)

        self._refresh()

    # -- public API, called by MainWindow --------------------------------

    def set_confirmed(self, confirmed: bool):
        """Wire to DataSource.signals.estop_confirmed."""
        self._timeout_timer.stop()
        self._pending = False
        self._timed_out = False
        self._confirmed = confirmed
        self._refresh()

    # -- internal -----------------------------------------------------

    def _on_button_clicked(self):
        self._pending = True
        self._timed_out = False
        self._timeout_timer.start()
        self._refresh()
        self.estop_requested.emit()

    def _on_no_confirmation_timeout(self):
        if self._pending and not self._confirmed:
            self._timed_out = True
            self._refresh()

    def _refresh(self):
        if self._confirmed:
            text, color, enabled = "E-STOPPED", _COLOR_CONFIRMED, False
        elif self._timed_out:
            text, color, enabled = "NO CONFIRMATION RECEIVED", _COLOR_NO_CONFIRMATION, True
        elif self._pending:
            text, color, enabled = "Requesting...", _COLOR_PENDING, False
        else:
            text, color, enabled = "READY", _COLOR_READY, True

        self._status_label.set_state(text, color)
        self._button.setEnabled(enabled)
