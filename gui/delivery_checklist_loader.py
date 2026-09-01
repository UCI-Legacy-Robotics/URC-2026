"""
Delivery checklist loader.

Loads delivery_checklist.json -- placeholder data shaped like the 2026
URC Delivery Mission rules, not the real 2027 rules (not yet published
as of writing). Swap the JSON file for a new season's tasks; nothing in
the GUI needs to change, since DeliveryChecklistWidget renders whatever
stages/tasks/options are in the file.

Schema:
    {
      "stages": [{"id", "label", "unlock_threshold"?}, ...],
      "tasks": [
        {"id", "stage", "label", "type": "checkbox", "points"},
        {"id", "stage", "label", "type": "counter",
         "options": [{"label", "points"}, ...], "total_points"},
        ...
      ]
    }

A counter task's options let one task score at more than one rate
(2026: large wreckage pieces 2 pts each, small pieces 5 pts each),
capped in one place at total_points, rather than needing a separate
task per rate with no shared cap.
"""

import json
from pathlib import Path

_DEFAULT_PATH = Path(__file__).parent / "delivery_checklist.json"

_REQUIRED_STAGE_FIELDS = ("id", "label")
_REQUIRED_TASK_FIELDS = ("id", "stage", "label", "type")
_REQUIRED_OPTION_FIELDS = ("label", "points")


def load_delivery_checklist(path: str | Path | None = None) -> dict:
    """Reads and validates the checklist JSON, returning
    {"stages": [...], "tasks": [...]} unchanged (plain dicts -- nothing
    downstream needs more structure than that). Raises ValueError with
    a specific message on any malformed entry, rather than letting
    widget code fail obscurely on a missing field later."""
    path = Path(path) if path is not None else _DEFAULT_PATH
    with open(path) as f:
        data = json.load(f)

    stages = data.get("stages")
    tasks = data.get("tasks")
    if not isinstance(stages, list) or not isinstance(tasks, list):
        raise ValueError(f"{path}: expected top-level 'stages' and 'tasks' lists")

    stage_ids = set()
    for stage in stages:
        _require_fields(stage, _REQUIRED_STAGE_FIELDS, f"{path}: stage {stage!r}")
        stage_ids.add(stage["id"])

    for task in tasks:
        _require_fields(task, _REQUIRED_TASK_FIELDS, f"{path}: task {task!r}")
        if task["stage"] not in stage_ids:
            raise ValueError(f"{path}: task {task['id']!r} references unknown stage {task['stage']!r}")

        task_type = task["type"]
        if task_type == "checkbox":
            _require_fields(task, ("points",), f"{path}: checkbox task {task['id']!r}")
        elif task_type == "counter":
            _require_fields(task, ("options", "total_points"), f"{path}: counter task {task['id']!r}")
            if not isinstance(task["options"], list) or not task["options"]:
                raise ValueError(f"{path}: counter task {task['id']!r} needs a non-empty 'options' list")
            for option in task["options"]:
                _require_fields(option, _REQUIRED_OPTION_FIELDS, f"{path}: option in task {task['id']!r}")
        else:
            raise ValueError(f"{path}: task {task['id']!r} has unknown type {task_type!r}")

    return {"stages": stages, "tasks": tasks}


def _require_fields(obj: dict, fields: tuple, context: str):
    missing = [f for f in fields if f not in obj]
    if missing:
        raise ValueError(f"{context} missing required field(s): {missing}")


if __name__ == '__main__':
    checklist = load_delivery_checklist()
    print(f"stages: {len(checklist['stages'])}")
    for stage in checklist["stages"]:
        print(" ", stage)
    print(f"tasks: {len(checklist['tasks'])}")
    for task in checklist["tasks"]:
        print(" ", task)
