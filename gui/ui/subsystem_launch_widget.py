"""
Subsystem Launch widget

Minimal for now: just displays which subsystem is currently selected
(Science / Arm / None). MainWindow drives `set_mode()` automatically from
mission state changes — operators don't pick this manually outside
Diagnostics mode, since it's implied by which mission is running. Real
launch/stop buttons and per-subsystem status indicators are a later step
(see handoff Step 8); this class is built so those can be added onto it
without changing `set_mode()`'s interface.
"""

from ui.mode_badge_widget import ModeBadgeWidget

_COLORS = {
    "SCIENCE": "#1b5e20",
    "ARM": "#0d47a1",
    "NONE": "#3a3a3a",
}


class SubsystemLaunchWidget(ModeBadgeWidget):

    def __init__(self, parent=None):
        super().__init__(
            title="SUBSYSTEM LAUNCH",
            colors=_COLORS,
            default_mode="NONE",
            parent=parent,
        )
