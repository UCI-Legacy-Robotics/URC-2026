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
    heartbeat               = pyqtSignal()          # comms liveness pulse, no payload
    software_enable_ack     = pyqtSignal(bool)      # confirmed enabled/disabled state
    estop_confirmed         = pyqtSignal(bool)      # True = confirmed stopped, False = reset

    # diagnostics_update's payload is always a plain list of dicts:
    #   {"name": str, "level": "OK"|"WARN"|"ERROR"|"STALE", "message": str,
    #    "values": dict[str, str]}
    # RosDataSource translates the raw diagnostic_msgs/DiagnosticArray into
    # this shape (see ros_node.py); SimulationDataSource fakes it directly.
    # Widgets should only ever see this shape, never a ROS message type.
    #
    # heartbeat carries no data — HealthStateMachine's HEALTHY/DEGRADED/LOST
    # comes from how *often* it fires, not a value on it (see
    # comms_health_controller.py, which watches it via two StaleDataWatchers
    # at different timeouts rather than a single fresh/stale flag).
    #
    # imu_update's payload is always SimpleNamespace(roll_deg, pitch_deg,
    # yaw_deg) — plain floats in degrees, never a ROS quaternion.
    # RosDataSource converts the raw sensor_msgs/Imu orientation quaternion
    # into this shape (see ros_node.py); SimulationDataSource fakes it
    # directly. GnssMapWidget's heading arrow reads yaw_deg off this.


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

    @abstractmethod
    def send_software_enable_command(self, enabled: bool):
        """Request software control be enabled or disabled.

        This is NOT E-Stop — it only tells the rover to start/stop
        listening to GUI/joystick commands, it does not cut power or
        comms (see estop_widget.py, Step 12, for that). Confirmation
        comes back asynchronously via signals.software_enable_ack, the
        same requested-vs-confirmed pattern as subsystem launch.
        """
        raise NotImplementedError

    @abstractmethod
    def send_estop_request(self):
        """Request an E-Stop (hardware-equivalent kill of power/comms).

        This is a request, not a command that takes effect immediately —
        signals.estop_confirmed is the only thing that means the rover
        actually stopped. The two must never be collapsed into one event;
        EstopWidget (ui/estop_widget.py) visibly flags the gap if
        confirmation doesn't arrive in time. One-directional from the
        GUI's side: there's no "un-estop" request, only detecting a
        hardware reset if the rover reports estop_confirmed(False).
        """
        raise NotImplementedError
