"""
Equipment Servicing checklist loader.

Loads equipment_servicing_checklist.json -- the manual/teleoperated
sub-tasks of the Equipment Servicing Mission (cache handling, the
lander panel/latch, the hose/valve/switches), grouped for display but
otherwise flat, plain checkboxes. Same "swap the JSON, nothing in the
GUI changes" shape as delivery_checklist_loader.py, just without any
points/scoring -- Equipment Servicing's rules don't publish a points
table the way Delivery's do, so this is a checklist, not a scoreboard.

The Autonomous Typing (launch key) and USB-card GNSS-read sub-tasks are
deliberately NOT in this checklist -- they're full launch/stop
sequences with their own status feedback (see EquipmentServicingWidget
/ EquipmentSequenceCard), not something a checkbox can represent.

Schema:
    {
      "groups": [{"id", "label"}, ...],
      "tasks": [{"id", "group", "label"}, ...]
    }
"""

import json
from pathlib import Path

_DEFAULT_PATH = Path(__file__).parent / "equipment_servicing_checklist.json"

_REQUIRED_GROUP_FIELDS = ("id", "label")
_REQUIRED_TASK_FIELDS = ("id", "group", "label")


def load_equipment_servicing_checklist(path: str | Path | None = None) -> dict:
    """Reads and validates the checklist JSON, returning
    {"groups": [...], "tasks": [...]} unchanged. Raises ValueError with
    a specific message on any malformed entry, rather than letting
    widget code fail obscurely on a missing field later."""
    path = Path(path) if path is not None else _DEFAULT_PATH
    with open(path) as f:
        data = json.load(f)

    groups = data.get("groups")
    tasks = data.get("tasks")
    if not isinstance(groups, list) or not isinstance(tasks, list):
        raise ValueError(f"{path}: expected top-level 'groups' and 'tasks' lists")

    group_ids = set()
    for group in groups:
        _require_fields(group, _REQUIRED_GROUP_FIELDS, f"{path}: group {group!r}")
        group_ids.add(group["id"])

    for task in tasks:
        _require_fields(task, _REQUIRED_TASK_FIELDS, f"{path}: task {task!r}")
        if task["group"] not in group_ids:
            raise ValueError(f"{path}: task {task['id']!r} references unknown group {task['group']!r}")

    return {"groups": groups, "tasks": tasks}


def _require_fields(obj: dict, fields: tuple, context: str):
    missing = [f for f in fields if f not in obj]
    if missing:
        raise ValueError(f"{context} missing required field(s): {missing}")


if __name__ == '__main__':
    checklist = load_equipment_servicing_checklist()
    print(f"groups: {len(checklist['groups'])}")
    for group in checklist["groups"]:
        print(" ", group)
    print(f"tasks: {len(checklist['tasks'])}")
    for task in checklist["tasks"]:
        print(" ", task)
