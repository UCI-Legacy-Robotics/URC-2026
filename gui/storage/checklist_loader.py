"""
Grouped-checklist loader.

Loads a plain completion checklist JSON -- grouped for display, plain
checkboxes, no points/scoring. Shared by any mission whose published
rules are just a list of sub-tasks rather than a points table (unlike
Delivery, which does score -- see delivery_checklist_loader.py for
that separate, points-bearing schema): Equipment Servicing
(equipment_servicing_checklist.json) and Autonomous Nav
(autonomous_nav_checklist.json) both use this same shape today.

Schema:
    {
      "groups": [{"id", "label"}, ...],
      "tasks": [{"id", "group", "label"}, ...]
    }
"""

import json
from pathlib import Path

from core.paths import CHECKLISTS_DIR


_REQUIRED_GROUP_FIELDS = ("id", "label")
_REQUIRED_TASK_FIELDS = ("id", "group", "label")


def load_checklist(path: str | Path) -> dict:
    """Reads and validates a checklist JSON, returning
    {"groups": [...], "tasks": [...]} unchanged. Raises ValueError with
    a specific message on any malformed entry, rather than letting
    widget code fail obscurely on a missing field later."""
    path = Path(path)
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
    import sys

    for path in sys.argv[1:] or [CHECKLISTS_DIR / "equipment_servicing_checklist.json"]:
        checklist = load_checklist(path)
        print(f"{path}:")
        print(f"  groups: {len(checklist['groups'])}")
        for group in checklist["groups"]:
            print("   ", group)
        print(f"  tasks: {len(checklist['tasks'])}")
        for task in checklist["tasks"]:
            print("   ", task)
