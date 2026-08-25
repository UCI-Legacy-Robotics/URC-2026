"""
Single camera-slot widget for the second-monitor camera MUX window.

One instance per camera (see CameraID in data_source.py) — shows the
decoded video frame while its camera is enabled and healthy, a fixed
"NO SIGNAL" placeholder otherwise, and a status strip in the chrome
above the video image (never overlaid on it) with the camera label,
state, and current data rate. The video area itself is locked to a
16:9 box (letterboxed within whatever space the grid gives this
widget) rather than stretching arbitrarily to fill the grid cell.

State/rate tracking lives in CameraFeedTracker (shared with the MUX
panel's per-camera row); this widget only turns that into pixels.
Whoever toggles a camera (the MUX panel, Step 4) is responsible for
calling set_enabled() here in the same action as calling
enable_camera()/disable_camera() on the DataSource — see
camera_feed_tracker.py for why that can't be inferred from the
DataSource alone.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from frame_decode import decode_frame_to_rgb
from widgets.camera_feed_tracker import CameraFeedTracker

_STATE_COLORS = {
    "ON": "#3ba33b",
    "OFF": "#888888",
    "NO SIGNAL": "#c0392b",
    "LOCKED": "#666666",
}

# Video area is locked to this aspect ratio (16:9 — a typical camera/
# screen ratio, e.g. 1920x1080), letterboxed within whatever space the
# grid cell gives this widget.
_VIDEO_ASPECT_W = 16
_VIDEO_ASPECT_H = 9


def _frame_to_pixmap(frame) -> QPixmap:
    """Decode a normalized camera_frame payload (SimpleNamespace with
    encoding/data/height/width — see DataSourceSignals.camera_frame in
    data_source.py) into a QPixmap."""
    rgb = decode_frame_to_rgb(frame)
    h, w, _ = rgb.shape
    qt_image = QImage(rgb.data, w, h, rgb.strides[0], QImage.Format.Format_RGB888)
    return QPixmap.fromImage(qt_image)


class CameraFeedWidget(QWidget):

    def __init__(self, camera_id: str, label: str, parent=None):
        super().__init__(parent)
        self.camera_id = camera_id
        self._label_text = label
        self._locked = False

        self.tracker = CameraFeedTracker(camera_id, parent=self)
        self.tracker.changed.connect(self._render)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet('CameraFeedWidget { background-color: #1a1a1a; border-radius: 6px; }')

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Status strip in the chrome, above the image — never overlaid
        # on the video itself (handoff Step 3).
        self._status_strip = QLabel()
        self._status_strip.setStyleSheet(
            'background: #0d0d0d; font-size: 15px; font-family: monospace; padding: 5px 8px;'
        )
        layout.addWidget(self._status_strip)

        self._video_label = QLabel()
        self._video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._video_label.setMinimumSize(160, 90)  # 16:9 floor, resizeEvent takes over once shown
        self._video_label.setStyleSheet(
            'background: transparent; color: #555; font-size: 13px; font-family: monospace;'
        )
        layout.addWidget(self._video_label, 1, Qt.AlignmentFlag.AlignCenter)

        self._render()

    def resizeEvent(self, event):
        # Lock the video area to a 16:9 box, letterboxed within
        # whatever space this widget currently has (a grid cell
        # is much wider than tall, and a plain landscape-filling label
        # ends up looking like a wide letterbox instead of a feed).
        avail_h = max(self.height() - self._status_strip.sizeHint().height(), 0)
        avail_w = self.width()

        target_w = avail_h * _VIDEO_ASPECT_W / _VIDEO_ASPECT_H
        if target_w <= avail_w:
            video_w, video_h = target_w, avail_h
        else:
            video_w = avail_w
            video_h = avail_w * _VIDEO_ASPECT_H / _VIDEO_ASPECT_W

        self._video_label.setFixedSize(max(int(video_w), 1), max(int(video_h), 1))
        super().resizeEvent(event)

    # -- public API -----------------------------------------------------

    def bind_data_source(self, data_source):
        self.tracker.bind_data_source(data_source)

    def set_enabled(self, enabled: bool):
        """Call whenever the MUX panel toggles this camera on/off — see
        module docstring for why this can't be inferred from the
        DataSource alone."""
        self.tracker.set_enabled(enabled)

    def set_locked(self, locked: bool):
        """Call whenever this camera's gating subsystem (Science/Arm)
        transitions to/from RUNNING — see CameraWindow. Locked is a
        display-only concept layered on top of OFF; it never affects
        the tracker itself, only whether OFF renders as "LOCKED"."""
        if locked == self._locked:
            return
        self._locked = locked
        self._render()

    # -- rendering --------------------------------------------------------

    def _render(self):
        state = self.tracker.current_state()
        frame = self.tracker.latest_frame()
        display_state = "LOCKED" if (self._locked and state == "OFF") else state

        if state == "ON" and frame is not None:
            try:
                pixmap = _frame_to_pixmap(frame).scaled(
                    self._video_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                self._video_label.setPixmap(pixmap)
            except Exception as e:
                self._video_label.setText(f'Decode error: {e}')
        else:
            # Same fixed placeholder text for OFF and NO SIGNAL — the
            # status strip below is what distinguishes the two. LOCKED
            # gets its own text so "why is this camera unavailable"
            # doesn't look identical to "should be on but isn't".
            self._video_label.setText("LOCKED" if display_state == "LOCKED" else "NO SIGNAL")

        rate = self.tracker.current_rate_mbps()
        fps = self.tracker.current_fps()
        self._status_strip.setText(
            f"{self._label_text}   {display_state}   {rate:.2f} Mbps   {fps:.1f} fps"
        )
        self._status_strip.setStyleSheet(
            'background: #0d0d0d; font-size: 15px; font-family: monospace; '
            f'padding: 5px 8px; color: {_STATE_COLORS[display_state]};'
        )
