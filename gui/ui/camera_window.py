"""
Second-monitor camera window: MUX panel on top, fixed 2x2 camera grid
below. Separate top-level window from MainWindow, instantiated
alongside it in main.py.

Pure display + the MUX panel — this window does not own any other GUI
state (mission state, electrical health, etc. stay on MainWindow only,
per the handoff). The grid's slot assignment is fixed and never
reflows based on which cameras are active; an inactive slot just shows
its own tile's "NO SIGNAL" placeholder in place.
"""

from PyQt6.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QWidget

from data_source import CAMERA_LABELS, CameraID
from widgets.camera_feed_widget import CameraFeedWidget
from widgets.camera_mux_panel import CameraMuxPanel

# Fixed slot assignment (row, col) — never changes based on which
# cameras are enabled/disabled.
_GRID_POSITIONS = {
    CameraID.BIRDS_EYE.value: (0, 0),        # top-left
    CameraID.SCIENCE_PAYLOAD.value: (0, 1),  # top-right
    CameraID.ARM_CAM_1.value: (1, 0),        # bottom-left
    CameraID.ARM_CAM_2.value: (1, 1),        # bottom-right
}


class CameraWindow(QWidget):

    def __init__(self, data_source=None, parent=None):
        super().__init__(parent)
        self.data_source = data_source

        self.setWindowTitle("Rover Base Station — Cameras")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)

        self.mux_panel = CameraMuxPanel()
        self.mux_panel.camera_toggle_requested.connect(self._on_camera_toggle_requested)

        # Panel only needs ~1/6 of the window's width, not a full-width
        # strip — stretch factors (1 vs. 5) split the row that way and
        # keep the rest empty rather than stretching the panel's own
        # rows to fill the leftover space.
        top_row = QHBoxLayout()
        top_row.addWidget(self.mux_panel, 1)
        top_row.addStretch(5)
        layout.addLayout(top_row)

        grid_container = QWidget()
        grid = QGridLayout(grid_container)
        grid.setSpacing(6)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)

        self.tiles = {}
        for camera_id, (row, col) in _GRID_POSITIONS.items():
            tile = CameraFeedWidget(camera_id, CAMERA_LABELS[camera_id])
            grid.addWidget(tile, row, col)
            self.tiles[camera_id] = tile

        layout.addWidget(grid_container, 1)

        if self.data_source is not None:
            self.mux_panel.bind_data_source(self.data_source)
            for tile in self.tiles.values():
                tile.bind_data_source(self.data_source)

    def _on_camera_toggle_requested(self, camera_id, enabled):
        if self.data_source is not None:
            if enabled:
                self.data_source.enable_camera(camera_id)
            else:
                self.data_source.disable_camera(camera_id)

        # Confirm back into both mirrors of this camera's state — see
        # camera_feed_tracker.py for why the DataSource call alone
        # can't drive either display.
        self.mux_panel.set_camera_enabled(camera_id, enabled)
        self.tiles[camera_id].set_enabled(enabled)
