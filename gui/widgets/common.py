"""
Small building blocks shared across widgets, so each widget composes
these instead of carrying its own copy-pasted stylesheet strings.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from qfluentwidgets import IconWidget, SimpleCardWidget, StrongBodyLabel

import theme


class SectionCard(SimpleCardWidget):
    """Rounded, theme-aware panel with an optional icon + title header.
    Add content to `self.body` (a QVBoxLayout)."""

    def __init__(self, title: str = None, icon_name: str = None, parent=None):
        super().__init__(parent)
        self.body = QVBoxLayout(self)
        self.body.setContentsMargins(12, 10, 12, 10)
        self.body.setSpacing(6)

        if title:
            header = QHBoxLayout()
            header.setSpacing(8)
            if icon_name:
                header_icon = IconWidget(theme.icon(icon_name, theme.ACCENT))
                header_icon.setFixedSize(16, 16)
                header.addWidget(header_icon)
            header.addWidget(StrongBodyLabel(title))
            header.addStretch()
            self.body.addLayout(header)


def readout_box(height: int, font_size: int) -> QLabel:
    """Fixed-height text box for a status message or a data readout.
    Fixed rather than content-sized so a longer message or new reading
    never grows/shrinks its card and shifts the rest of the dashboard."""
    label = QLabel()
    label.setWordWrap(True)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setFixedHeight(height)
    label.setStyleSheet(
        f"color: {theme.TEXT}; font-size: {font_size}px; "
        "background: rgba(255, 255, 255, 0.04); "
        "border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 6px; padding: 2px;"
    )
    return label


class DangerButton(QPushButton):
    """Unmistakably red button for E-Stop/Abort. Deliberately not a
    themed Fluent button -- these must stay red whatever the accent
    color is."""

    def __init__(self, text: str, icon_name: str = None, font_size: int = 14, parent=None):
        super().__init__(text, parent)
        if icon_name:
            self.setIcon(theme.icon(icon_name, "#ffffff"))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(
            f"QPushButton {{ font-size: {font_size}px; font-weight: bold; color: #ffffff; "
            f"background: #b3261e; border: 1px solid #e5484d; border-radius: 6px; padding: 8px; }} "
            "QPushButton:hover { background: #c9302c; } "
            "QPushButton:pressed { background: #8f1f19; } "
            "QPushButton:disabled { color: #777; background: #2a2a2a; border: 1px solid #3a3a3a; }"
        )


def set_button(button, text: str, icon_name: str = None):
    """Update a button's text and icon together -- launch/stop buttons
    swap both on every status change."""
    button.setText(text)
    if icon_name:
        button.setIcon(theme.icon(icon_name))
