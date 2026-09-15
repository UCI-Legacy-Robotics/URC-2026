"""
Equipment Servicing checklist widget.

Renders whatever's in equipment_servicing_checklist.json as a plain
completion checklist, grouped by the JSON's group order -- a QCheckBox
per task, a "done / total" tally per group and overall. Unlike
DeliveryChecklistWidget there is no scoring here at all: Equipment
Servicing's published rules don't hand out a points table, just a list
of sub-tasks that get done or don't, so this widget tracks completion
only.

Every frame/checkbox here sets its own explicit border/indicator style
rather than relying on the app-wide dark stylesheet, same reasoning as
delivery_checklist_widget.py -- a bare QFrame.StyledPanel and default
QCheckBox indicator both render with essentially no visible edge
against a fully dark theme otherwise.

Fully self-contained: no DataSource/bind_data_source, same as
DeliveryChecklistWidget -- every task here is physically performed by
an operator watching the arm/cache/panel, not telemetry.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton, QFrame

from equipment_servicing_checklist_loader import load_equipment_servicing_checklist

_SECTION_STYLE = (
    "QFrame#groupSection { border: 1px solid #444; border-radius: 6px; "
    "background: #141414; }"
)
_CHECKBOX_STYLE = (
    "QCheckBox { font-size: 15px; spacing: 8px; } "
    "QCheckBox::indicator { width: 22px; height: 22px; border: 1px solid #888; "
    "border-radius: 4px; background: #1a1a1a; } "
    "QCheckBox::indicator:hover { border: 1px solid #aaa; } "
    "QCheckBox::indicator:checked { background: #1b5e20; border: 1px solid #3ba33b; }"
)
_BUTTON_STYLE = (
    "QPushButton { font-size: 14px; padding: 6px; color: #e0e0e0; "
    "background: #1e1e1e; border: 1px solid #555; border-radius: 4px; } "
    "QPushButton:hover { background: #2a2a2a; border: 1px solid #777; } "
    "QPushButton:pressed { background: #333; }"
)


class EquipmentChecklistWidget(QWidget):

    def __init__(self, checklist_path=None, parent=None):
        super().__init__(parent)
        checklist = load_equipment_servicing_checklist(checklist_path)

        self._checkboxes = []       # [(QCheckBox, group_id), ...]
        self._group_sections = {}   # group_id -> {"tally_label", "checkbox_count"}

        layout = QVBoxLayout(self)

        tasks_by_group = {}
        for task in checklist["tasks"]:
            tasks_by_group.setdefault(task["group"], []).append(task)

        for group in checklist["groups"]:
            layout.addWidget(self._build_group_section(group, tasks_by_group.get(group["id"], [])))

        layout.addStretch()

        self._total_label = QLabel()
        self._total_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self._total_label)

        self._reset_button = QPushButton("Reset")
        self._reset_button.setStyleSheet(_BUTTON_STYLE)
        self._reset_button.clicked.connect(self._on_reset_clicked)
        layout.addWidget(self._reset_button)

        self._recompute_tallies()

    # -- section/row construction -----------------------------------------

    def _build_group_section(self, group: dict, tasks: list) -> QFrame:
        section = QFrame()
        section.setObjectName("groupSection")
        section.setFrameShape(QFrame.Shape.StyledPanel)
        section.setStyleSheet(_SECTION_STYLE)
        section_layout = QVBoxLayout(section)

        header = QLabel(group["label"])
        header.setStyleSheet("font-size: 16px; font-weight: bold; border: none;")
        section_layout.addWidget(header)

        for task in tasks:
            checkbox = QCheckBox(task["label"])
            checkbox.setStyleSheet(_CHECKBOX_STYLE)
            checkbox.stateChanged.connect(self._recompute_tallies)
            self._checkboxes.append((checkbox, group["id"]))
            section_layout.addWidget(checkbox)

        tally_label = QLabel()
        tally_label.setStyleSheet("font-size: 14px; border: none;")
        section_layout.addWidget(tally_label)

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
