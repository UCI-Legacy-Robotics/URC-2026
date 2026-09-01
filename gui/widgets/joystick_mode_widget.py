"""
Joystick Mode indicator

Shows which subsystem the physical game controller currently drives:
DRIVETRAIN or ARM. A hardware mode button on the joystick itself picks
this, not the GUI -- the GUI only displays whatever the rover reports,
sourced purely from DataSource.signals.joystick_mode (MainWindow
forwards it straight to `set_mode()`, same pattern as ControlModeWidget
just under it in the Sidebar).

Defaults to DRIVETRAIN, since ARM is never valid before the Arm
subsystem has actually launched -- see SimulationDataSource's
set_joystick_mode() for how --sim enforces that same constraint.
"""

from widgets.mode_badge_widget import ModeBadgeWidget

_COLORS = {
    "DRIVETRAIN": "#0d47a1",
    "ARM": "#6a1b9a",
}


class JoystickModeWidget(ModeBadgeWidget):

    def __init__(self, parent=None):
        super().__init__(
            title="JOYSTICK MODE",
            colors=_COLORS,
            default_mode="DRIVETRAIN",
            parent=parent,
        )
