"""
Science Mission tab.

Composes the Science-mission-specific controls: the current-site label
(ScienceSiteBar) and the four rover-driven sequences (Spectrometer, NPK
probe, Panorama, Stratigraphic Photo), each a ScienceSequenceWidget.
NPK/Panorama/Stratigraphic Photo are still dashed placeholders here —
they get their own ScienceSequenceWidget instances in Steps 3-5, same
incremental-build approach as the rest of the tab (site tagging,
persistence, gating, review dialog) arriving in later steps.

This widget owns the "which sequence is this data for" dispatch:
DataSource.signals.science_* are multiplexed by a `sequence` tag (see
data_source.py), so bind_data_source() connects each once here and
routes to whichever ScienceSequenceWidget matches, via
self._sequence_widgets. Outbound launch_requested/stop_requested are
aggregated the same way in reverse — each sequence widget's signal is
re-emitted on this widget's own signal, which MainWindow connects to
DataSource.send_science_sequence_command (mirroring how
SubsystemLaunchWidget's signals get forwarded).

science_image's frame decode currently borrows CameraFeedWidget's
_frame_to_pixmap directly -- Step 6 extracts that into a shared
frame_decode module so this import goes away.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal

from widgets.science_site_bar import ScienceSiteBar
from widgets.science_sequence_widget import ScienceSequenceWidget
from widgets.camera_feed_widget import _frame_to_pixmap

_PLACEHOLDER_TITLES = ("Panorama", "Stratigraphic Photo")


def _placeholder_slot(title: str) -> QFrame:
    """Dashed-border stand-in for a not-yet-built ScienceSequenceWidget,
    same visual language as main_window.py's _placeholder_box so the
    tab doesn't look inconsistent with the other still-placeholder
    tabs while this one is under construction."""
    frame = QFrame()
    frame.setFrameShape(QFrame.Shape.StyledPanel)
    frame.setMinimumHeight(160)
    frame.setStyleSheet(
        "QFrame { border: 1px dashed #3a3a3a; border-radius: 4px; background: #111; }"
    )

    label = QLabel(f"{title}\n(not yet implemented)")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet("color: #666; font-size: 11px; border: none;")
    label.setWordWrap(True)

    layout = QVBoxLayout(frame)
    layout.addWidget(label)
    return frame


class ScienceTabWidget(QWidget):

    launch_requested = pyqtSignal(str, bool)  # (sequence, collect_to_cache)
    stop_requested = pyqtSignal(str)          # (sequence)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._data_source = None
        self._sequence_widgets = {}  # sequence -> ScienceSequenceWidget, filled in as each is built

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(8)

        self.site_bar = ScienceSiteBar()
        layout.addWidget(self.site_bar)

        sequences_row = QHBoxLayout()
        sequences_row.setSpacing(8)

        spectrometer = ScienceSequenceWidget(
            sequence="SPECTROMETER", title="Spectrometer", stoppable=True,
            has_cache_flag=True, show_gnss=True, show_image=True, show_reading=True,
        )
        self._register_sequence_widget(spectrometer)
        sequences_row.addWidget(spectrometer)

        npk = ScienceSequenceWidget(
            sequence="NPK", title="NPK Probe", stoppable=True,
            reading_fields=[
                ("nitrogen_ppm", "N (ppm)"),
                ("phosphorus_ppm", "P (ppm)"),
                ("potassium_ppm", "K (ppm)"),
            ],
        )
        self._register_sequence_widget(npk)
        sequences_row.addWidget(npk)

        for title in _PLACEHOLDER_TITLES:
            sequences_row.addWidget(_placeholder_slot(title))

        layout.addLayout(sequences_row, 1)

        self.review_button = QPushButton("Review Sites...")
        self.review_button.setEnabled(False)  # wired in Step 10
        layout.addWidget(self.review_button)

    def bind_data_source(self, data_source):
        self._data_source = data_source
        data_source.signals.science_sequence_status.connect(self._on_science_status)
        data_source.signals.science_gnss_fix.connect(self._on_science_gnss)
        data_source.signals.science_image.connect(self._on_science_image)
        data_source.signals.science_reading.connect(self._on_science_reading)

    # -- internal ---------------------------------------------------------

    def _register_sequence_widget(self, widget: ScienceSequenceWidget):
        self._sequence_widgets[widget.sequence] = widget
        widget.launch_requested.connect(self.launch_requested)
        widget.stop_requested.connect(self.stop_requested)

    def _on_science_status(self, sequence: str, status: str, message: str):
        widget = self._sequence_widgets.get(sequence)
        if widget is not None:
            widget.set_status(sequence, status, message)

    def _on_science_gnss(self, sequence: str, lat: float, lon: float):
        widget = self._sequence_widgets.get(sequence)
        if widget is not None:
            widget.set_gnss(lat, lon)

    def _on_science_image(self, sequence: str, frame, frame_bytes: int, timestamp: float):
        widget = self._sequence_widgets.get(sequence)
        if widget is not None:
            widget.set_image(_frame_to_pixmap(frame))

    def _on_science_reading(self, sequence: str, reading: dict):
        widget = self._sequence_widgets.get(sequence)
        if widget is not None:
            widget.set_reading(reading)
