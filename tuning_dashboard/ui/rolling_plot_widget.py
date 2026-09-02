"""
One rolling time-series tile: title/units header, a "last update" age
label, a Pause/Live button, and a pyqtgraph plot underneath.

Live mode (default) keeps the X range following the newest sample --
"rolling graph that moves forward in time". Y range is left on
pyqtgraph's continuous auto-range the whole time, so it always rescales
to whatever's currently visible regardless of pause state.

Pausing only stops *this widget* from calling setXRange -- it does not
stop buffering incoming samples. That's deliberate: once auto-follow
stops fighting the view, pyqtgraph's own mouse-drag-to-pan and
scroll-to-zoom on the ViewBox (enabled by default, no extra code needed
here) become the scroll-back/rescale controls. "Jump to Live" snaps the
view back and resumes auto-follow; nothing was lost while paused since
the buffer kept growing underneath.

add_sample() only buffers -- it deliberately does NOT touch the plot.
Redrawing (curve.setData + setXRange) happens separately, on refresh(),
called by MainWindow on a fixed-rate timer shared across all tiles.
Redrawing on every single incoming sample was tried first and made the
whole window unresponsive (couldn't even click Pause or close it) once
real topics were publishing at their actual rate -- 19 tiles x ~20 Hz is
~380 repaints/sec competing with the GUI thread for button clicks and
the close event. Capping the redraw rate independent of the data rate
is the standard fix for this in real-time plotting.
"""

import time
from collections import deque

import pyqtgraph as pg
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

_AGE_TICK_MS = 500


class RollingPlotWidget(QWidget):
    def __init__(self, title: str, units: str, window_seconds: float, parent=None):
        super().__init__(parent)
        self._window_seconds = window_seconds
        self._buffer = deque()  # [(t_relative, value), ...], oldest first
        self._paused = False
        self._last_update_wall = None  # time.time() of most recent sample, for the age label
        self._dirty = False  # True when the buffer has samples refresh() hasn't drawn yet

        self._title_label = QLabel(f"{title} ({units})" if units else title)
        self._title_label.setStyleSheet("font-weight: bold;")

        self._age_label = QLabel("no data")
        self._age_label.setStyleSheet("color: #888;")

        self._pause_button = QPushButton("Pause")
        self._pause_button.clicked.connect(self._toggle_paused)

        header = QHBoxLayout()
        header.addWidget(self._title_label)
        header.addStretch()
        header.addWidget(self._age_label)
        header.addWidget(self._pause_button)

        self._plot = pg.PlotWidget()
        self._plot.setBackground("k")
        self._plot.showGrid(x=True, y=True, alpha=0.3)
        self._plot.setLabel("left", units)
        self._plot.setLabel("bottom", "t", units="s")
        self._plot.getViewBox().enableAutoRange(axis=pg.ViewBox.YAxis, enable=True)
        self._curve = self._plot.plot(pen=pg.mkPen(color="#4a9eff", width=2))

        layout = QVBoxLayout(self)
        layout.addLayout(header)
        layout.addWidget(self._plot)

        self._age_timer = QTimer(self)
        self._age_timer.timeout.connect(self._update_age_label)
        self._age_timer.start(_AGE_TICK_MS)

    def add_sample(self, t_relative: float, value: float):
        """Cheap: buffer the sample and mark dirty. Never touches the
        plot itself -- see the class docstring for why."""
        self._buffer.append((t_relative, value))
        cutoff = t_relative - self._window_seconds
        while self._buffer and self._buffer[0][0] < cutoff:
            self._buffer.popleft()

        self._last_update_wall = time.time()
        self._dirty = True

    def refresh(self):
        """Redraws the curve from the current buffer, if it's changed
        since the last refresh. Called by MainWindow on a fixed-rate
        timer shared across all tiles -- not from add_sample."""
        if not self._dirty:
            return
        self._dirty = False

        xs, ys = zip(*self._buffer)
        self._curve.setData(xs, ys)
        if not self._paused:
            latest_t = xs[-1]
            self._plot.setXRange(latest_t - self._window_seconds, latest_t, padding=0)

    def _toggle_paused(self):
        self._paused = not self._paused
        self._pause_button.setText("Jump to Live" if self._paused else "Pause")
        if not self._paused and self._buffer:
            latest_t = self._buffer[-1][0]
            self._plot.setXRange(latest_t - self._window_seconds, latest_t, padding=0)

    def set_paused(self, paused: bool):
        """Driven by a global Pause All/Resume All toolbar (main_window.py)."""
        if paused != self._paused:
            self._toggle_paused()

    def _update_age_label(self):
        if self._last_update_wall is None:
            return
        age = time.time() - self._last_update_wall
        self._age_label.setText(f"{age:.1f}s ago")
