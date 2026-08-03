"""
Subsystem Launch widget

Shows which subsystem the current mission implies (Science / Arm / None
— MainWindow drives `set_mode()` automatically on mission changes, see
main_window.py), plus a status indicator (IDLE / STARTING / RUNNING /
ERROR) and a Launch/Stop toggle for that subsystem. There's nothing to
launch in "NONE" mode (Autonomous Nav, or no mission), so the button is
disabled there.

Real subsystem process management lives outside the GUI. Pressing
Launch/Stop only emits `launch_requested`/`stop_requested` — MainWindow
wires these to `DataSource.send_subsystem_command()`, which each
DataSource implementation logs or no-ops on (see data_source.py).
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal

from ui.mode_badge_widget import ModeBadgeWidget
from ui.color_coded_label import ColorCodedLabel

_MODE_COLORS = {
    "SCIENCE": "#1b5e20",
    "ARM": "#0d47a1",
    "NONE": "#3a3a3a",
}

_STATUS_COLORS = {
    "IDLE": "#3a3a3a",
    "STARTING": "#8a6d1a",
    "RUNNING": "#1b5e20",
    "ERROR": "#7a1f1f",
}

_RUNNING_LIKE_STATUSES = ("STARTING", "RUNNING")


class SubsystemLaunchWidget(QWidget):

    launch_requested = pyqtSignal(str)  # subsystem name
    stop_requested = pyqtSignal(str)    # subsystem name

    def __init__(self, parent=None):
        super().__init__(parent)
        self._mode = "NONE"
        self._status = "IDLE"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self._mode_badge = ModeBadgeWidget(
            title="SUBSYSTEM LAUNCH", colors=_MODE_COLORS, default_mode="NONE"
        )
        layout.addWidget(self._mode_badge)

        self._status_label = ColorCodedLabel()
        layout.addWidget(self._status_label)

        self._launch_button = QPushButton()
        self._launch_button.clicked.connect(self._on_button_clicked)
        layout.addWidget(self._launch_button)

        self._refresh_status_label()
        self._refresh_button()

    # -- public API, called by MainWindow --------------------------------

    def set_mode(self, mode: str):
        """mode: one of "SCIENCE", "ARM", "NONE"."""
        self._mode = mode
        self._mode_badge.set_mode(mode)
        self._status = "IDLE"
        self._refresh_status_label()
        self._refresh_button()

    def set_status(self, subsystem: str, status: str):
        """Wire to DataSource.signals.subsystem_status_update. Ignored if
        the update isn't for the currently-selected subsystem."""
        if subsystem != self._mode:
            return
        self._status = status
        self._refresh_status_label()
        self._refresh_button()

    # -- internal ---------------------------------------------------------

    def _on_button_clicked(self):
        if self._status in _RUNNING_LIKE_STATUSES:
            self.stop_requested.emit(self._mode)
        else:
            self.launch_requested.emit(self._mode)

    def _refresh_status_label(self):
        color = _STATUS_COLORS.get(self._status, _STATUS_COLORS["IDLE"])
        self._status_label.set_state(self._status, color)

    def _refresh_button(self):
        launchable = self._mode in ("SCIENCE", "ARM")
        self._launch_button.setEnabled(launchable)
        self._launch_button.setText(
            "Stop" if self._status in _RUNNING_LIKE_STATUSES else "Launch"
        )
