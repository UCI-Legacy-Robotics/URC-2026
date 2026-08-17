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
click-to-place — per current design decision, via a modal
(_PinManagerDialog below) rather than inline controls, to keep the
always-visible map as large as possible in the cramped sidebar. Pin IDs
are generated in the dialog (a simple incrementing counter) and tracked
there purely so its list widget and Remove/Clear buttons have something
to act on; app.js's own `pins` dict is the actual source of truth for
what's drawn on the map, and pins persist on the map after the dialog
closes since they live on GnssMapWidget, not the dialog.
"""

import functools
import http.server
import json
import threading
from pathlib import Path

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QDialog, QLineEdit, QPushButton,
    QDoubleSpinBox, QListWidget, QListWidgetItem
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage

from stale_data import StaleDataWatcher

_ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets" / "gnss_map"

# How long without a GNSS fix before the rover marker dims. Placeholder —
# real threshold TBD with systems/electrical, same as elsewhere in the app.
_GNSS_STALE_TIMEOUT_MS = 5000


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


class _LockedWebEnginePage(QWebEnginePage):
    """Blocks all navigation except within our own local map page.

    The competition site has no internet, so any link inside the page
    (Leaflet/OSM attribution, or anything else that ends up in there
    later) navigating away would strand the operator on a dead/blank
    page with no way back short of restarting the app. This is on top
    of removing the attribution control in app.js — that fixes the
    specific link, this is the general safety net for any navigation
    attempt, from anywhere in the page.
    """

    def __init__(self, allowed_url_prefix: str, parent=None):
        super().__init__(parent)
        self._allowed_url_prefix = allowed_url_prefix

    def acceptNavigationRequest(self, url, nav_type, is_main_frame):
        return url.toString().startswith(self._allowed_url_prefix)


class _PinManagerDialog(QDialog):
    """Modal for adding/removing/clearing manually-entered waypoint pins.

    Operates on the GnssMapWidget passed in — pins are drawn on the map
    itself (owned by the widget, not this dialog), so they persist after
    this dialog is closed rather than disappearing with it.
    """

    def __init__(self, map_widget: "GnssMapWidget", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Waypoints")

        self._map_widget = map_widget

        # pin_id -> (lat, lon, label) — mirrors app.js's own `pins` dict
        # just enough for the list widget below to show what's placed and
        # for Remove/Clear to know what IDs to send back to JS.
        self._pins = {}
        self._next_pin_id = 1

        layout = QVBoxLayout(self)

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
        layout.addWidget(self._pin_list)

        pin_controls_row = QHBoxLayout()
        self._remove_pin_button = QPushButton("Remove Selected")
        self._remove_pin_button.clicked.connect(self._on_remove_selected_pin_clicked)
        self._clear_pins_button = QPushButton("Clear All")
        self._clear_pins_button.clicked.connect(self._on_clear_pins_clicked)
        pin_controls_row.addWidget(self._remove_pin_button)
        pin_controls_row.addWidget(self._clear_pins_button)
        layout.addLayout(pin_controls_row)

    def _on_add_pin_clicked(self):
        lat = self._lat_spin.value()
        lon = self._lon_spin.value()
        label = self._pin_label_edit.text().strip() or None

        pin_id = str(self._next_pin_id)
        self._next_pin_id += 1
        self._pins[pin_id] = (lat, lon, label)
        self._map_widget.add_pin(pin_id, lat, lon, label)

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
        self._map_widget.remove_pin(pin_id)
        self._pins.pop(pin_id, None)
        self._pin_list.takeItem(self._pin_list.row(item))

    def _on_clear_pins_clicked(self):
        self._map_widget.clear_pins()
        self._pins.clear()
        self._pin_list.clear()


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

        # Degrades visibly per the top-level ground rule: if gnss_fix goes
        # quiet, the marker should visibly dim rather than just freezing at
        # its last position with no indication the feed died.
        self._gnss_watcher = StaleDataWatcher(_GNSS_STALE_TIMEOUT_MS, parent=self)
        self._gnss_watcher.became_stale.connect(lambda: self.set_rover_stale(True))
        self._gnss_watcher.became_fresh.connect(lambda: self.set_rover_stale(False))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self._view = QWebEngineView()
        self._view.setPage(_LockedWebEnginePage(self._asset_server.base_url, self._view))
        self._view.loadFinished.connect(self._on_load_finished)
        self._view.load(QUrl(self._asset_server.base_url + "index.html"))
        layout.addWidget(self._view)

        button_row = QHBoxLayout()

        self._center_on_rover_button = QPushButton("Center on Rover")
        self._center_on_rover_button.clicked.connect(self.center_on_rover)
        button_row.addWidget(self._center_on_rover_button)

        self._manage_pins_button = QPushButton("Manage Waypoints...")
        self._manage_pins_button.clicked.connect(self._on_manage_pins_clicked)
        button_row.addWidget(self._manage_pins_button)

        layout.addLayout(button_row)

        self._pin_dialog = _PinManagerDialog(self, parent=self)

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

    def _on_manage_pins_clicked(self):
        self._pin_dialog.exec()

    def _on_gnss_fix(self, lat: float, lon: float):
        self._last_lat = lat
        self._last_lon = lon
        self._gnss_watcher.notify()
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
