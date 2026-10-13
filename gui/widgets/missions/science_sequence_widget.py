"""
Science Sequence widget.

One instance per Science Mission sequence (Bradford/Cache, NPK Probe,
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

from PyQt6.QtWidgets import QVBoxLayout, QLabel, QButtonGroup
from PyQt6.QtCore import Qt, pyqtSignal
from qfluentwidgets import PushButton, RadioButton

from ui.theme import STATUS_COLORS as _STATUS_COLORS, RUNNING_LIKE_STATUSES as _RUNNING_LIKE_STATUSES
from widgets.shared.color_coded_label import ColorCodedLabel
from widgets.shared.controls import SectionCard, readout_box as _fixed_text_box, set_button

# Fixed-height text boxes for status message / GNSS / reading -- height is
# hardcoded rather than derived from QLabel.fontMetrics() (which doesn't
# reflect a stylesheet's font-size until the widget has been polished/
# shown, so it can't be trusted at construction time).
_MESSAGE_BOX_HEIGHT = 44   # 2 rows at 12px
_DATA_BOX_HEIGHT = 56      # up to 2 rows at 18px
_DATA_BOX_FONT_SIZE = 18

# Thumbnail size the image slot is fixed to, 4:3 to match the science
# payload camera's frame aspect (see _CAMERA_FRAME_WIDTH/HEIGHT in
# simulation_data_source.py) -- deliberately small/fixed rather than
# stretching to fill the card, so it doesn't dominate the layout.
_IMAGE_THUMB_WIDTH = 400
_IMAGE_THUMB_HEIGHT = 300


class ScienceSequenceWidget(SectionCard):

    launch_requested = pyqtSignal(str, str)  # (sequence, mode -- "" if launch_modes wasn't given)
    stop_requested = pyqtSignal(str)         # (sequence)

    def __init__(self, sequence: str, title: str, stoppable: bool,
                 icon_name: str = None,
                 launch_modes: list[tuple[str, str]] | None = None,
                 show_gnss: bool = False,
                 show_image: bool = False, show_reading: bool = False,
                 reading_fields: list[tuple[str, str]] | None = None,
                 parent=None):
        super().__init__(title, icon_name, parent)
        self.sequence = sequence
        self._stoppable = stoppable
        self._status = "IDLE"
        self._blocked = False
        self._blocked_reason = ""

        layout = self.body

        self._status_label = ColorCodedLabel()
        layout.addWidget(self._status_label)

        self._message_label = _fixed_text_box(_MESSAGE_BOX_HEIGHT, font_size=12)
        layout.addWidget(self._message_label)

        # launch_modes (e.g. Bradford/Cache's Cache-vs-Analyze choice) is a
        # radio group, not checkboxes -- these are mutually exclusive
        # site-exclusive resources (only one site's sample can occupy the
        # cache, and separately only one site's sample can go through the
        # spectrometer/vials), so a site picks exactly one, never both/
        # neither.
        self._mode_group = None
        self._mode_buttons = None
        if launch_modes:
            self._mode_buttons = {}
            self._mode_group = QButtonGroup(self)
            for i, (mode_key, mode_label) in enumerate(launch_modes):
                button = RadioButton(mode_label)
                if i == 0:
                    button.setChecked(True)
                self._mode_group.addButton(button)
                self._mode_buttons[mode_key] = button
                layout.addWidget(button)

        self._launch_button = PushButton()
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
            self._image_label.setStyleSheet(
                "background: #000; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 6px;"
            )
            layout.addWidget(self._image_label, 0, Qt.AlignmentFlag.AlignHCenter)

        # reading_fields (e.g. NPK's nitrogen/phosphorus/potassium) splits
        # the reading into one fixed box per element, laid out in a
        # column, instead of a single box with every key crammed into
        # one line -- readable per-element rather than a single
        # show_reading box (Bradford/Cache's peak-wavelength/absorbance
        # pair, still one box).
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
            mode = ""
            if self._mode_buttons:
                mode = next(
                    (key for key, button in self._mode_buttons.items() if button.isChecked()), ""
                )
            self.launch_requested.emit(self.sequence, mode)

    def _refresh_status_label(self, message: str = ""):
        color = _STATUS_COLORS.get(self._status, _STATUS_COLORS["IDLE"])
        self._status_label.set_state(self._status, color)
        self._message_label.setText(message)

    def _refresh_button(self):
        if self._blocked:
            self._launch_button.setEnabled(False)
            self._launch_button.setToolTip(self._blocked_reason)
            set_button(self._launch_button, "Blocked", "mdi6.lock")
            return

        self._launch_button.setToolTip("")

        if self._stoppable:
            self._launch_button.setEnabled(self._status != "STOPPING")
            if self._status == "STOPPING":
                set_button(self._launch_button, "Stopping...", "mdi6.dots-horizontal")
            elif self._status in _RUNNING_LIKE_STATUSES:
                set_button(self._launch_button, "Stop", "mdi6.stop")
            else:
                set_button(self._launch_button, "Launch", "mdi6.play")
        else:
            running = self._status in _RUNNING_LIKE_STATUSES or self._status == "STOPPING"
            self._launch_button.setEnabled(not running)
            if running:
                set_button(self._launch_button, "Running...", "mdi6.dots-horizontal")
            else:
                set_button(self._launch_button, "Launch", "mdi6.play")
