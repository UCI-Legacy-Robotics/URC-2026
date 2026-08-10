"""
GNSS map widget — sidebar, main area.

Renders the Leaflet map in assets/gnss_map/ (vendored locally — Leaflet,
its CSS, and the rotatedMarker plugin all live under
assets/gnss_map/vendor/, no CDN references) inside a QWebEngineView.

Assets are served over a tiny local HTTP server bound to 127.0.0.1 on an
OS-assigned port, rather than loaded via file://. QtWebEngine's file://
handling has enough quirks around relative asset resolution that a local
server sidesteps them cleanly — this is purely a loading mechanism, not
a live/CDN fetch: nothing here ever leaves 127.0.0.1, matching the "no
internet at the competition site" constraint.

Waypoint pins are added by manual coordinate entry only — no
click-to-place — per current design decision. Pin IDs are generated
here (a simple incrementing counter) and tracked in self._pins purely
so the pin list widget and Remove/Clear buttons have something to act
on; app.js's own `pins` dict is the actual source of truth for what's
drawn on the map.
"""

import functools
import http.server
import json
import threading
from pathlib import Path

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QDoubleSpinBox, QListWidget, QListWidgetItem
)
from PyQt6.QtWebEngineWidgets import QWebEngineView

_ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets" / "gnss_map"


class _AssetServer:
    """Serves _ASSETS_DIR over 127.0.0.1 on an OS-assigned ephemeral
    port, in a daemon thread. One instance per GnssMapWidget; no
    explicit teardown — the thread is a daemon, so it dies with the
    process, which matches this widget's actual lifetime (one persistent
    instance for the app's duration)."""

    def __init__(self, directory: Path):
        handler = functools.partial(
            http.server.SimpleHTTPRequestHandler, directory=str(directory)
        )
        # Binding port 0 lets the OS assign a free ephemeral port directly
        # (avoids the bind-then-close-then-rebind race of picking a port
        # ahead of time).
        self._httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.port = self._httpd.server_address[1]

        self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)
        self._thread.start()

    @property
    def base_url(self) -> str:
        return f"http://127.0.0.1:{self.port}/"


class GnssMapWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._asset_server = _AssetServer(_ASSETS_DIR)

        # gnss_fix and imu_update arrive as two independent streams —
        # heading comes from IMU, position from GNSS, and the rover
        # marker needs both together. Cache the latest of each and push
        # a combined update to JS whenever either one changes, rather
        # than waiting for both to update in lockstep (which they won't,
        # since they're on different timers/topics).
        self._last_lat = None
        self._last_lon = None
        self._last_heading_deg = 0.0

        # gnss_fix/imu_update can start arriving (via bind_data_source)
        # before the page has finished loading app.js — SimulationDataSource
        # in particular starts its timers immediately, well before the
        # localhost round-trip to fetch and parse the page completes. Calls
        # made before load finishes are queued here and flushed once ready,
        # instead of hitting "X is not defined" in the JS console and being
        # silently dropped.
        self._page_ready = False
        self._pending_js_calls = []

        # pin_id -> (lat, lon, label) — mirrors app.js's own `pins` dict
        # just enough for the list widget below to show what's placed and
        # for Remove/Clear to know what IDs to send back to JS.
        self._pins = {}
        self._next_pin_id = 1

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self._view = QWebEngineView()
        self._view.loadFinished.connect(self._on_load_finished)
        self._view.load(QUrl(self._asset_server.base_url + "index.html"))
        layout.addWidget(self._view)

        # -- manual waypoint pin entry (no click-to-place) -------------

        coord_row = QHBoxLayout()
        self._lat_spin = QDoubleSpinBox()
        self._lat_spin.setRange(-90.0, 90.0)
        self._lat_spin.setDecimals(6)
        self._lat_spin.setPrefix("lat ")
        self._lon_spin = QDoubleSpinBox()
        self._lon_spin.setRange(-180.0, 180.0)
        self._lon_spin.setDecimals(6)
        self._lon_spin.setPrefix("lon ")
        coord_row.addWidget(self._lat_spin)
        coord_row.addWidget(self._lon_spin)
        layout.addLayout(coord_row)

        label_row = QHBoxLayout()
        self._pin_label_edit = QLineEdit()
        self._pin_label_edit.setPlaceholderText("Label (optional)")
        self._add_pin_button = QPushButton("Add Pin")
        self._add_pin_button.clicked.connect(self._on_add_pin_clicked)
        label_row.addWidget(self._pin_label_edit)
        label_row.addWidget(self._add_pin_button)
        layout.addLayout(label_row)

        self._pin_list = QListWidget()
        self._pin_list.setMaximumHeight(80)
        layout.addWidget(self._pin_list)

        pin_controls_row = QHBoxLayout()
        self._remove_pin_button = QPushButton("Remove Selected")
        self._remove_pin_button.clicked.connect(self._on_remove_selected_pin_clicked)
        self._clear_pins_button = QPushButton("Clear All")
        self._clear_pins_button.clicked.connect(self._on_clear_pins_clicked)
        pin_controls_row.addWidget(self._remove_pin_button)
        pin_controls_row.addWidget(self._clear_pins_button)
        layout.addLayout(pin_controls_row)

    def bind_data_source(self, data_source):
        data_source.signals.gnss_fix.connect(self._on_gnss_fix)
        data_source.signals.imu_update.connect(self._on_imu_update)

    # -- public API, thin wrappers over the JS functions in app.js -----

    def set_rover_position(self, lat: float, lon: float, heading_degrees: float):
        self._run_js("setRoverPosition", lat, lon, heading_degrees)

    def set_rover_stale(self, is_stale: bool):
        self._run_js("setRoverStale", is_stale)

    def center_on_rover(self):
        self._run_js("centerOnRover")

    def add_pin(self, pin_id, lat: float, lon: float, label: str = None):
        self._run_js("addPin", pin_id, lat, lon, label)

    def remove_pin(self, pin_id):
        self._run_js("removePin", pin_id)

    def clear_pins(self):
        self._run_js("clearPins")

    def set_zoom(self, level: int):
        self._run_js("setZoom", level)

    def zoom_in(self):
        self._run_js("zoomIn")

    def zoom_out(self):
        self._run_js("zoomOut")

    # -- internal -------------------------------------------------------

    def _on_add_pin_clicked(self):
        lat = self._lat_spin.value()
        lon = self._lon_spin.value()
        label = self._pin_label_edit.text().strip() or None

        pin_id = str(self._next_pin_id)
        self._next_pin_id += 1
        self._pins[pin_id] = (lat, lon, label)
        self.add_pin(pin_id, lat, lon, label)

        item_text = f"{lat:.6f}, {lon:.6f}"
        if label:
            item_text += f" — {label}"
        item = QListWidgetItem(item_text)
        item.setData(Qt.ItemDataRole.UserRole, pin_id)
        self._pin_list.addItem(item)

        self._pin_label_edit.clear()

    def _on_remove_selected_pin_clicked(self):
        item = self._pin_list.currentItem()
        if item is None:
            return
        pin_id = item.data(Qt.ItemDataRole.UserRole)
        self.remove_pin(pin_id)
        self._pins.pop(pin_id, None)
        self._pin_list.takeItem(self._pin_list.row(item))

    def _on_clear_pins_clicked(self):
        self.clear_pins()
        self._pins.clear()
        self._pin_list.clear()

    def _on_gnss_fix(self, lat: float, lon: float):
        self._last_lat = lat
        self._last_lon = lon
        self._push_rover_position()

    def _on_imu_update(self, imu):
        self._last_heading_deg = imu.yaw_deg
        self._push_rover_position()

    def _push_rover_position(self):
        if self._last_lat is None or self._last_lon is None:
            return  # no GNSS fix yet — nothing to place on the map
        self.set_rover_position(self._last_lat, self._last_lon, self._last_heading_deg)

    def _on_load_finished(self, ok: bool):
        if not ok:
            return
        self._page_ready = True
        for js in self._pending_js_calls:
            self._view.page().runJavaScript(js)
        self._pending_js_calls.clear()

    def _run_js(self, function_name: str, *args):
        # json.dumps rather than manual string formatting/f-strings for
        # the arguments — handles quote/unicode escaping correctly (e.g.
        # a pin label containing a quote or backslash) and turns None
        # into JS's `null`, which app.js's falsy checks already expect.
        args_js = ", ".join(json.dumps(arg) for arg in args)
        js = f"{function_name}({args_js});"
        if self._page_ready:
            self._view.page().runJavaScript(js)
        else:
            self._pending_js_calls.append(js)
