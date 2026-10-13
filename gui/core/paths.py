"""
Filesystem locations the GUI reads from and writes to, all relative to
the gui/ directory -- one place to update if files move, instead of
`Path(__file__).parent.parent...` chains scattered across modules.
"""

from pathlib import Path

GUI_ROOT = Path(__file__).resolve().parent.parent

CONFIG_DIR = GUI_ROOT / "config"
CHECKLISTS_DIR = CONFIG_DIR / "checklists"
ASSETS_DIR = GUI_ROOT / "assets"

# Generated at runtime (gitignored) -- everything the mission data
# stores record to disk.
MISSION_DATA_DIR = GUI_ROOT / "mission_data"
