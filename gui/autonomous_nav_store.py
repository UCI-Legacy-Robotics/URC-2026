"""
Autonomous Nav waypoint persistence.

Every GNSS coordinate an operator enters, plus the status events its
navigation attempt reports, gets saved to disk here -- same "nothing
reported gets silently dropped" motivation as ScienceDataStore, just
sized to what this mission actually needs: no images/readings, no
per-site directory tree, just one JSON file of waypoint records (a
run only ever has a handful of waypoints -- 2 GNSS-only locations, 2
posts, 3 objects, plus whatever repeat attempts happen -- nowhere near
the volume that would justify Science's one-file-per-site layout).

On-disk layout, rooted at gui/autonomous_nav_data/ by default
(generated data, not source -- see .gitignore):

    autonomous_nav_data/
      waypoints.json   {"waypoints": [
          {"id", "label", "type", "lat", "lon", "created_at", "events": [
              {"status", "message", "timestamp"}, ...
          ]},
          ...
      ]}

Each record_status() call is a read-modify-write of the whole file --
fine at this data volume, same reasoning ScienceDataStore's docstring
gives for its own per-site file.
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path

from PyQt6.QtCore import QObject, pyqtSignal


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class AutonomousNavStore(QObject):

    waypoints_changed = pyqtSignal()  # a waypoint was added or got a new status event

    def __init__(self, root_dir: Path | str | None = None, parent=None):
        super().__init__(parent)
        self._root = Path(root_dir) if root_dir is not None else Path(__file__).parent / "autonomous_nav_data"
        self._root.mkdir(parents=True, exist_ok=True)
        self._path = self._root / "waypoints.json"

    def add_waypoint(self, label: str, waypoint_type: str, lat: float, lon: float) -> dict:
        """Creates and persists a new waypoint record, returning it
        (including its generated id) so the caller can use that id for
        the navigation command and subsequent record_status() calls."""
        data = self._read()
        waypoint = {
            "id": f"wp_{int(time.time() * 1000)}",
            "label": label,
            "type": waypoint_type,
            "lat": lat,
            "lon": lon,
            "created_at": _now_iso(),
            "events": [],
        }
        data["waypoints"].append(waypoint)
        self._write(data)
        self.waypoints_changed.emit()
        return waypoint

    def record_status(self, waypoint_id: str, status: str, message: str = ""):
        data = self._read()
        for waypoint in data["waypoints"]:
            if waypoint["id"] == waypoint_id:
                waypoint["events"].append({
                    "status": status, "message": message, "timestamp": time.time(),
                })
                break
        else:
            return  # unknown waypoint id -- nothing to attach the event to
        self._write(data)
        self.waypoints_changed.emit()

    def list_waypoints(self) -> list[dict]:
        return self._read()["waypoints"]

    # -- disk I/O -----------------------------------------------------------

    def _read(self) -> dict:
        if not self._path.exists():
            return {"waypoints": []}
        with open(self._path) as f:
            return json.load(f)

    def _write(self, data: dict):
        with open(self._path, "w") as f:
            json.dump(data, f, indent=2)


if __name__ == '__main__':
    import sys
    import tempfile
    from PyQt6.QtCore import QCoreApplication

    app = QCoreApplication(sys.argv)

    with tempfile.TemporaryDirectory() as tmp:
        store = AutonomousNavStore(root_dir=tmp)
        store.waypoints_changed.connect(lambda: print("[waypoints_changed]"))

        wp1 = store.add_waypoint("GNSS Point 1", "accurate", 33.6405, -117.8443)
        store.record_status(wp1["id"], "STARTING", "beginning autonomous traverse")
        store.record_status(wp1["id"], "RUNNING", "en route")
        store.record_status(wp1["id"], "ARRIVED", "stopped within 3m")
        store.record_status(wp1["id"], "STOPPED", "control handed back to teleoperation")

        wp2 = store.add_waypoint("Post A", "post", 33.6410, -117.8440)

        print("waypoints:")
        for waypoint in store.list_waypoints():
            print(" ", waypoint)
