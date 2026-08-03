"""
GNSS map widget — sidebar, main area.

Locally-rendered only: no live tile fetching (the competition site has no
internet access). This draws a simple grid rather than real map tiles —
picking/loading an actual offline tile source is a later, non-blocking
decision (see handoff Step 13); the position/heading/pin-plotting logic
here is written so a real tile layer can be dropped in underneath later
without touching it.

Shows the rover's position (from gnss_fix) and heading (from imu_update's
yaw_deg — there's no separate heading widget, IMU is the only source of
truth for it) on a simple local flat-earth projection centered on the
first GNSS fix received. Waypoints are manually entered by the operator
(lat/lon fields + Add Pin) rather than click-to-place, per current design
decision.

Degrades visibly per the top-level ground rule: if gnss_fix goes quiet,
the rover marker dims and a "GNSS: STALE" label appears rather than the
marker just freezing with no indication.
"""

import math

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDoubleSpinBox
)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QColor, QPolygonF

from stale_data import StaleDataWatcher

_GRID_COLOR = QColor("#1e1e1e")
_ROVER_COLOR = QColor("#4a9eff")
_ROVER_STALE_COLOR = QColor("#555566")
_PIN_COLOR = QColor("#ff4a4a")
_TEXT_COLOR = QColor("#888888")

_PIXELS_PER_METER = 1.5
_GRID_STEP_PX = 30

_GNSS_STALE_TIMEOUT_MS = 5000

# Meters per degree of latitude is ~constant; longitude shrinks with
# cos(latitude) — a flat-earth approximation, fine at competition-site
# scale (tens to hundreds of meters), not for anything larger.
_METERS_PER_DEG_LAT = 111_320


class _MapCanvas(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(220)

        self._origin = None       # (lat, lon) of first fix — local projection center
        self._rover_pos = None    # (lat, lon)
        self._heading_deg = 0.0
        self._pins = []           # list of (lat, lon, label)

        self._gnss_watcher = StaleDataWatcher(_GNSS_STALE_TIMEOUT_MS, parent=self)
        self._gnss_watcher.became_stale.connect(self.update)
        self._gnss_watcher.became_fresh.connect(self.update)

    def on_gnss_fix(self, lat: float, lon: float):
        if self._origin is None:
            self._origin = (lat, lon)
        self._rover_pos = (lat, lon)
        self._gnss_watcher.notify()
        self.update()

    def on_imu_update(self, imu):
        self._heading_deg = imu.yaw_deg
        self.update()

    def add_pin(self, lat: float, lon: float, label: str = ""):
        self._pins.append((lat, lon, label))
        self.update()

    # -- internal -----------------------------------------------------

    def _to_pixels(self, lat: float, lon: float) -> QPointF:
        origin_lat, origin_lon = self._origin
        meters_per_deg_lon = _METERS_PER_DEG_LAT * math.cos(math.radians(origin_lat))

        dx_m = (lon - origin_lon) * meters_per_deg_lon
        dy_m = (lat - origin_lat) * _METERS_PER_DEG_LAT

        center = QPointF(self.width() / 2, self.height() / 2)
        return QPointF(
            center.x() + dx_m * _PIXELS_PER_METER,
            center.y() - dy_m * _PIXELS_PER_METER,  # screen y grows downward
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#0d0d0d"))

        painter.setPen(_GRID_COLOR)
        for x in range(0, self.width(), _GRID_STEP_PX):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), _GRID_STEP_PX):
            painter.drawLine(0, y, self.width(), y)

        if self._origin is None:
            painter.setPen(_TEXT_COLOR)
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Waiting for GNSS fix...")
            return

        for lat, lon, label in self._pins:
            self._draw_pin(painter, lat, lon, label)

        if self._rover_pos is not None:
            self._draw_rover(painter, *self._rover_pos)

        if self._gnss_watcher.is_stale():
            painter.setPen(_ROVER_STALE_COLOR)
            painter.drawText(6, 14, "GNSS: STALE")

    def _draw_pin(self, painter: QPainter, lat: float, lon: float, label: str):
        pos = self._to_pixels(lat, lon)
        painter.setPen(_PIN_COLOR)
        painter.setBrush(_PIN_COLOR)
        painter.drawEllipse(pos, 4, 4)
        if label:
            painter.drawText(pos + QPointF(6, 4), label)

    def _draw_rover(self, painter: QPainter, lat: float, lon: float):
        pos = self._to_pixels(lat, lon)
        color = _ROVER_STALE_COLOR if self._gnss_watcher.is_stale() else _ROVER_COLOR

        painter.save()
        painter.translate(pos)
        painter.rotate(self._heading_deg)  # 0 = up/north, clockwise, per compass convention
        triangle = QPolygonF([QPointF(0, -9), QPointF(6, 7), QPointF(-6, 7)])
        painter.setPen(color)
        painter.setBrush(color)
        painter.drawPolygon(triangle)
        painter.restore()


class GnssMapWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self._canvas = _MapCanvas()
        layout.addWidget(self._canvas)

        entry_row = QHBoxLayout()

        self._lat_spin = QDoubleSpinBox()
        self._lat_spin.setRange(-90.0, 90.0)
        self._lat_spin.setDecimals(6)
        self._lat_spin.setPrefix("lat ")

        self._lon_spin = QDoubleSpinBox()
        self._lon_spin.setRange(-180.0, 180.0)
        self._lon_spin.setDecimals(6)
        self._lon_spin.setPrefix("lon ")

        self._add_pin_button = QPushButton("Add Pin")
        self._add_pin_button.clicked.connect(self._on_add_pin_clicked)

        entry_row.addWidget(self._lat_spin)
        entry_row.addWidget(self._lon_spin)
        entry_row.addWidget(self._add_pin_button)
        layout.addLayout(entry_row)

    def bind_data_source(self, data_source):
        data_source.signals.gnss_fix.connect(self._canvas.on_gnss_fix)
        data_source.signals.imu_update.connect(self._canvas.on_imu_update)

    def _on_add_pin_clicked(self):
        self._canvas.add_pin(self._lat_spin.value(), self._lon_spin.value())
