"""
Science Mission tab.

Composes the Science-mission-specific controls: the current-site label
(ScienceSiteBar) and the four rover-driven sequences (Spectrometer, NPK
probe, Panorama, Stratigraphic Photo), each a ScienceSequenceWidget.
Panorama's payload-lowered gating and the review dialog arrive in
later steps.

This widget owns the "which sequence is this data for" dispatch:
DataSource.signals.science_* are multiplexed by a `sequence` tag (see
data_source.py), so bind_data_source() connects each once here and
routes to whichever ScienceSequenceWidget matches, via
self._sequence_widgets. Outbound launch_requested/stop_requested are
aggregated the same way in reverse — each sequence widget's signal is
re-emitted on this widget's own signal, which MainWindow connects to
DataSource.send_science_sequence_command (mirroring how
SubsystemLaunchWidget's signals get forwarded).

Every dispatch handler also records the data into ScienceDataStore,
tagged with whatever site is current at the moment it arrives -- since
every sequence now requires a site to be set before it's launchable
(set_blocked() enforces that), the store's "Unsited" fallback bucket
should never actually be hit in practice, but stays as a safety net so
nothing is silently dropped if that assumption ever changes.

The site bar separately locks itself while Spectrometer or NPK is
running (STARTING/RUNNING/STOPPING) -- payload-lowered, not just
"site required" -- the same _PAYLOAD_LOWERED_SEQUENCES Step 8 reuses
to gate Panorama.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal

from widgets.science_site_bar import ScienceSiteBar
from widgets.science_sequence_widget import ScienceSequenceWidget
from widgets.camera_feed_widget import _frame_to_pixmap
from science_data_store import ScienceDataStore

_PAYLOAD_LOWERED_STATUSES = ("STARTING", "RUNNING", "STOPPING")
_PAYLOAD_LOWERED_SEQUENCES = ("SPECTROMETER", "NPK")
_SITE_REQUIRED_SEQUENCES = ("SPECTROMETER", "NPK", "PANORAMA", "STRATIGRAPHY")


class ScienceTabWidget(QWidget):

    launch_requested = pyqtSignal(str, bool)  # (sequence, collect_to_cache)
    stop_requested = pyqtSignal(str)          # (sequence)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._data_source = None
        self._sequence_widgets = {}  # sequence -> ScienceSequenceWidget, filled in as each is built
        self._sequence_statuses = {}  # sequence -> last known status, for payload-lowered gating
        self._store = ScienceDataStore()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(8)

        self.site_bar = ScienceSiteBar()
        self.site_bar.site_confirmed.connect(self._refresh_gating)
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

        panorama = ScienceSequenceWidget(
            sequence="PANORAMA", title="Panorama", stoppable=False, show_image=True,
        )
        self._register_sequence_widget(panorama)
        sequences_row.addWidget(panorama)

        stratigraphy = ScienceSequenceWidget(
            sequence="STRATIGRAPHY", title="Stratigraphic Photo", stoppable=False, show_image=True,
        )
        self._register_sequence_widget(stratigraphy)
        sequences_row.addWidget(stratigraphy)

        layout.addLayout(sequences_row, 1)

        self.review_button = QPushButton("Review Sites...")
        self.review_button.setEnabled(False)  # wired in Step 10
        layout.addWidget(self.review_button)

        self._refresh_gating()  # Spectrometer/NPK start blocked -- no site set yet

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
        self._sequence_statuses[sequence] = status
        self._store.record_status(self.site_bar.current_site(), sequence, status, message)
        self._refresh_gating()

    def _on_science_gnss(self, sequence: str, lat: float, lon: float):
        widget = self._sequence_widgets.get(sequence)
        if widget is not None:
            widget.set_gnss(lat, lon)
        self._store.record_gnss(self.site_bar.current_site(), sequence, lat, lon)

    def _on_science_image(self, sequence: str, frame, frame_bytes: int, timestamp: float):
        widget = self._sequence_widgets.get(sequence)
        if widget is not None:
            widget.set_image(_frame_to_pixmap(frame))
        self._store.record_image(self.site_bar.current_site(), sequence, frame)

    def _on_science_reading(self, sequence: str, reading: dict):
        widget = self._sequence_widgets.get(sequence)
        if widget is not None:
            widget.set_reading(reading)
        self._store.record_reading(self.site_bar.current_site(), sequence, reading)

    def _refresh_gating(self):
        site_set = self.site_bar.current_site() is not None
        for sequence in _SITE_REQUIRED_SEQUENCES:
            widget = self._sequence_widgets.get(sequence)
            if widget is not None:
                widget.set_blocked(not site_set, "Set a site first")

        payload_lowered = any(
            self._sequence_statuses.get(sequence) in _PAYLOAD_LOWERED_STATUSES
            for sequence in _PAYLOAD_LOWERED_SEQUENCES
        )
        self.site_bar.set_locked(payload_lowered)
