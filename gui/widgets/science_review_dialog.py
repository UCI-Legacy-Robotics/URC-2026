"""
Science Review dialog.

Modal for showing judges a past site's full record -- everything
ScienceDataStore saved for that site (status log, GNSS fixes, readings,
images) in one place, reopenable at any time rather than only visible
live as it streamed in. Same "list on the left, detail panel on the
right" idiom as gnss_map_widget.py's _PinManagerDialog.

Read-only: this dialog never writes back to the store, it only reads
via list_sites()/load_site().
"""

from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QTextEdit, QLabel, QScrollArea, QWidget
)

from science_data_store import ScienceDataStore

_THUMB_SIZE = 120


def _format_timestamp(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")


def _format_event(event: dict) -> str:
    ts = _format_timestamp(event["timestamp"])
    kind = event["type"]
    sequence = event["sequence"]

    if kind == "status":
        line = f"[{ts}] {sequence} — {event['status']}"
        if event.get("message"):
            line += f": {event['message']}"
        return line
    if kind == "gnss":
        return f"[{ts}] {sequence} — GNSS {event['lat']:.6f}, {event['lon']:.6f}"
    if kind == "image":
        return f"[{ts}] {sequence} — image saved ({event['path'].name})"
    if kind == "reading":
        reading = "  ".join(f"{k}: {v}" for k, v in event["reading"].items())
        return f"[{ts}] {sequence} — reading: {reading}"
    return f"[{ts}] {sequence} — {kind}"


class ScienceReviewDialog(QDialog):

    def __init__(self, store: ScienceDataStore, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Review Sites")
        self.resize(700, 450)

        self._store = store
        self._store.sites_changed.connect(self._refresh_site_list)

        layout = QHBoxLayout(self)

        self._site_list = QListWidget()
        self._site_list.setMaximumWidth(220)
        self._site_list.currentItemChanged.connect(self._on_site_selected)
        layout.addWidget(self._site_list)

        detail_layout = QVBoxLayout()

        self._detail_title = QLabel("Select a site")
        self._detail_title.setStyleSheet("font-size: 14px; font-weight: bold;")
        detail_layout.addWidget(self._detail_title)

        self._event_log = QTextEdit()
        self._event_log.setReadOnly(True)
        detail_layout.addWidget(self._event_log, 1)

        self._image_scroll = QScrollArea()
        self._image_scroll.setWidgetResizable(True)
        self._image_scroll.setFixedHeight(_THUMB_SIZE + 20)
        self._image_row = QWidget()
        self._image_row_layout = QHBoxLayout(self._image_row)
        self._image_row_layout.setContentsMargins(4, 4, 4, 4)
        self._image_scroll.setWidget(self._image_row)
        detail_layout.addWidget(self._image_scroll)

        layout.addLayout(detail_layout, 1)

        self._refresh_site_list()

    # -- internal ---------------------------------------------------------

    def _refresh_site_list(self):
        selected_slug = self._current_slug()

        self._site_list.clear()
        for site in self._store.list_sites():
            item = QListWidgetItem(f"{site['label']}  ({site['event_count']} events)")
            item.setData(Qt.ItemDataRole.UserRole, site["slug"])
            self._site_list.addItem(item)
            if site["slug"] == selected_slug:
                self._site_list.setCurrentItem(item)

    def _current_slug(self) -> str | None:
        item = self._site_list.currentItem()
        return item.data(Qt.ItemDataRole.UserRole) if item is not None else None

    def _on_site_selected(self, current: QListWidgetItem, previous: QListWidgetItem):
        while self._image_row_layout.count():
            child = self._image_row_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if current is None:
            self._detail_title.setText("Select a site")
            self._event_log.clear()
            return

        slug = current.data(Qt.ItemDataRole.UserRole)
        site = self._store.load_site(slug)

        self._detail_title.setText(site["label"])
        self._event_log.setPlainText(
            "\n".join(_format_event(event) for event in site["events"])
        )

        for event in site["events"]:
            if event["type"] != "image":
                continue
            pixmap = QPixmap(str(event["path"])).scaled(
                _THUMB_SIZE, _THUMB_SIZE,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            thumb = QLabel()
            thumb.setPixmap(pixmap)
            thumb.setToolTip(event["sequence"])
            self._image_row_layout.addWidget(thumb)
        self._image_row_layout.addStretch()
