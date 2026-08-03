"""
Subsystem Launch widget — top strip, middle section.

Minimal for now: just displays which subsystem is currently selected
(Science / Arm / None). MainWindow drives `set_mode()` automatically from
mission state changes — operators don't pick this manually outside
Diagnostics mode, since it's implied by which mission is running. Real
launch/stop buttons and per-subsystem status indicators are a later step
(see handoff Step 8); this class is built so those can be added onto it
without changing `set_mode()`'s interface.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class SubsystemLaunchWidget(QWidget):

    _COLORS = {
        "SCIENCE": "#1b5e20",
        "ARM": "#0d47a1",
        "NONE": "#3a3a3a",
    }

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)

        title = QLabel("SUBSYSTEM LAUNCH")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #888; font-size: 10px;")
        layout.addWidget(title)

        self._mode_label = QLabel()
        self._mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._mode_label)

        self.set_mode("NONE")

    def set_mode(self, mode: str):
        """mode: one of "SCIENCE", "ARM", "NONE"."""
        color = self._COLORS.get(mode, self._COLORS["NONE"])
        self._mode_label.setText(mode)
        self._mode_label.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #ffffff; "
            f"background: {color}; border-radius: 4px; padding: 10px;"
        )
