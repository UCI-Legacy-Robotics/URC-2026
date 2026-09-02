"""
Tuning dashboard graph config loader.

Loads graphs_config.json -- currently all placeholder topics/values (see
the file's own entries), swapped for real ones once confirmed on testing
day. The dashboard builds exactly one plot tile per entry in "graphs";
nothing else about the UI needs to change when the JSON does.

Schema:
    {
      "window_seconds": <number>,          // default rolling window, all graphs
      "graphs": [
        {"id", "title", "units", "topic", "msg_type", "field",
         "window_seconds"?},                // per-graph override, optional
        ...
      ]
    }

msg_type is "pkg/msg/Type" (e.g. "std_msgs/msg/Float32"); field is a
dotted attribute path into that message (e.g. "data", or
"twist.twist.linear.x") yielding the plotted number.
"""

import json
from pathlib import Path

from msg_resolve import resolve_msg_type, get_field

_DEFAULT_PATH = Path(__file__).parent / "graphs_config.json"
_DEFAULT_WINDOW_SECONDS = 60

_REQUIRED_GRAPH_FIELDS = ("id", "title", "units", "topic", "msg_type", "field")


def load_graphs_config(path: str | Path | None = None) -> dict:
    """Reads and validates the graphs JSON, returning
    {"window_seconds": float, "graphs": [...]} -- each graph dict is
    unchanged from the JSON except "window_seconds" is always filled in
    (per-graph override, else the top-level default). Raises ValueError
    with a specific message on any malformed or unresolvable entry,
    rather than letting the ROS node or a widget fail obscurely later."""
    path = Path(path) if path is not None else _DEFAULT_PATH
    with open(path) as f:
        data = json.load(f)

    graphs = data.get("graphs")
    if not isinstance(graphs, list) or not graphs:
        raise ValueError(f"{path}: expected a non-empty top-level 'graphs' list")

    default_window = data.get("window_seconds", _DEFAULT_WINDOW_SECONDS)

    seen_ids = set()
    resolved_graphs = []
    for graph in graphs:
        _require_fields(graph, _REQUIRED_GRAPH_FIELDS, f"{path}: graph {graph!r}")

        graph_id = graph["id"]
        if graph_id in seen_ids:
            raise ValueError(f"{path}: duplicate graph id {graph_id!r}")
        seen_ids.add(graph_id)

        msg_class = resolve_msg_type(graph["msg_type"])
        # Fail fast on a typo'd field path too -- a default-constructed
        # instance is enough to check the attribute chain resolves,
        # without needing a live ROS topic.
        get_field(msg_class(), graph["field"])

        resolved_graphs.append({
            **graph,
            "window_seconds": graph.get("window_seconds", default_window),
        })

    return {"window_seconds": default_window, "graphs": resolved_graphs}


def _require_fields(obj: dict, fields: tuple, context: str):
    missing = [f for f in fields if f not in obj]
    if missing:
        raise ValueError(f"{context} missing required field(s): {missing}")


if __name__ == '__main__':
    config = load_graphs_config()
    print(f"window_seconds (default): {config['window_seconds']}")
    print(f"graphs: {len(config['graphs'])}")
    for graph in config["graphs"]:
        print(" ", graph["id"], "->", graph["topic"], graph["msg_type"], graph["field"])
