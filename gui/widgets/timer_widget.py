"""
Mission countdown timer widget.

Lives in the persistent status bar (owned by MainWindow), not inside any
one mission tab. Each mission tab is responsible for calling start() with
its own duration when the operator begins that mission — durations are
NOT hardcoded here since some missions have judge-set/variable time
limits (e.g. Science: 20-30 min, Delivery: 30-60 min).

Per rule 3.c.viii, the mission clock keeps running during interventions —
pause() is exposed for operator override only, it is not auto-triggered
by intervention logging.
"""

from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import QTimer, pyqtSignal, Qt


class MissionTimerWidget(QWidget):

    time_updated = pyqtSignal(int)   # remaining seconds
    time_expired = pyqtSignal()

    # Below this many remaining seconds, display switches to a warning color.
    WARNING_THRESHOLD_SECONDS = 60

    _COLOR_NORMAL = "#e0e0e0"
    _COLOR_WARNING = "#ff4a4a"
    _COLOR_STOPPED = "#777777"

    def __init__(self, parent=None):
        super().__init__(parent)

        self._remaining_seconds = 0
        self._running = False

        self._qtimer = QTimer(self)
        self._qtimer.setInterval(1000)
        self._qtimer.timeout.connect(self._tick)

        self._label = QLabel("--:--")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setStyleSheet(
            f"font-size: 20px; font-weight: bold; color: {self._COLOR_STOPPED};"
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.addWidget(self._label)

    # -- public control API --------------------------------------------

    def start(self, duration_seconds: int):
        """Start (or restart) the countdown from duration_seconds."""
        self._remaining_seconds = max(0, int(duration_seconds))
        self._running = True
        self._qtimer.start()
        self._refresh_display()

    def pause(self):
        self._running = False
        self._qtimer.stop()
        self._refresh_display()

    def resume(self):
        if self._remaining_seconds <= 0:
            return
        self._running = True
        self._qtimer.start()
        self._refresh_display()

    def reset(self):
        self._running = False
        self._qtimer.stop()
        self._remaining_seconds = 0
        self._label.setText("--:--")
        self._label.setStyleSheet(
            f"font-size: 20px; font-weight: bold; color: {self._COLOR_STOPPED};"
        )

    def is_running(self) -> bool:
        return self._running

    def remaining_seconds(self) -> int:
        return self._remaining_seconds

    # -- internal ---------------------------------------------------------

    def _tick(self):
        if self._remaining_seconds <= 0:
            self._qtimer.stop()
            self._running = False
            self.time_expired.emit()
            self._refresh_display()
            return

        self._remaining_seconds -= 1
        self.time_updated.emit(self._remaining_seconds)
        self._refresh_display()

    def _refresh_display(self):
        minutes, seconds = divmod(self._remaining_seconds, 60)
        self._label.setText(f"{minutes:02d}:{seconds:02d}")

        if not self._running and self._remaining_seconds > 0:
            color = self._COLOR_STOPPED  # paused
        elif self._remaining_seconds <= self.WARNING_THRESHOLD_SECONDS:
            color = self._COLOR_WARNING
        else:
            color = self._COLOR_NORMAL

        self._label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {color};")