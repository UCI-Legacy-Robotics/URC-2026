import math
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt6.QtCore import Qt, QPointF


_METERS_PER_DEG = 111_320.0
_PADDING = 40          # px margin inside the widget
_DOT_R = 5             # rover marker radius


def _to_meters(lat0: float, lon0: float, lat: float, lon: float) -> tuple[float, float]:
    """Equirectangular projection: returns (dx_m, dy_m) from origin."""
    cos0 = math.cos(math.radians(lat0))
    dx = (lon - lon0) * cos0 * _METERS_PER_DEG
    dy = (lat - lat0) * _METERS_PER_DEG
    return dx, dy


class GnssWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(750, 750)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet('GnssWidget { background-color: #1a1a1a; border-radius: 6px; }')

        self._track: list[tuple[float, float]] = []   # (lat, lon) history
        self._current: tuple[float, float] | None = None

        self._placeholder = QLabel('Waiting for GNSS fix...')
        self._placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._placeholder.setStyleSheet(
            'background: transparent; color: #555; font-size: 13px; font-family: monospace;'
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._placeholder)

    def on_gnss_fix(self, lat: float, lon: float):
        if self._placeholder.isVisible():
            self._placeholder.hide()
        self._track.append((lat, lon))
        self._current = (lat, lon)
        self.update()

    # ------------------------------------------------------------------
    def paintEvent(self, _event):
        if not self._track:
            super().paintEvent(_event)
            return

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        draw_w = w - 2 * _PADDING
        draw_h = h - 2 * _PADDING

        lat0, lon0 = self._track[0]
        pts_m = [_to_meters(lat0, lon0, la, lo) for la, lo in self._track]

        xs = [x for x, _ in pts_m]
        ys = [y for _, y in pts_m]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        span_x = max(max_x - min_x, 1.0)
        span_y = max(max_y - min_y, 1.0)
        scale = min(draw_w / span_x, draw_h / span_y)

        def to_screen(mx: float, my: float) -> QPointF:
            sx = _PADDING + (mx - min_x) * scale
            sy = h - _PADDING - (my - min_y) * scale   # flip Y (north = up)
            return QPointF(sx, sy)

        # Track line
        if len(pts_m) > 1:
            pen = QPen(QColor('#4a90d9'), 2)
            p.setPen(pen)
            for i in range(1, len(pts_m)):
                p.drawLine(to_screen(*pts_m[i - 1]), to_screen(*pts_m[i]))

        # Origin marker
        origin = to_screen(0.0, 0.0)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(QColor('#555')))
        p.drawEllipse(origin, _DOT_R, _DOT_R)

        # Current position
        cur = to_screen(*pts_m[-1])
        p.setBrush(QBrush(QColor('#e05c5c')))
        p.drawEllipse(cur, _DOT_R + 1, _DOT_R + 1)

        # Coordinate overlay
        lat, lon = self._current
        dist_m = math.hypot(*pts_m[-1])
        label = f'Lat {lat:.6f}  Lon {lon:.6f}   Δ {dist_m:.1f} m from start'
        p.setPen(QPen(QColor('#aaa')))
        p.setFont(QFont('monospace', 10))
        p.drawText(8, h - 8, label)

        p.end()
