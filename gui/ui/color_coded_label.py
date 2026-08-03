"""
QLabel that renders as a colored badge: bold white text on a colored,
rounded background. Shared by anything that shows "current state/mode as
a colored box" — the Mission State Machine's state display, Subsystem
Launch, Control Mode, etc. — so the visual style lives in exactly one
place instead of being restyled per widget.
"""

from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt


class ColorCodedLabel(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_state(self, text: str, color: str):
        self.setText(text)
        self.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #ffffff; "
            f"background: {color}; border-radius: 4px; padding: 8px;"
        )
