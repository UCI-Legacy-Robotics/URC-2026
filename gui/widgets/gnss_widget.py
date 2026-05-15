import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QColor
from PyQt6.QtCore import QUrl, Qt


class GnssWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('background: #0a0a0a;')

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.map_view = QWebEngineView()
        self.map_view.page().setBackgroundColor(QColor(10, 10, 10))

        map_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'map.html')
        self.map_view.load(QUrl.fromLocalFile(os.path.abspath(map_path)))

        self._placeholder = QLabel('Waiting for GNSS fix...')
        self._placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._placeholder.setStyleSheet(
            'background: #0a0a0a; color: #333; font-size: 13px; font-family: monospace;'
        )

        layout.addWidget(self.map_view)
        layout.addWidget(self._placeholder)

        self.map_view.hide()

    def on_gnss_fix(self, lat: float, lon: float):
        if not self.map_view.isVisible():
            self._placeholder.hide()
            self.map_view.show()
        self.map_view.page().runJavaScript(f'updatePosition({lat}, {lon});')
