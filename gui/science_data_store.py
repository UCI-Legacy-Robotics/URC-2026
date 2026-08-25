"""
Science Mission data persistence.

Every piece of data a science sequence reports (status messages, GNSS,
images, readings) gets saved to disk here, tagged by site, so it can be
reopened later to show judges -- nothing in the GUI persisted anything
before this (see handoff). Data reported while no site is set (Panorama/
Stratigraphic Photo don't require one) falls into a fixed "Unsited"
bucket rather than being dropped, since every event must be saved
somewhere even when the site-label requirement doesn't apply to it.

On-disk layout, rooted at gui/science_data/ by default (generated data,
not source -- see .gitignore):

    science_data/
      _cache_state.json          {"cached_site": "...", "set_at": "..."}
      <slug>/
        site.json                {"label", "slug", "created_at", "events": [...]}
        images/<sequence>_<timestamp_ms>.png

Each events[] entry is one of:
    {"type": "status",  "sequence", "status", "message", "timestamp"}
    {"type": "gnss",    "sequence", "lat", "lon", "timestamp"}
    {"type": "image",   "sequence", "path", "timestamp"}
    {"type": "reading", "sequence", "reading", "timestamp"}

Each record_*() call is a read-modify-write of the whole site.json --
fine at this data volume (dozens of events per run, not a high-frequency
stream), and keeps a site's full record in one file that's easy for
load_site()/the review dialog (Step 10) to hand back in one piece.
"""

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image
from PyQt6.QtCore import QObject, pyqtSignal

from frame_decode import decode_frame_to_rgb

_UNSITED_LABEL = "Unsited"


def _slugify(label: str) -> str:
    slug = re.sub(r'[^a-z0-9]+', '_', label.strip().lower()).strip('_')
    return slug or 'site'


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class ScienceDataStore(QObject):

    sites_changed = pyqtSignal()  # a site was created or appended to

    def __init__(self, root_dir: Path | str | None = None, parent=None):
        super().__init__(parent)
        self._root = Path(root_dir) if root_dir is not None else Path(__file__).parent / "science_data"
        self._root.mkdir(parents=True, exist_ok=True)

    # -- site lifecycle -----------------------------------------------------

    def ensure_site(self, label: str | None) -> str:
        """Returns the slug for `label`, creating the site directory +
        site.json on first use. label=None (data reported with no
        current site set) always lands in the same fixed Unsited bucket."""
        label = label or _UNSITED_LABEL
        slug = self._resolve_slug(label)
        if self._read_site_json(slug) is None:
            (self._root / slug / "images").mkdir(parents=True, exist_ok=True)
            self._write_site_json(slug, {
                "label": label,
                "slug": slug,
                "created_at": _now_iso(),
                "events": [],
            })
            self.sites_changed.emit()
        return slug

    def _resolve_slug(self, label: str) -> str:
        base = _slugify(label)
        candidate = base
        suffix = 2
        while True:
            existing = self._read_site_json(candidate)
            if existing is None or existing.get("label") == label:
                return candidate
            candidate = f"{base}_{suffix}"
            suffix += 1

    # -- recording ------------------------------------------------------

    def record_status(self, site_label: str | None, sequence: str, status: str, message: str = ""):
        self._append_event(site_label, {
            "type": "status", "sequence": sequence, "status": status,
            "message": message, "timestamp": time.time(),
        })

    def record_gnss(self, site_label: str | None, sequence: str, lat: float, lon: float):
        self._append_event(site_label, {
            "type": "gnss", "sequence": sequence, "lat": lat, "lon": lon,
            "timestamp": time.time(),
        })

    def record_image(self, site_label: str | None, sequence: str, frame):
        slug = self.ensure_site(site_label)
        rgb = decode_frame_to_rgb(frame)
        timestamp = time.time()
        rel_path = f"images/{sequence.lower()}_{int(timestamp * 1000)}.png"
        Image.fromarray(rgb).save(self._root / slug / rel_path)
        self._append_event(site_label, {
            "type": "image", "sequence": sequence, "path": rel_path, "timestamp": timestamp,
        })

    def record_reading(self, site_label: str | None, sequence: str, reading: dict):
        self._append_event(site_label, {
            "type": "reading", "sequence": sequence, "reading": reading, "timestamp": time.time(),
        })

    def _append_event(self, site_label: str | None, event: dict):
        slug = self.ensure_site(site_label)
        data = self._read_site_json(slug)
        data["events"].append(event)
        self._write_site_json(slug, data)
        self.sites_changed.emit()

    # -- cache slot -------------------------------------------------------

    def get_cache_owner(self) -> str | None:
        return self._read_cache_state().get("cached_site")

    def set_cache_owner(self, site_label: str):
        self._write_cache_state({"cached_site": site_label, "set_at": _now_iso()})

    # -- review (Step 10) -------------------------------------------------

    def list_sites(self) -> list[dict]:
        sites = []
        for entry in sorted(self._root.iterdir()) if self._root.exists() else ():
            if not entry.is_dir():
                continue
            data = self._read_site_json(entry.name)
            if data is None:
                continue
            sites.append({
                "label": data["label"],
                "slug": data["slug"],
                "created_at": data["created_at"],
                "event_count": len(data.get("events", [])),
            })
        sites.sort(key=lambda s: s["created_at"], reverse=True)
        return sites

    def load_site(self, slug: str) -> dict:
        data = self._read_site_json(slug)
        if data is None:
            raise FileNotFoundError(f"No site found for slug {slug!r}")
        data = dict(data)
        data["events"] = [
            {**event, "path": self._root / slug / event["path"]} if event.get("type") == "image" else event
            for event in data.get("events", [])
        ]
        return data

    # -- disk I/O -----------------------------------------------------------

    def _site_json_path(self, slug: str) -> Path:
        return self._root / slug / "site.json"

    def _read_site_json(self, slug: str) -> dict | None:
        path = self._site_json_path(slug)
        if not path.exists():
            return None
        with open(path) as f:
            return json.load(f)

    def _write_site_json(self, slug: str, data: dict):
        path = self._site_json_path(slug)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def _cache_state_path(self) -> Path:
        return self._root / "_cache_state.json"

    def _read_cache_state(self) -> dict:
        path = self._cache_state_path()
        if not path.exists():
            return {}
        with open(path) as f:
            return json.load(f)

    def _write_cache_state(self, state: dict):
        path = self._cache_state_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(state, f, indent=2)


if __name__ == '__main__':
    import sys
    import tempfile
    from types import SimpleNamespace

    import numpy as np
    from PyQt6.QtCore import QCoreApplication

    app = QCoreApplication(sys.argv)

    with tempfile.TemporaryDirectory() as tmp:
        store = ScienceDataStore(root_dir=tmp)
        store.sites_changed.connect(lambda: print("[sites_changed]"))

        fake_frame = SimpleNamespace(
            encoding="rgb8",
            data=np.full((10, 10, 3), (40, 120, 40), dtype=np.uint8).tobytes(),
            height=10, width=10,
        )

        store.record_status("Site Alpha", "SPECTROMETER", "STARTING", "lowering drill")
        store.record_gnss("Site Alpha", "SPECTROMETER", 33.6405, -117.8443)
        store.record_image("Site Alpha", "SPECTROMETER", fake_frame)
        store.record_reading("Site Alpha", "SPECTROMETER", {"peak_wavelength_nm": 550.0, "absorbance": 1.2})
        store.set_cache_owner("Site Alpha")

        store.record_status("Site Beta", "NPK", "STARTING", "lowering probe")
        store.record_reading("Site Beta", "NPK", {"nitrogen_ppm": 30.0})

        store.record_image(None, "PANORAMA", fake_frame)  # no site set -> Unsited bucket

        print("cache owner:", store.get_cache_owner())
        print("sites:", store.list_sites())

        alpha_slug = store.ensure_site("Site Alpha")
        loaded = store.load_site(alpha_slug)
        print(f"loaded site {alpha_slug!r}:")
        for event in loaded["events"]:
            print(" ", event)

        print("\non-disk tree:")
        for path in sorted(Path(tmp).rglob("*")):
            print(" ", path.relative_to(tmp))
