"""
Science Mission tab.

Composes the Science-mission-specific controls: the current-site label
(ScienceSiteBar) and the four rover-driven sequences (Spectrometer, NPK
probe, Panorama, Stratigraphic Photo). Each sequence slot is still a
dashed placeholder here — ScienceSequenceWidget instances replace them
one at a time in Steps 2-5, same incremental-build approach as the rest
of the tab (site tagging, persistence, gating, review dialog) arriving
in later steps.

bind_data_source() only stores the reference for now; nothing in this
tab reacts to DataSource signals yet (that starts in Step 2, once
there's a real sequence signal contract to listen to).
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton
)
from PyQt6.QtCore import Qt

from widgets.science_site_bar import ScienceSiteBar

_SEQUENCE_TITLES = ("Spectrometer", "NPK Probe", "Panorama", "Stratigraphic Photo")


def _placeholder_slot(title: str) -> QFrame:
    """Dashed-border stand-in for a not-yet-built ScienceSequenceWidget,
    same visual language as main_window.py's _placeholder_box so the
    tab doesn't look inconsistent with the other still-placeholder
    tabs while this one is under construction."""
    frame = QFrame()
    frame.setFrameShape(QFrame.Shape.StyledPanel)
    frame.setMinimumHeight(160)
    frame.setStyleSheet(
        "QFrame { border: 1px dashed #3a3a3a; border-radius: 4px; background: #111; }"
    )

    label = QLabel(f"{title}\n(not yet implemented)")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet("color: #666; font-size: 11px; border: none;")
    label.setWordWrap(True)

    layout = QVBoxLayout(frame)
    layout.addWidget(label)
    return frame


class ScienceTabWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._data_source = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(8)

        self.site_bar = ScienceSiteBar()
        layout.addWidget(self.site_bar)

        sequences_row = QHBoxLayout()
        sequences_row.setSpacing(8)
        for title in _SEQUENCE_TITLES:
            sequences_row.addWidget(_placeholder_slot(title))
        layout.addLayout(sequences_row, 1)

        self.review_button = QPushButton("Review Sites...")
        self.review_button.setEnabled(False)  # wired in Step 10
        layout.addWidget(self.review_button)

    def bind_data_source(self, data_source):
        self._data_source = data_source
