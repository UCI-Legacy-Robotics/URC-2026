"""
Control Mode indicator

Shows whether the rover is presently under teleoperation or autonomous
control. Deliberately NOT derived from GUI/mission state -- the game
controller can teleoperate the rover whether or not a mission is even
active in the GUI, and the rover switches itself into AUTONOMOUS for
specific self-driven maneuvers (e.g. Panorama's 360 rotation) on its
own schedule, not the GUI's. This is sourced purely from
DataSource.signals.rover_control_mode -- MainWindow forwards it
straight to `set_mode()`, no merging with mission state, no inference.

Defaults to TELEOPERATION (not an "unknown" placeholder state) because
that's the actual physical default any time nothing has overridden it,
in both --sim (which starts sequences from TELEOPERATION and switches
away only for things like Panorama) and real hardware (teleoperation
via the game controller needs no launched subsystem or active mission).
"""

from widgets.mode_badge_widget import ModeBadgeWidget

_COLORS = {
    "TELEOPERATION": "#0d47a1",
    "AUTONOMOUS": "#7a1f1f",
}


class ControlModeWidget(ModeBadgeWidget):

    def __init__(self, parent=None):
        super().__init__(
            title="CONTROL MODE",
            colors=_COLORS,
            default_mode="TELEOPERATION",
            parent=parent,
        )
