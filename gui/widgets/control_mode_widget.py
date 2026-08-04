"""
Control Mode indicator

Shows whether the rover is presently under teleoperation or autonomous
control. Derived from mission state rather than a separate ROS topic:
in URC's ruleset, only the Autonomous Navigation mission drives itself —
every other active mission (Science, Delivery, Equipment Servicing) is
teleoperated, and Idle/Diagnostics have no drive mode at all. MainWindow
drives `set_mode()` the same way it drives SubsystemLaunchWidget. If a
real control-mode topic shows up later, this is the seam to wire it into
instead of mission state.
"""

from widgets.mode_badge_widget import ModeBadgeWidget

_COLORS = {
    "TELEOPERATION": "#0d47a1",
    "AUTONOMOUS": "#7a1f1f",
    "STANDBY": "#3a3a3a",
}


class ControlModeWidget(ModeBadgeWidget):

    def __init__(self, parent=None):
        super().__init__(
            title="CONTROL MODE",
            colors=_COLORS,
            default_mode="STANDBY",
            parent=parent,
        )
