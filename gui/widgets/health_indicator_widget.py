"""
Base widget for a single Electrical Health cluster indicator.

Composes its own StaleDataWatcher (stale_data.py) rather than sharing one
across the cluster — a real DiagnosticArray message may only carry
updates for the fields that changed, so one probe going quiet shouldn't
be masked by others still reporting on the same tick.

Per the "degrade visibly, not silently" rule: a stale indicator keeps
showing its last known text/color but dims it and appends "(STALE)"
rather than freezing on the old value with no indication, or blanking to
a generic placeholder that loses the last-known reading.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from widgets.color_coded_label import ColorCodedLabel
from stale_data import StaleDataWatcher

_STALE_COLOR = "#4a4a2a"
_DEFAULT_COLOR = "#3a3a3a"


class HealthIndicatorWidget(QWidget):

    def __init__(self, title: str, stale_timeout_ms: int, parent=None):
        super().__init__(parent)
        self._last_text = "--"
        self._last_color = _DEFAULT_COLOR

        self.watcher = StaleDataWatcher(stale_timeout_ms, parent=self)
        self.watcher.became_stale.connect(self._on_became_stale)
        self.watcher.became_fresh.connect(self._on_became_fresh)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #888; font-size: 9px;")
        layout.addWidget(title_label)

        self._value_label = ColorCodedLabel()
        layout.addWidget(self._value_label)

        self._render(self._last_text, self._last_color)

    def update_value(self, text: str, color: str):
        """Call whenever fresh data for this indicator arrives."""
        self._last_text = text
        self._last_color = color
        self.watcher.notify()
        self._render(text, color)

    def _on_became_stale(self):
        self._render(f"{self._last_text} (STALE)", _STALE_COLOR)

    def _on_became_fresh(self):
        self._render(self._last_text, self._last_color)

    def _render(self, text: str, color: str):
        self._value_label.set_state(text, color)


class DiagnosticsStatusIndicator(HealthIndicatorWidget):
    """A HealthIndicatorWidget driven by one named entry out of
    DataSource.signals.diagnostics_update's list-of-dicts payload (see
    data_source.py for the shape).

    Subclasses implement `_render_status(status) -> (text, color)`;
    this base handles finding "its" entry by name on every update — the
    bit every diagnostics-backed indicator needs, shared in one place
    instead of copy-pasted per indicator.
    """

    def __init__(self, title: str, diagnostics_name: str, stale_timeout_ms: int, parent=None):
        super().__init__(title, stale_timeout_ms, parent)
        self.diagnostics_name = diagnostics_name

    def on_diagnostics_update(self, statuses):
        for status in statuses:
            if status["name"] == self.diagnostics_name:
                text, color = self._render_status(status)
                self.update_value(text, color)
                return

    def _render_status(self, status: dict):
        raise NotImplementedError
