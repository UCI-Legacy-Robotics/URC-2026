"""
MainWindow -- builds one RollingPlotWidget per graphs_config.json entry,
laid out in a grid inside a scroll area (19 tiles won't all fit on one
screen at once), plus a Pause All/Resume All toolbar.
"""

import math

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QScrollArea,
)

from ui.rolling_plot_widget import RollingPlotWidget


class MainWindow(QWidget):
    def __init__(self, config: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tuning Dashboard")

        self._widgets = {}  # graph_id -> RollingPlotWidget

        pause_all_button = QPushButton("Pause All")
        pause_all_button.clicked.connect(self.pause_all)
        resume_all_button = QPushButton("Resume All")
        resume_all_button.clicked.connect(self.resume_all)

        toolbar = QHBoxLayout()
        toolbar.addWidget(pause_all_button)
        toolbar.addWidget(resume_all_button)
        toolbar.addStretch()

        grid_container = QWidget()
        grid = QGridLayout(grid_container)
        columns = max(1, math.ceil(math.sqrt(len(config["graphs"]))))
        for i, graph in enumerate(config["graphs"]):
            widget = RollingPlotWidget(graph["title"], graph["units"], graph["window_seconds"])
            self._widgets[graph["id"]] = widget
            grid.addWidget(widget, i // columns, i % columns)

        scroll_area = QScrollArea()
        scroll_area.setWidget(grid_container)
        scroll_area.setWidgetResizable(True)

        layout = QVBoxLayout(self)
        layout.addLayout(toolbar)
        layout.addWidget(scroll_area)

    def on_sample(self, graph_id: str, t_relative: float, value: float):
        widget = self._widgets.get(graph_id)
        if widget is not None:
            widget.add_sample(t_relative, value)

    def pause_all(self):
        for widget in self._widgets.values():
            widget.set_paused(True)

    def resume_all(self):
        for widget in self._widgets.values():
            widget.set_paused(False)
