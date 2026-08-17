"""
Single camera-slot widget for the second-monitor camera MUX window.

One instance per camera (see CameraID in data_source.py) — shows the
decoded video frame while its camera is enabled and healthy, a fixed
"NO SIGNAL" placeholder otherwise, and a status strip in the chrome
(never overlaid on the video image) with the camera label, state, and
current data rate.

DataSource has no "is this camera currently enabled" query — only the
enable_camera()/disable_camera() commands — so this widget can't infer
its own on/off state from the backend. Whoever toggles a camera (the
MUX panel, Step 4) is responsible for calling set_enabled() here in
the same action as calling enable_camera()/disable_camera(), so the
widget's displayed state and the DataSource's actual subscription
state never drift apart.
"""

from collections import deque

import cv2
import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from stale_data import StaleDataWatcher

# Rolling window size for the Mbps average — starting point per the
# handoff, tune later.
_RATE_WINDOW_N = 30

# How long an enabled camera can go quiet before the widget flags NO
# SIGNAL instead of ON — same class of issue as the usb_cam startup
# crash: a subscription can exist while the topic itself stays silent
# (bad cable, camera unpowered, wrong topic).
_NO_SIGNAL_TIMEOUT_MS = 2000

_STATE_COLORS = {
    "ON": "#3ba33b",
    "OFF": "#888888",
    "NO SIGNAL": "#c0392b",
}


def _frame_to_pixmap(frame) -> QPixmap:
    """Decode a normalized camera_frame payload (SimpleNamespace with
    encoding/data/height/width — see DataSourceSignals.camera_frame in
    data_source.py) into a QPixmap. Manual numpy/cv2 decode, no
    cv_bridge (see handoff Step 0 — cv_bridge isn't used anywhere in
    the GUI process)."""
    enc = frame.encoding.lower()
    arr = np.frombuffer(frame.data, dtype=np.uint8)

    if enc in ('rgb8', 'rgb'):
        rgb = arr.reshape((frame.height, frame.width, 3))
    elif enc in ('bgr8', 'bgr'):
        rgb = cv2.cvtColor(arr.reshape((frame.height, frame.width, 3)), cv2.COLOR_BGR2RGB)
    elif enc in ('mono8', '8uc1'):
        rgb = cv2.cvtColor(arr.reshape((frame.height, frame.width)), cv2.COLOR_GRAY2RGB)
    elif enc in ('yuv422', 'yuv422_yuy2', 'yuyv'):
        rgb = cv2.cvtColor(arr.reshape((frame.height, frame.width, 2)), cv2.COLOR_YUV2RGB_YUYV)
    elif enc in ('mono16', '16uc1'):
        gray16 = arr.view(np.uint16).reshape((frame.height, frame.width))
        gray8 = (gray16 >> 8).astype(np.uint8)
        rgb = cv2.cvtColor(gray8, cv2.COLOR_GRAY2RGB)
    else:
        raise ValueError(f'Unsupported encoding: {frame.encoding}')

    rgb = np.ascontiguousarray(rgb)
    h, w, _ = rgb.shape
    qt_image = QImage(rgb.data, w, h, rgb.strides[0], QImage.Format.Format_RGB888)
    return QPixmap.fromImage(qt_image)


class CameraFeedWidget(QWidget):

    def __init__(self, camera_id: str, label: str, parent=None):
        super().__init__(parent)
        self.camera_id = camera_id
        self._label_text = label
        self._enabled = False
        self._rate_samples = deque(maxlen=_RATE_WINDOW_N)  # (timestamp, frame_bytes)

        self._watcher = StaleDataWatcher(_NO_SIGNAL_TIMEOUT_MS, parent=self)
        self._watcher.became_stale.connect(self._render)
        self._watcher.became_fresh.connect(self._render)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet('CameraFeedWidget { background-color: #1a1a1a; border-radius: 6px; }')

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._video_label = QLabel()
        self._video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._video_label.setMinimumSize(160, 120)
        self._video_label.setStyleSheet(
            'background: transparent; color: #555; font-size: 13px; font-family: monospace;'
        )
        layout.addWidget(self._video_label, 1)

        # Status strip in the chrome, below the image — never overlaid
        # on the video itself (handoff Step 3).
        self._status_strip = QLabel()
        self._status_strip.setStyleSheet(
            'background: #0d0d0d; font-size: 10px; font-family: monospace; padding: 3px 6px;'
        )
        layout.addWidget(self._status_strip)

        self._render()

    # -- public API -----------------------------------------------------

    def bind_data_source(self, data_source):
        data_source.signals.camera_frame.connect(self._on_camera_frame)

    def set_enabled(self, enabled: bool):
        """Call whenever the MUX panel toggles this camera on/off — see
        class docstring for why this can't be inferred from the
        DataSource alone."""
        if enabled == self._enabled:
            return
        self._enabled = enabled
        self._rate_samples.clear()
        self._watcher.stop()
        if not enabled:
            self._video_label.clear()
        self._render()

    # -- signal handling --------------------------------------------------

    def _on_camera_frame(self, camera_id, frame, frame_bytes, timestamp):
        if camera_id != self.camera_id or not self._enabled:
            return

        self._watcher.notify()
        self._rate_samples.append((timestamp, frame_bytes))

        try:
            pixmap = _frame_to_pixmap(frame).scaled(
                self._video_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self._video_label.setPixmap(pixmap)
        except Exception as e:
            self._video_label.setText(f'Decode error: {e}')

        self._render()

    # -- rendering --------------------------------------------------------

    def _current_state(self) -> str:
        if not self._enabled:
            return "OFF"
        if self._watcher.is_stale() or not self._rate_samples:
            return "NO SIGNAL"
        return "ON"

    def _current_rate_mbps(self) -> float:
        if len(self._rate_samples) < 2:
            return 0.0
        t_first, _ = self._rate_samples[0]
        t_last, _ = self._rate_samples[-1]
        elapsed = t_last - t_first
        if elapsed <= 0:
            return 0.0
        total_bits = sum(frame_bytes for _, frame_bytes in self._rate_samples) * 8
        return (total_bits / elapsed) / 1_000_000

    def _render(self):
        state = self._current_state()
        if state != "ON":
            # Same fixed placeholder text for OFF and NO SIGNAL — the
            # status strip below is what distinguishes the two.
            self._video_label.setText("NO SIGNAL")

        rate = self._current_rate_mbps()
        self._status_strip.setText(f"{self._label_text}   {state}   {rate:.2f} Mbps")
        self._status_strip.setStyleSheet(
            'background: #0d0d0d; font-size: 10px; font-family: monospace; '
            f'padding: 3px 6px; color: {_STATE_COLORS[state]};'
        )
