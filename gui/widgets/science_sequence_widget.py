"""
Science Sequence widget.

One instance per Science Mission sequence (Spectrometer, NPK Probe,
Panorama, Stratigraphic Photo) — generic over which sequence it is
and what data it displays, the same "one widget class, configured per
instance" pattern CameraFeedWidget uses for CameraID. Status/button
behavior mirrors SubsystemLaunchWidget's launch/stop-with-pending-
confirmation pattern: launch/stop only emit *_requested, the button
never flips state on its own — only a status update round-tripping
back through DataSource.signals.science_sequence_status confirms it.

Start-only sequences (Panorama, Stratigraphic Photo; stoppable=False)
have no operator-initiated abort — once launched the button stays
disabled until the rover reports STOPPED/ERROR on its own.

set_blocked() is a second, independent reason a launch can be refused
(no site set yet, or -- for Panorama -- the science payload currently
lowered by another sequence) layered on top of whatever the status-
derived enablement would otherwise allow.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal

from widgets.mode_badge_widget import ModeBadgeWidget
from widgets.color_coded_label import ColorCodedLabel

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

# Fixed-height text boxes for status message / GNSS / reading -- height is
# hardcoded rather than derived from QLabel.fontMetrics() (which doesn't
# reflect a stylesheet's font-size until the widget has been polished/
# shown, so it can't be trusted at construction time). The point of a
# fixed height is that a widget updating its own displayed text (a longer
# status message, a new reading) never grows/shrinks the card and shifts
# the rest of the dashboard around it.
_MESSAGE_BOX_HEIGHT = 44   # 2 rows at 12px
_DATA_BOX_HEIGHT = 56      # up to 2 rows at 18px
_DATA_BOX_FONT_SIZE = 18

# Thumbnail size the image slot is fixed to, 4:3 to match the science
# payload camera's frame aspect (see _CAMERA_FRAME_WIDTH/HEIGHT in
# simulation_data_source.py) -- deliberately small/fixed rather than
# stretching to fill the card, so it doesn't dominate the layout.
_IMAGE_THUMB_WIDTH = 400
_IMAGE_THUMB_HEIGHT = 300


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


class ScienceSequenceWidget(QWidget):

    launch_requested = pyqtSignal(str, bool)  # (sequence, collect_to_cache)
    stop_requested = pyqtSignal(str)          # (sequence)

    def __init__(self, sequence: str, title: str, stoppable: bool,
                 has_cache_flag: bool = False, show_gnss: bool = False,
                 show_image: bool = False, show_reading: bool = False,
                 reading_fields: list[tuple[str, str]] | None = None,
                 parent=None):
        super().__init__(parent)
        self.sequence = sequence
        self._stoppable = stoppable
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

        if has_cache_flag:
            self._cache_checkbox = QCheckBox("Collect to cache")
            layout.addWidget(self._cache_checkbox)
        else:
            self._cache_checkbox = None

        self._launch_button = QPushButton()
        self._launch_button.clicked.connect(self._on_button_clicked)
        layout.addWidget(self._launch_button)

        self._gnss_label = None
        if show_gnss:
            self._gnss_label = _fixed_text_box(_DATA_BOX_HEIGHT, font_size=_DATA_BOX_FONT_SIZE)
            self._gnss_label.setText("GNSS: --")
            layout.addWidget(self._gnss_label)

        self._image_label = None
        if show_image:
            self._image_label = QLabel()
            self._image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._image_label.setFixedSize(_IMAGE_THUMB_WIDTH, _IMAGE_THUMB_HEIGHT)
            self._image_label.setStyleSheet("background: #000; border: 1px solid #2a2a2a;")
            layout.addWidget(self._image_label, 0, Qt.AlignmentFlag.AlignHCenter)

        # reading_fields (e.g. NPK's nitrogen/phosphorus/potassium) splits
        # the reading into one fixed box per element, laid out in a row,
        # instead of a single box with every key crammed into one line --
        # readable per-element rather than a single show_reading box
        # (Spectrometer's peak-wavelength/absorbance pair, still one box).
        self._reading_label = None
        self._reading_boxes = None
        if reading_fields:
            self._reading_boxes = {}
            reading_column = QVBoxLayout()
            reading_column.setSpacing(4)
            for key, field_label in reading_fields:
                box = _fixed_text_box(_DATA_BOX_HEIGHT, font_size=_DATA_BOX_FONT_SIZE)
                box.setText(f"{field_label}\n--")
                self._reading_boxes[key] = (box, field_label)
                reading_column.addWidget(box)
            layout.addLayout(reading_column)
        elif show_reading:
            self._reading_label = _fixed_text_box(_DATA_BOX_HEIGHT, font_size=_DATA_BOX_FONT_SIZE)
            self._reading_label.setText("No reading yet")
            layout.addWidget(self._reading_label)

        layout.addStretch()

        self._refresh_status_label()
        self._refresh_button()

    # -- public API, called by ScienceTabWidget --------------------------

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

    def set_image(self, pixmap):
        if self._image_label is not None:
            self._image_label.setPixmap(
                pixmap.scaled(
                    _IMAGE_THUMB_WIDTH, _IMAGE_THUMB_HEIGHT,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

    def set_reading(self, reading: dict):
        if self._reading_boxes is not None:
            for key, (box, field_label) in self._reading_boxes.items():
                if key in reading:
                    box.setText(f"{field_label}\n{reading[key]}")
        elif self._reading_label is not None:
            self._reading_label.setText(
                "  ".join(f"{k}: {v}" for k, v in reading.items())
            )

    # -- internal ---------------------------------------------------------

    def _on_button_clicked(self):
        if self._stoppable and self._status in _RUNNING_LIKE_STATUSES:
            self.stop_requested.emit(self.sequence)
        else:
            collect_to_cache = self._cache_checkbox.isChecked() if self._cache_checkbox else False
            self.launch_requested.emit(self.sequence, collect_to_cache)

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

        if self._stoppable:
            self._launch_button.setEnabled(self._status != "STOPPING")
            if self._status == "STOPPING":
                self._launch_button.setText("Stopping...")
            elif self._status in _RUNNING_LIKE_STATUSES:
                self._launch_button.setText("Stop")
            else:
                self._launch_button.setText("Launch")
        else:
            running = self._status in _RUNNING_LIKE_STATUSES or self._status == "STOPPING"
            self._launch_button.setEnabled(not running)
            self._launch_button.setText("Running..." if running else "Launch")
