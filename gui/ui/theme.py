"""
App-wide look: theme setup, semantic status colors, and icons.

Three libraries split the styling work, each doing what it's best at:
  - pyqtdarktheme (qdarktheme) restyles every *stock* Qt widget app-wide
    -- QTabWidget, QProgressBar, QDialog, QScrollArea, combo popups, etc.
    -- so nothing falls back to the OS's light palette.
  - PyQt-Fluent-Widgets supplies the controls themselves (PushButton,
    CheckBox, LineEdit, ComboBox, cards, labels, InfoBar toasts, ...),
    which carry their own stylesheets and so take precedence over
    qdarktheme's wherever the two overlap.
  - QtAwesome supplies icons by name (Material Design Icons, "mdi6.*").

Status colors stay hand-picked rather than coming from either theme:
they're semantic (green = running, amber = pending, red = fault) and
operators read them at a glance, so they must not drift with a theme
change. Every widget pulls them from here rather than keeping its own
copy of the same table.
"""

import os

# QtAwesome finds Qt through QtPy, which would otherwise pick the system
# PyQt5 that ROS installs before PyQt6 -- and mixing both in one process
# crashes. Must be set before qtawesome is first imported.
os.environ.setdefault("QT_API", "pyqt6")

import qdarktheme  # noqa: E402
import qtawesome as qta  # noqa: E402
from qfluentwidgets import Theme, setTheme, setThemeColor  # noqa: E402

ACCENT = "#4a9eff"
TEXT = "#e0e0e0"
TEXT_MUTED = "#9aa0a6"

GREEN = "#1b5e20"
AMBER = "#8a6d1a"
RED = "#7a1f1f"
BRIGHT_RED = "#d32f2f"
ORANGE = "#e65100"
BLUE = "#0d47a1"
PURPLE = "#6a1b9a"
NEUTRAL = "#3a3a3a"
STALE = "#4a4a2a"

# Shared by every launch/stop sequence (subsystem launch, science and
# equipment sequences, autonomous nav).
STATUS_COLORS = {
    "IDLE": NEUTRAL,
    "STARTING": AMBER,
    "RUNNING": GREEN,
    "ARRIVED": GREEN,
    "STOPPING": AMBER,
    "STOPPED": NEUTRAL,
    "ERROR": RED,
}
RUNNING_LIKE_STATUSES = ("STARTING", "RUNNING")

# Camera feed state text colors (MUX panel rows and grid tiles).
CAMERA_STATE_COLORS = {
    "ON": "#3ba33b",
    "OFF": "#888888",
    "NO SIGNAL": "#c0392b",
    "LOCKED": "#666666",
}


def icon(name: str, color: str = TEXT):
    """QtAwesome icon by name, e.g. icon("mdi6.play"). Browse names with
    the `qta-browser` command that QtAwesome installs."""
    return qta.icon(name, color=color, color_disabled="#5f6368")


# qdarktheme gives QLineEdit/QAbstractSpinBox a stylesheet min-height, and
# a stylesheet size constraint beats the setFixedHeight(33) Fluent's
# inputs set on themselves -- they'd render squashed to ~20px without
# this. 31px content + 1px border top and bottom = Fluent's 33px. Type
# selectors match Fluent's Python class names (and subclasses, e.g.
# SearchLineEdit).
_FLUENT_FIXUPS_QSS = """
LineEdit, SpinBox, DoubleSpinBox { min-height: 31px; max-height: 31px; }
"""


def apply_theme(app):
    """Call once, right after constructing the QApplication."""
    qdarktheme.setup_theme(
        "dark",
        corner_shape="rounded",
        custom_colors={"primary": ACCENT},
        additional_qss=_FLUENT_FIXUPS_QSS,
    )
    setTheme(Theme.DARK)
    setThemeColor(ACCENT)
