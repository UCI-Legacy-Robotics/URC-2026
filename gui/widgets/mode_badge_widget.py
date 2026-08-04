"""
Small reusable "title label + colored mode badge" widget, built on
ColorCodedLabel. For compact indicators that are just a name from a
fixed set of modes with a background color per mode (Subsystem Launch,
Control Mode, ...). Not for anything with sub-controls or its own live
data stream — those get their own dedicated widget.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from widgets.color_coded_label import ColorCodedLabel


class ModeBadgeWidget(QWidget):

    def __init__(self, title: str, colors: dict, default_mode: str, parent=None):
        super().__init__(parent)
        self._colors = colors
        self._default_color = colors.get(default_mode, "#3a3a3a")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #888; font-size: 10px;")
        layout.addWidget(title_label)

        self._mode_label = ColorCodedLabel()
        layout.addWidget(self._mode_label)

        self.set_mode(default_mode)

    def set_mode(self, mode: str):
        color = self._colors.get(mode, self._default_color)
        self._mode_label.set_state(mode, color)
