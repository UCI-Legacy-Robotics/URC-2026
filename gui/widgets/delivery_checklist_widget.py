"""
Delivery Checklist widget.

Renders whatever's in delivery_checklist.json as a live scoring
checklist -- a fixed-point QCheckBox per "checkbox" task, or a
QSpinBox per option (each option its own points-per-unit rate) plus a
QProgressBar capped at total_points per "counter" task (see
delivery_checklist_loader.py for the schema). Nothing here is specific
to any one year's rules -- swap the JSON file for a new season.

Fully self-contained: no DataSource/bind_data_source, since Delivery is
almost entirely teleoperated and this widget is just a running tally of
completed tasks, not telemetry.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QSpinBox,
    QProgressBar, QPushButton, QFrame
)

from delivery_checklist_loader import load_delivery_checklist


class DeliveryChecklistWidget(QWidget):

    def __init__(self, checklist_path=None, parent=None):
        super().__init__(parent)
        checklist = load_delivery_checklist(checklist_path)

        self._checkboxes = []   # [(QCheckBox, points), ...]
        self._counter_tasks = []  # [{"total_points", "option_widgets": [(QSpinBox, points), ...], "progress_bar"}, ...]

        layout = QVBoxLayout(self)

        for task in checklist["tasks"]:
            if task["type"] == "checkbox":
                layout.addWidget(self._build_checkbox_row(task))
            elif task["type"] == "counter":
                layout.addWidget(self._build_counter_row(task))

        layout.addStretch()

        self._total_label = QLabel()
        self._total_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self._total_label)

        self._reset_button = QPushButton("Reset")
        self._reset_button.clicked.connect(self._on_reset_clicked)
        layout.addWidget(self._reset_button)

        self._recompute_total()

    # -- row construction ---------------------------------------------------

    def _build_checkbox_row(self, task: dict) -> QCheckBox:
        checkbox = QCheckBox(f"{task['label']} (+{task['points']} pts)")
        checkbox.stateChanged.connect(self._recompute_total)
        self._checkboxes.append((checkbox, task["points"]))
        return checkbox

    def _build_counter_row(self, task: dict) -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame_layout = QVBoxLayout(frame)

        title = QLabel(task["label"])
        frame_layout.addWidget(title)

        option_widgets = []
        for option in task["options"]:
            option_row = QHBoxLayout()
            option_row.addWidget(QLabel(f"{option['label']} ({option['points']} pts)"))
            spin = QSpinBox()
            spin.setRange(0, 999)
            spin.valueChanged.connect(self._recompute_total)
            option_row.addWidget(spin)
            frame_layout.addLayout(option_row)
            option_widgets.append((spin, option["points"]))

        progress_bar = QProgressBar()
        progress_bar.setRange(0, task["total_points"])
        progress_bar.setFormat("%v / %m pts")
        frame_layout.addWidget(progress_bar)

        self._counter_tasks.append({
            "total_points": task["total_points"],
            "option_widgets": option_widgets,
            "progress_bar": progress_bar,
        })
        return frame

    # -- scoring --------------------------------------------------------

    def _recompute_total(self, *_args):
        total = 0

        for checkbox, points in self._checkboxes:
            if checkbox.isChecked():
                total += points

        for counter in self._counter_tasks:
            raw = sum(spin.value() * points for spin, points in counter["option_widgets"])
            capped = min(raw, counter["total_points"])
            counter["progress_bar"].setValue(capped)
            total += capped

        self._total_label.setText(f"Total: {total} pts")

    def _on_reset_clicked(self):
        for checkbox, _ in self._checkboxes:
            checkbox.setChecked(False)
        for counter in self._counter_tasks:
            for spin, _ in counter["option_widgets"]:
                spin.setValue(0)
        self._recompute_total()
