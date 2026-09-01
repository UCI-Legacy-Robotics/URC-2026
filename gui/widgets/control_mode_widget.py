"""
Control Mode indicator

Shows whether the rover is presently under teleoperation or autonomous
control. Default comes from mission state: in URC's ruleset, only the
Autonomous Navigation mission drives itself — every other active
mission (Science, Delivery, Equipment Servicing) is teleoperated, and
Idle has no drive mode at all. Diagnostics isn't a mission state and
never appears here — it's an always-available tab with no bearing on
control mode. MainWindow drives `set_mode()` on mission state change
the same way it drives SubsystemLaunchWidget.

The rover can also override that default live: it broadcasts its own
control mode over ROS when it self-drives a maneuver mid-mission (e.g.
switching itself to AUTONOMOUS for Panorama's 360 rotation, then
reporting back to TELEOPERATION once it hands control back) --
MainWindow forwards DataSource.signals.rover_control_mode straight to
`set_mode()` for that, no merging/inference, same signal shape.
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
