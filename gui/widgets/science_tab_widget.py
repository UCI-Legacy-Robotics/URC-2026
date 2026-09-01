"""
Science Mission tab.

Composes the Science-mission-specific controls: the current-site label
(ScienceSiteBar), the four rover-driven sequences (Spectrometer, NPK
probe, Panorama, Stratigraphic Photo, each a ScienceSequenceWidget),
and a "Review Sites..." button opening ScienceReviewDialog to browse
what's been saved so far.

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

No sequence is launchable at all until the rover has confirmed the
SCIENCE subsystem is actually RUNNING -- set_subsystem_mode()/
set_science_subsystem_status() track that (MainWindow calls them the
same way it drives SubsystemLaunchWidget), and both explicitly depend
on the mission being Science: set_subsystem_mode(mode != "SCIENCE")
forces the tracked RUNNING flag back off, so a stale confirmation from
a previous Science mission can't leak into gating for a different one.
In --sim this becomes true as soon as the top-strip Launch button's
fake progression reaches RUNNING; against real ROS it stays false
until a real launch topic/service exists and actually confirms it
(RosDataSource.send_subsystem_command is a no-op today -- see
ros_node.py), which is the intended fail-closed behavior, not a bug.

The site bar separately locks itself while Spectrometer or NPK is
running (STARTING/RUNNING/STOPPING) -- payload-lowered, not just
"site required" -- and Panorama is blocked on that same condition,
since it needs the science payload raised for its 360 rotation.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import pyqtSignal

from widgets.science_site_bar import ScienceSiteBar
from widgets.science_sequence_widget import ScienceSequenceWidget
from widgets.science_review_dialog import ScienceReviewDialog
from widgets.camera_feed_widget import _frame_to_pixmap
from science_data_store import ScienceDataStore

_PAYLOAD_LOWERED_STATUSES = ("STARTING", "RUNNING", "STOPPING")
_PAYLOAD_LOWERED_SEQUENCES = ("SPECTROMETER", "NPK")
_SITE_REQUIRED_SEQUENCES = ("SPECTROMETER", "NPK", "PANORAMA", "STRATIGRAPHY")


_RESOURCE_LABELS = {"CACHE": "Cache", "SPECTRO": "Spectrometer/vials"}


class ScienceTabWidget(QWidget):

    launch_requested = pyqtSignal(str, str)  # (sequence, mode -- "" if the sequence has none)
    stop_requested = pyqtSignal(str)         # (sequence)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._data_source = None
        self._sequence_widgets = {}  # sequence -> ScienceSequenceWidget, filled in as each is built
        self._sequence_statuses = {}  # sequence -> last known status, for payload-lowered gating
        self._mission_is_science = False
        self._science_subsystem_running = False
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
            launch_modes=[
                ("SPECTRO", "Run Spectrometer Analysis"),
                ("CACHE", "Collect to Cache"),
            ],
            show_gnss=True, show_image=True, show_reading=True,
        )
        # Spectrometer's mode choice needs a confirm-before-overwrite
        # check the other sequences don't -- routed through a dedicated
        # handler instead of the generic pass-through so a "No" on the
        # conflict dialog can abort the launch entirely.
        self._register_sequence_widget(spectrometer, launch_handler=self._on_spectrometer_launch_requested)
        sequences_row.addWidget(spectrometer)

        npk = ScienceSequenceWidget(
            sequence="NPK", title="NPK Probe", stoppable=True,
            reading_fields=[
                ("nitrogen_ppm", "N (ppm)"),
                ("phosphorus_ppm", "P (ppm)"),
                ("potassium_ppm", "K (ppm)"),
                ("temperature_c", "Temp (°C)"),
                ("humidity_pct", "Humidity (%)"),
                ("ph", "pH"),
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

        self._review_dialog = ScienceReviewDialog(self._store, parent=self)
        self.review_button = QPushButton("Review Sites...")
        self.review_button.clicked.connect(self._review_dialog.exec)
        layout.addWidget(self.review_button)

        self._refresh_gating()  # everything starts blocked -- no subsystem confirmation, no site set yet

    def bind_data_source(self, data_source):
        self._data_source = data_source
        data_source.signals.science_sequence_status.connect(self._on_science_status)
        data_source.signals.science_gnss_fix.connect(self._on_science_gnss)
        data_source.signals.science_image.connect(self._on_science_image)
        data_source.signals.science_reading.connect(self._on_science_reading)

    # -- public API, called by MainWindow ----------------------------------

    def set_subsystem_mode(self, mode: str):
        """Mirrors SubsystemLaunchWidget.set_mode() -- MainWindow calls
        this on every mission state change, same call site. Resetting
        the tracked RUNNING flag whenever the mission isn't Science
        (rather than only ever setting it from status updates) is what
        stops a launch confirmation from a previous Science mission
        from leaking into gating the next time Science comes around."""
        self._mission_is_science = (mode == "SCIENCE")
        if not self._mission_is_science:
            self._science_subsystem_running = False
        self._refresh_gating()

    def set_science_subsystem_status(self, subsystem: str, status: str):
        """Wire to DataSource.signals.subsystem_status_update. Ignored
        for any subsystem but SCIENCE, same filtering convention as
        ScienceSequenceWidget.set_status() filtering by its own sequence."""
        if subsystem != "SCIENCE":
            return
        self._science_subsystem_running = (status == "RUNNING")
        self._refresh_gating()

    # -- internal ---------------------------------------------------------

    def _register_sequence_widget(self, widget: ScienceSequenceWidget, launch_handler=None):
        self._sequence_widgets[widget.sequence] = widget
        widget.launch_requested.connect(launch_handler or self.launch_requested)
        widget.stop_requested.connect(self.stop_requested)

    def _on_spectrometer_launch_requested(self, sequence: str, mode: str):
        # CACHE and SPECTRO are each their own site-exclusive resource
        # (only one site's sample can occupy the cache, separately only
        # one site's sample can go through the spectrometer/vials) --
        # same conflict-confirm shape for either, just keyed by mode.
        current_site = self.site_bar.current_site()
        owner = self._store.get_resource_owner(mode)
        if owner is not None and owner != current_site:
            resource_label = _RESOURCE_LABELS.get(mode, mode)
            reply = QMessageBox.question(
                self, f"{resource_label} in use",
                f"{resource_label} currently holds a sample from '{owner}' — overwrite with '{current_site}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return  # abort -- no command sent, no status change
        self._store.set_resource_owner(mode, current_site)
        self.launch_requested.emit(sequence, mode)

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
        subsystem_ready = self._mission_is_science and self._science_subsystem_running
        site_set = self.site_bar.current_site() is not None
        payload_lowered = any(
            self._sequence_statuses.get(sequence) in _PAYLOAD_LOWERED_STATUSES
            for sequence in _PAYLOAD_LOWERED_SEQUENCES
        )

        # Multiple independent block reasons can apply to the same widget
        # (Panorama needs the subsystem up, a site set, AND the payload
        # not lowered) -- combine them into one set_blocked() call per
        # widget, checked in priority order, rather than separate calls
        # that would just have the last one overwrite the rest.
        for sequence in _SITE_REQUIRED_SEQUENCES:
            widget = self._sequence_widgets.get(sequence)
            if widget is None:
                continue
            if not subsystem_ready:
                widget.set_blocked(True, "Science subsystem not launched")
            elif not site_set:
                widget.set_blocked(True, "Set a site first")
            elif sequence == "PANORAMA" and payload_lowered:
                widget.set_blocked(True, "Blocked: payload lowered")
            else:
                widget.set_blocked(False)

        self.site_bar.set_locked(payload_lowered)
