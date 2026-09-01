"""
Delivery Checklist widget.

Renders whatever's in delivery_checklist.json as a live scoring
checklist, grouped by stage (in the JSON's stage order) -- a
fixed-point QCheckBox per "checkbox" task, or a QSpinBox per option
(each option its own points-per-unit rate) plus a QProgressBar capped
at total_points per "counter" task (see delivery_checklist_loader.py
for the schema). Nothing here is specific to any one year's rules --
swap the JSON file for a new season.

Each stage gets its own subtotal, and -- if the stage's JSON entry has
an unlock_threshold -- a LOCKED/UNLOCKED badge (reusing ColorCodedLabel,
same status-badge idiom as SubsystemLaunchWidget etc.) showing progress
toward it, e.g. 2026's "clear Stage 1 to unlock Stage 2 at 40 pts".
Purely a display computed from the stage's own subtotal -- no state of
its own, no cross-stage logic.

Fully self-contained: no DataSource/bind_data_source, since Delivery is
almost entirely teleoperated and this widget is just a running tally of
completed tasks, not telemetry.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QSpinBox,
    QProgressBar, QPushButton, QFrame
)

from delivery_checklist_loader import load_delivery_checklist
from widgets.color_coded_label import ColorCodedLabel

_LOCKED_COLOR = "#3a3a3a"
_UNLOCKED_COLOR = "#1b5e20"


class DeliveryChecklistWidget(QWidget):

    def __init__(self, checklist_path=None, parent=None):
        super().__init__(parent)
        checklist = load_delivery_checklist(checklist_path)

        self._checkboxes = []     # [(QCheckBox, points, stage_id), ...]
        self._counter_tasks = []  # [{"stage_id", "total_points", "option_widgets": [(QSpinBox, points), ...], "progress_bar"}, ...]
        self._stage_sections = {}  # stage_id -> {"subtotal_label", "unlock_threshold", "threshold_badge"}

        layout = QVBoxLayout(self)

        tasks_by_stage = {}
        for task in checklist["tasks"]:
            tasks_by_stage.setdefault(task["stage"], []).append(task)

        for stage in checklist["stages"]:
            layout.addWidget(self._build_stage_section(stage, tasks_by_stage.get(stage["id"], [])))

        layout.addStretch()

        self._total_label = QLabel()
        self._total_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self._total_label)

        self._reset_button = QPushButton("Reset")
        self._reset_button.clicked.connect(self._on_reset_clicked)
        layout.addWidget(self._reset_button)

        self._recompute_total()

    # -- section/row construction -----------------------------------------

    def _build_stage_section(self, stage: dict, tasks: list) -> QFrame:
        section = QFrame()
        section.setFrameShape(QFrame.Shape.StyledPanel)
        section_layout = QVBoxLayout(section)

        header = QLabel(stage["label"])
        header.setStyleSheet("font-size: 14px; font-weight: bold;")
        section_layout.addWidget(header)

        for task in tasks:
            if task["type"] == "checkbox":
                section_layout.addWidget(self._build_checkbox_row(task))
            elif task["type"] == "counter":
                section_layout.addWidget(self._build_counter_row(task))

        subtotal_label = QLabel()
        section_layout.addWidget(subtotal_label)

        unlock_threshold = stage.get("unlock_threshold")
        threshold_badge = None
        if unlock_threshold is not None:
            threshold_badge = ColorCodedLabel()
            section_layout.addWidget(threshold_badge)

        self._stage_sections[stage["id"]] = {
            "subtotal_label": subtotal_label,
            "unlock_threshold": unlock_threshold,
            "threshold_badge": threshold_badge,
        }
        return section

    def _build_checkbox_row(self, task: dict) -> QCheckBox:
        checkbox = QCheckBox(f"{task['label']} (+{task['points']} pts)")
        checkbox.stateChanged.connect(self._recompute_total)
        self._checkboxes.append((checkbox, task["points"], task["stage"]))
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
            "stage_id": task["stage"],
            "total_points": task["total_points"],
            "option_widgets": option_widgets,
            "progress_bar": progress_bar,
        })
        return frame

    # -- scoring --------------------------------------------------------

    def _recompute_total(self, *_args):
        stage_totals = {stage_id: 0 for stage_id in self._stage_sections}
        total = 0

        for checkbox, points, stage_id in self._checkboxes:
            if checkbox.isChecked():
                stage_totals[stage_id] += points
                total += points

        for counter in self._counter_tasks:
            raw = sum(spin.value() * points for spin, points in counter["option_widgets"])
            capped = min(raw, counter["total_points"])
            counter["progress_bar"].setValue(capped)
            stage_totals[counter["stage_id"]] += capped
            total += capped

        for stage_id, section in self._stage_sections.items():
            subtotal = stage_totals[stage_id]
            section["subtotal_label"].setText(f"Stage subtotal: {subtotal} pts")

            threshold = section["unlock_threshold"]
            if threshold is not None:
                unlocked = subtotal >= threshold
                status = "UNLOCKED" if unlocked else "LOCKED"
                color = _UNLOCKED_COLOR if unlocked else _LOCKED_COLOR
                section["threshold_badge"].set_state(f"{subtotal} / {threshold} pts — {status}", color)

        self._total_label.setText(f"Total: {total} pts")

    def _on_reset_clicked(self):
        for checkbox, _, _ in self._checkboxes:
            checkbox.setChecked(False)
        for counter in self._counter_tasks:
            for spin, _ in counter["option_widgets"]:
                spin.setValue(0)
        self._recompute_total()
