"""
Manual camera MUX control panel — lives on the second monitor, above
the fixed 2x2 camera grid (not on the primary window — space
constraints there, see handoff Step 4).

4 independent toggles, one per camera (see CameraID in data_source.py).
Manual only: no mission-state ties, no auto-enable/disable — same
philosophy as the Diagnostics tab decoupling (main_window.py). Toggling
emits camera_toggle_requested; the owning window (Step 5) is what
actually calls DataSource.enable_camera()/disable_camera() and updates
the matching CameraFeedWidget in the grid — the same emit-a-request /
window-drives-the-DataSource pattern every other outbound-command
widget in this GUI already follows (SoftwareEnableWidget,
SubsystemLaunchWidget, EstopWidget).

Each row tracks its own state/rate via CameraFeedTracker (shared with
CameraFeedWidget) so the panel's displayed state genuinely mirrors the
grid tile's rather than being a second independent guess.
"""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QGridLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from data_source import CAMERA_LABELS, CameraID
from widgets.camera_feed_tracker import CameraFeedTracker

_STATE_COLORS = {
    "ON": "#3ba33b",
    "OFF": "#888888",
    "NO SIGNAL": "#c0392b",
}


class _CameraMuxRow(QWidget):
    """One camera's label + toggle + mirrored state/rate. Private to
    this module — CameraMuxPanel owns the set of rows."""

    toggle_requested = pyqtSignal(str, bool)  # (camera_id, requested_enabled)

    def __init__(self, camera_id: str, label: str, parent=None):
        super().__init__(parent)
        self.camera_id = camera_id

        self.tracker = CameraFeedTracker(camera_id, parent=self)
        self.tracker.changed.connect(self._render)

        layout = QGridLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(8)

        self._label = QLabel(label)
        self._label.setStyleSheet("font-size: 12px;")
        self._state_label = QLabel()
        self._state_label.setStyleSheet("font-size: 12px; font-family: monospace;")
        self._rate_label = QLabel()
        self._rate_label.setStyleSheet("font-size: 12px; font-family: monospace; color: #999;")
        self._button = QPushButton()
        self._button.setFixedWidth(90)
        self._button.clicked.connect(self._on_button_clicked)

        layout.addWidget(self._label, 0, 0)
        layout.addWidget(self._state_label, 0, 1)
        layout.addWidget(self._rate_label, 0, 2)
        layout.addWidget(self._button, 0, 3)
        layout.setColumnStretch(0, 1)

        self._render()

    def bind_data_source(self, data_source):
        self.tracker.bind_data_source(data_source)

    def set_enabled(self, enabled: bool):
        """Call after the window has actually enabled/disabled this
        camera on the DataSource, so this row's displayed state
        reflects the confirmed toggle, not just the click."""
        self.tracker.set_enabled(enabled)

    def _on_button_clicked(self):
        target = not self.tracker.is_enabled()
        self.toggle_requested.emit(self.camera_id, target)

    def _render(self):
        state = self.tracker.current_state()
        rate = self.tracker.current_rate_mbps()

        self._state_label.setText(state)
        self._state_label.setStyleSheet(
            f"font-size: 12px; font-family: monospace; color: {_STATE_COLORS[state]};"
        )
        self._rate_label.setText(f"{rate:.2f} Mbps")
        self._button.setText("Disable" if self.tracker.is_enabled() else "Enable")


class CameraMuxPanel(QWidget):
    """4 independent camera toggles — manual only, see module docstring."""

    camera_toggle_requested = pyqtSignal(str, bool)  # (camera_id, requested_enabled)

    def __init__(self, parent=None):
        super().__init__(parent)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(6, 6, 6, 6)
        outer.setSpacing(4)

        title = QLabel("CAMERA MUX")
        title.setStyleSheet("color: #888; font-size: 10px; font-weight: bold;")
        outer.addWidget(title)

        self._rows = {}
        for camera in CameraID:
            row = _CameraMuxRow(camera.value, CAMERA_LABELS[camera.value])
            row.toggle_requested.connect(self.camera_toggle_requested.emit)
            outer.addWidget(row)
            self._rows[camera.value] = row

    # -- public API, called by the second-monitor window (Step 5) -------

    def bind_data_source(self, data_source):
        for row in self._rows.values():
            row.bind_data_source(data_source)

    def set_camera_enabled(self, camera_id: str, enabled: bool):
        """Call after the window has actually toggled this camera on
        the DataSource — see _CameraMuxRow.set_enabled()."""
        self._rows[camera_id].set_enabled(enabled)
