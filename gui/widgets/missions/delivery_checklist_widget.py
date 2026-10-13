"""
Delivery Checklist widget.

Renders whatever's in delivery_checklist.json as a live scoring
checklist, grouped by stage (in the JSON's stage order) -- a
fixed-point QCheckBox per "checkbox" task, or a _PlusMinusCounter per
option (each option its own points-per-unit rate) plus a QProgressBar
capped at total_points per "counter" task (see
delivery_checklist_loader.py for the schema). Nothing here is specific
to any one year's rules -- swap the JSON file for a new season.

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

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QProgressBar
from qfluentwidgets import (
    BodyLabel, CaptionLabel, CardWidget, CheckBox, PushButton, StrongBodyLabel,
    SubtitleLabel, ToolButton
)

from ui import theme
from storage.delivery_checklist_loader import load_delivery_checklist
from widgets.shared.color_coded_label import ColorCodedLabel
from widgets.shared.controls import SectionCard

_LOCKED_COLOR = theme.NEUTRAL
_UNLOCKED_COLOR = theme.GREEN


class _PlusMinusCounter(QWidget):
    """Minus button / value / plus button, standing in for a QSpinBox --
    same value()/set_value()/valueChanged surface a caller needs, just
    without a text-entry field (nothing here needs typed input, only
    incrementing a per-piece count)."""

    valueChanged = pyqtSignal(int)

    def __init__(self, minimum: int = 0, maximum: int = 999, parent=None):
        super().__init__(parent)
        self._minimum = minimum
        self._maximum = maximum
        self._value = minimum

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self._minus_button = ToolButton(theme.icon("mdi6.minus"))
        self._minus_button.setFixedSize(34, 34)
        self._minus_button.clicked.connect(lambda: self.set_value(self._value - 1))

        self._value_label = StrongBodyLabel(str(self._value))
        self._value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._value_label.setFixedWidth(32)

        self._plus_button = ToolButton(theme.icon("mdi6.plus"))
        self._plus_button.setFixedSize(34, 34)
        self._plus_button.clicked.connect(lambda: self.set_value(self._value + 1))

        layout.addWidget(self._minus_button)
        layout.addWidget(self._value_label)
        layout.addWidget(self._plus_button)

    def value(self) -> int:
        return self._value

    def set_value(self, value: int):
        value = max(self._minimum, min(self._maximum, value))
        if value == self._value:
            return
        self._value = value
        self._value_label.setText(str(value))
        self.valueChanged.emit(value)


class DeliveryChecklistWidget(QWidget):

    def __init__(self, checklist_path=None, parent=None):
        super().__init__(parent)
        checklist = load_delivery_checklist(checklist_path)

        self._checkboxes = []     # [(QCheckBox, points, stage_id), ...]
        self._counter_tasks = []  # [{"stage_id", "total_points", "option_widgets": [(_PlusMinusCounter, points), ...], "progress_bar"}, ...]
        self._stage_sections = {}  # stage_id -> {"subtotal_label", "unlock_threshold", "threshold_badge"}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(8)

        tasks_by_stage = {}
        for task in checklist["tasks"]:
            tasks_by_stage.setdefault(task["stage"], []).append(task)

        for stage in checklist["stages"]:
            layout.addWidget(self._build_stage_section(stage, tasks_by_stage.get(stage["id"], [])))

        layout.addStretch()

        footer = QHBoxLayout()
        self._total_label = SubtitleLabel()
        footer.addWidget(self._total_label, 1)
        self._reset_button = PushButton(theme.icon("mdi6.restart"), "Reset")
        self._reset_button.clicked.connect(self._on_reset_clicked)
        footer.addWidget(self._reset_button)
        layout.addLayout(footer)

        self._recompute_total()

    # -- section/row construction -----------------------------------------

    def _build_stage_section(self, stage: dict, tasks: list) -> SectionCard:
        section = SectionCard(stage["label"], "mdi6.package-variant-closed")
        section_layout = section.body

        for task in tasks:
            if task["type"] == "checkbox":
                section_layout.addWidget(self._build_checkbox_row(task))
            elif task["type"] == "counter":
                section_layout.addWidget(self._build_counter_row(task))

        subtotal_label = CaptionLabel()
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

    def _build_checkbox_row(self, task: dict) -> CheckBox:
        checkbox = CheckBox(f"{task['label']} (+{task['points']} pts)")
        checkbox.stateChanged.connect(self._recompute_total)
        self._checkboxes.append((checkbox, task["points"], task["stage"]))
        return checkbox

    def _build_counter_row(self, task: dict) -> CardWidget:
        frame = CardWidget()
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(10, 8, 10, 8)

        frame_layout.addWidget(StrongBodyLabel(task["label"]))

        option_widgets = []
        for option in task["options"]:
            option_row = QHBoxLayout()
            option_row.addWidget(BodyLabel(f"{option['label']} ({option['points']} pts)"))
            option_row.addStretch()

            counter = _PlusMinusCounter()
            counter.valueChanged.connect(self._recompute_total)
            option_row.addWidget(counter)
            frame_layout.addLayout(option_row)
            option_widgets.append((counter, option["points"]))

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
            raw = sum(widget.value() * points for widget, points in counter["option_widgets"])
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
            for widget, _ in counter["option_widgets"]:
                widget.set_value(0)
        self._recompute_total()
