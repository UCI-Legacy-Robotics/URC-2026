"""
Non-visual per-camera state tracker: enabled/disabled, rolling data-rate
average, and the derived ON/OFF/NO SIGNAL state.

Shared by CameraFeedWidget (Step 3, the 2x2 grid tile) and the MUX
panel's per-camera row (Step 4) so the two displays can't disagree
about a camera's state or rate — the panel is required to "mirror" the
tile's state, so both derive it the same way rather than one copying
the other's number on a stale tick.
"""

from collections import deque

from PyQt6.QtCore import QObject, pyqtSignal

from stale_data import StaleDataWatcher

# Rolling window size for the Mbps average — starting point per the
# handoff, tune later.
_RATE_WINDOW_N = 30

# How long an enabled camera can go quiet before the tracker flags NO
# SIGNAL instead of ON — same class of issue as the usb_cam startup
# crash: a subscription can exist while the topic itself stays silent
# (bad cable, camera unpowered, wrong topic).
_NO_SIGNAL_TIMEOUT_MS = 2000


class CameraFeedTracker(QObject):
    """Tracks one camera's enabled state, latest frame, and rolling
    data rate. DataSource has no "is this camera enabled" query, so
    set_enabled() must be called by whoever toggles the camera (the
    MUX panel) — it can't be inferred from frame arrival alone."""

    changed = pyqtSignal()  # state, rate, or latest_frame changed — re-render

    def __init__(self, camera_id: str, parent=None):
        super().__init__(parent)
        self.camera_id = camera_id
        self._enabled = False
        self._latest_frame = None
        self._rate_samples = deque(maxlen=_RATE_WINDOW_N)  # (timestamp, frame_bytes)

        self._watcher = StaleDataWatcher(_NO_SIGNAL_TIMEOUT_MS, parent=self)
        self._watcher.became_stale.connect(self.changed.emit)
        self._watcher.became_fresh.connect(self.changed.emit)

    def bind_data_source(self, data_source):
        data_source.signals.camera_frame.connect(self._on_camera_frame)

    def is_enabled(self) -> bool:
        return self._enabled

    def set_enabled(self, enabled: bool):
        if enabled == self._enabled:
            return
        self._enabled = enabled
        self._latest_frame = None
        self._rate_samples.clear()
        self._watcher.stop()
        self.changed.emit()

    def latest_frame(self):
        return self._latest_frame

    def current_state(self) -> str:
        if not self._enabled:
            return "OFF"
        if self._watcher.is_stale() or not self._rate_samples:
            return "NO SIGNAL"
        return "ON"

    def current_rate_mbps(self) -> float:
        if len(self._rate_samples) < 2:
            return 0.0
        t_first, _ = self._rate_samples[0]
        t_last, _ = self._rate_samples[-1]
        elapsed = t_last - t_first
        if elapsed <= 0:
            return 0.0
        total_bits = sum(frame_bytes for _, frame_bytes in self._rate_samples) * 8
        return (total_bits / elapsed) / 1_000_000

    def current_fps(self) -> float:
        if len(self._rate_samples) < 2:
            return 0.0
        t_first, _ = self._rate_samples[0]
        t_last, _ = self._rate_samples[-1]
        elapsed = t_last - t_first
        if elapsed <= 0:
            return 0.0
        frame_intervals = len(self._rate_samples) - 1
        return frame_intervals / elapsed

    def _on_camera_frame(self, camera_id, frame, frame_bytes, timestamp):
        if camera_id != self.camera_id or not self._enabled:
            return
        self._watcher.notify()
        self._latest_frame = frame
        self._rate_samples.append((timestamp, frame_bytes))
        self.changed.emit()
