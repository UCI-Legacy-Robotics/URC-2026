"""
Grouped checklist widget.

Renders whatever's in a checklist JSON (see checklist_loader.py) as a
plain completion checklist, grouped by the JSON's group order -- a
QCheckBox per task, a "done / total" tally per group and overall.
Unlike DeliveryChecklistWidget there is no scoring here at all: not
every mission's published rules hand out a points table -- some are
just a list of sub-tasks that get done or don't, so this widget tracks
completion only. Generic over which mission's checklist it's showing
(configured entirely by checklist_path), the same "one widget class,
one JSON per instance" shape as ScienceSequenceWidget/CameraFeedWidget
use -- both Equipment Servicing and Autonomous Nav use this unchanged,
just pointed at their own JSON file.

Fully self-contained: no DataSource/bind_data_source, same as
DeliveryChecklistWidget -- every task here is physically performed or
externally verified by an operator, not telemetry.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import CaptionLabel, CheckBox, PushButton, SubtitleLabel

from ui import theme
from storage.checklist_loader import load_checklist
from widgets.shared.controls import SectionCard


class ChecklistWidget(QWidget):

    def __init__(self, checklist_path, parent=None):
        super().__init__(parent)
        checklist = load_checklist(checklist_path)

        self._checkboxes = []       # [(QCheckBox, group_id), ...]
        self._group_sections = {}   # group_id -> {"tally_label", "checkbox_count"}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        tasks_by_group = {}
        for task in checklist["tasks"]:
            tasks_by_group.setdefault(task["group"], []).append(task)

        for group in checklist["groups"]:
            layout.addWidget(self._build_group_section(group, tasks_by_group.get(group["id"], [])))

        layout.addStretch()

        footer = QHBoxLayout()
        self._total_label = SubtitleLabel()
        footer.addWidget(self._total_label, 1)
        self._reset_button = PushButton(theme.icon("mdi6.restart"), "Reset")
        self._reset_button.clicked.connect(self._on_reset_clicked)
        footer.addWidget(self._reset_button)
        layout.addLayout(footer)

        self._recompute_tallies()

    # -- section/row construction -----------------------------------------

    def _build_group_section(self, group: dict, tasks: list) -> SectionCard:
        section = SectionCard(group["label"], "mdi6.format-list-checks")

        for task in tasks:
            checkbox = CheckBox(task["label"])
            checkbox.stateChanged.connect(self._recompute_tallies)
            self._checkboxes.append((checkbox, group["id"]))
            section.body.addWidget(checkbox)

        tally_label = CaptionLabel()
        section.body.addWidget(tally_label)

        self._group_sections[group["id"]] = {
            "tally_label": tally_label,
            "checkbox_count": len(tasks),
        }
        return section

    # -- tallying -----------------------------------------------------------

    def _recompute_tallies(self, *_args):
        group_done = {group_id: 0 for group_id in self._group_sections}
        total_done = 0

        for checkbox, group_id in self._checkboxes:
            if checkbox.isChecked():
                group_done[group_id] += 1
                total_done += 1

        for group_id, section in self._group_sections.items():
            section["tally_label"].setText(
                f"{group_done[group_id]} / {section['checkbox_count']} complete"
            )

        self._total_label.setText(f"Total: {total_done} / {len(self._checkboxes)} complete")

    def _on_reset_clicked(self):
        for checkbox, _ in self._checkboxes:
            checkbox.setChecked(False)
        self._recompute_tallies()
