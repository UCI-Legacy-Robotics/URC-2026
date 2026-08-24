"""
Second-monitor camera window: MUX panel on top, fixed 2x2 camera grid
below. Separate top-level window from MainWindow, instantiated
alongside it in main.py.

Pure display + the MUX panel — this window does not own any other GUI
state (mission state, electrical health, etc. stay on MainWindow only,
per the handoff). The grid's slot assignment is fixed and never
reflows based on which cameras are active; an inactive slot just shows
its own tile's "NO SIGNAL"/"LOCKED" placeholder in place.

Science and Arm cameras are gated on their payload's subsystem being
confirmed RUNNING via DataSource.signals.subsystem_status_update — a
camera physically can't produce a feed before its payload has power.
This is the one deliberate exception to "the MUX is otherwise fully
manual, no MissionState ties" (see camera_mux_panel.py): it's wired to
subsystem launch confirmation, not to MissionState directly, and it
only gates *enabling* a camera — it doesn't select/lock the mission
tabs or anything else MissionStateMachine already governs. Bird's Eye
lives on the comms tower, independent of any subsystem, so it's never
gated.
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

# Which subsystem_status_update subsystem name gates each camera.
# Cameras with no entry here (Bird's Eye) are never locked.
_CAMERA_GATING_SUBSYSTEM = {
    CameraID.SCIENCE_PAYLOAD.value: "SCIENCE",
    CameraID.ARM_CAM_1.value: "ARM",
    CameraID.ARM_CAM_2.value: "ARM",
}


class CameraWindow(QWidget):

    def __init__(self, data_source=None, parent=None):
        super().__init__(parent)
        self.data_source = data_source

        # Gated cameras start locked — no subsystem is RUNNING until an
        # operator launches it, regardless of whether a DataSource is
        # even wired up.
        self._subsystem_running = {"SCIENCE": False, "ARM": False}

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
            self.data_source.signals.subsystem_status_update.connect(
                self._on_subsystem_status_update
            )

        # Apply the initial locked state to both mirrors of every gated
        # camera (all locked, since self._subsystem_running starts
        # all-False above).
        for camera_id in _CAMERA_GATING_SUBSYSTEM:
            self._set_camera_locked(camera_id, True)

    def _on_camera_toggle_requested(self, camera_id, enabled):
        if enabled and self._is_camera_locked(camera_id):
            return  # belt-and-suspenders — the MUX button is disabled while locked anyway

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

    def _on_subsystem_status_update(self, subsystem, status):
        if subsystem not in self._subsystem_running:
            return  # not a gating subsystem (or an unrecognized name) — nothing to do

        running = status == "RUNNING"
        if running == self._subsystem_running[subsystem]:
            return
        self._subsystem_running[subsystem] = running

        for camera_id, gating_subsystem in _CAMERA_GATING_SUBSYSTEM.items():
            if gating_subsystem != subsystem:
                continue
            self._set_camera_locked(camera_id, not running)
            if not running:
                # Subsystem confirmed stopped — auto-disable the camera
                # too rather than leaving it ON with no power behind
                # it; re-enabling requires the payload to launch again.
                self._on_camera_toggle_requested(camera_id, False)

    def _is_camera_locked(self, camera_id):
        subsystem = _CAMERA_GATING_SUBSYSTEM.get(camera_id)
        if subsystem is None:
            return False
        return not self._subsystem_running[subsystem]

    def _set_camera_locked(self, camera_id, locked):
        self.mux_panel.set_camera_locked(camera_id, locked)
        self.tiles[camera_id].set_locked(locked)
