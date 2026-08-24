"""
Science Site Bar

Lets the operator label the "current site" before launching a
site-scoped sequence (Spectrometer / NPK) — the science team visits
multiple sites per run, and everything those sequences report (status,
GNSS, images, readings) needs to land tagged under the right site
rather than getting mixed together (see ScienceDataStore, Step 6).

This widget only tracks the label text itself; it has no DataSource
dependency and doesn't know anything about sequences, gating, or
persistence — ScienceTabWidget composes those concerns on top of it
(disabling Spectrometer/NPK launch while no site is set, locking this
bar while one is running, in Step 7).
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import pyqtSignal

from widgets.color_coded_label import ColorCodedLabel

_NO_SITE_COLOR = "#3a3a3a"
_SITE_SET_COLOR = "#1b5e20"


class ScienceSiteBar(QWidget):

    site_confirmed = pyqtSignal(str)  # new current-site label

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_site = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self._input = QLineEdit()
        self._input.setPlaceholderText("Site label (e.g. Outcrop North)")
        self._input.returnPressed.connect(self._on_confirm_clicked)

        self._confirm_button = QPushButton("Set Current Site")
        self._confirm_button.clicked.connect(self._on_confirm_clicked)

        self._badge = ColorCodedLabel()
        self._badge.setMinimumWidth(160)

        layout.addWidget(self._input)
        layout.addWidget(self._confirm_button)
        layout.addWidget(self._badge)

        self._refresh_badge()

    # -- public API ---------------------------------------------------

    def current_site(self) -> str | None:
        return self._current_site

    def set_locked(self, locked: bool):
        """Disable editing while a site-scoped sequence is running, so
        the operator can't relabel the site mid-sequence."""
        self._input.setEnabled(not locked)
        self._confirm_button.setEnabled(not locked)

    # -- internal -------------------------------------------------------

    def _on_confirm_clicked(self):
        label = self._input.text().strip()
        if not label:
            return
        self._current_site = label
        self._refresh_badge()
        self.site_confirmed.emit(label)

    def _refresh_badge(self):
        if self._current_site is None:
            self._badge.set_state("No site set", _NO_SITE_COLOR)
        else:
            self._badge.set_state(f"Site: {self._current_site}", _SITE_SET_COLOR)
