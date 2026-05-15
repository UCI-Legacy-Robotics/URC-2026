import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl


class GnssWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.map_view = QWebEngineView()
        map_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'map.html')
        self.map_view.load(QUrl.fromLocalFile(os.path.abspath(map_path)))
        layout.addWidget(self.map_view)

    def on_gnss_fix(self, lat: float, lon: float):
        self.map_view.page().runJavaScript(f'updatePosition({lat}, {lon});')
