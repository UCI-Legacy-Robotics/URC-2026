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
"""

import functools
import http.server
import json
import threading
from pathlib import Path

from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QWidget, QVBoxLayout
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

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._view = QWebEngineView()
        self._view.load(QUrl(self._asset_server.base_url + "index.html"))
        layout.addWidget(self._view)

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

    def _run_js(self, function_name: str, *args):
        # json.dumps rather than manual string formatting/f-strings for
        # the arguments — handles quote/unicode escaping correctly (e.g.
        # a pin label containing a quote or backslash) and turns None
        # into JS's `null`, which app.js's falsy checks already expect.
        args_js = ", ".join(json.dumps(arg) for arg in args)
        self._view.page().runJavaScript(f"{function_name}({args_js});")
