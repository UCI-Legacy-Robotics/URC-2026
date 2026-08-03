"""
Abstract telemetry source interface.

MainWindow and its widgets talk only to a DataSource's `.signals` — they
never know or care whether the feed is real ROS traffic (RosDataSource)
or synthetic data (SimulationDataSource). This is the seam that lets the
GUI run standalone without rclpy or hardware.

Kept dependency-free from rclpy/ROS message types on purpose, so this
module can be imported by main_window.py (or anything else) without
pulling in ROS.
"""

from abc import ABC, abstractmethod
from PyQt6.QtCore import QObject, pyqtSignal


class DataSourceSignals(QObject):
    """Qt signal contract every DataSource must expose via `.signals`.

    Used directly by both RosDataSource and SimulationDataSource — not
    just a matching shape, the literal same class — so there's exactly
    one place defining what a telemetry stream looks like.

    camera_frame/gnss_fix/battery_update/imu_update/diagnostics_update
    are inbound (rover -> GUI). subsystem_status_update is also inbound
    (subsystem process state -> GUI); the outbound direction (GUI ->
    rover subsystem commands) goes through DataSource.send_subsystem_command
    below rather than a signal, since it's a request, not a stream.
    """
    camera_frame            = pyqtSignal(object)
    gnss_fix                = pyqtSignal(float, float)
    battery_update          = pyqtSignal(float)
    imu_update              = pyqtSignal(object)
    diagnostics_update      = pyqtSignal(object)
    subsystem_status_update = pyqtSignal(str, str)  # (subsystem, status)

    # diagnostics_update's payload is always a plain list of dicts:
    #   {"name": str, "level": "OK"|"WARN"|"ERROR"|"STALE", "message": str,
    #    "values": dict[str, str]}
    # RosDataSource translates the raw diagnostic_msgs/DiagnosticArray into
    # this shape (see ros_node.py); SimulationDataSource fakes it directly.
    # Widgets should only ever see this shape, never a ROS message type.


class DataSource(ABC):
    """Base interface for anything that feeds telemetry to the GUI.

    Subclasses construct a `DataSourceSignals` as `self.signals` and emit
    on it from whatever backend they wrap (ROS callbacks, QTimers, ...).
    Widget code should only ever touch `.signals` and `start()`/`stop()`
    — no isinstance checks on the concrete subclass.
    """

    def __init__(self):
        self.signals = DataSourceSignals()

    @abstractmethod
    def start(self):
        """Begin producing data (start timers, spin a node, etc)."""
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        """Stop producing data and release any resources it holds."""
        raise NotImplementedError

    @abstractmethod
    def send_subsystem_command(self, subsystem: str, action: str):
        """Request a subsystem be launched or stopped.

        subsystem: "SCIENCE" or "ARM". action: "launch" or "stop".
        Real subsystem process management is out of scope for the GUI —
        implementations just log/no-op on this for now (see handoff
        Step 8); SimulationDataSource additionally fakes a status
        progression via subsystem_status_update so the UI has something
        to react to in --sim mode.
        """
        raise NotImplementedError
