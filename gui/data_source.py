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
from enum import Enum

from PyQt6.QtCore import QObject, pyqtSignal


class CameraID(Enum):
    """The 4 camera feeds the second-monitor MUX window can toggle.

    Values are the plain strings carried by camera_frame/enable_camera/
    disable_camera — the enum exists so call sites don't hand-type these
    strings, not because the signal contract requires an enum type.
    """
    SCIENCE_PAYLOAD = "science_payload"
    ARM_CAM_1 = "arm_cam_1"
    ARM_CAM_2 = "arm_cam_2"
    BIRDS_EYE = "birds_eye"


# Human-readable labels, keyed by CameraID value — shared by
# CameraFeedWidget's status strip and the MUX panel (Step 4) so there's
# one place to edit if a label needs to change.
CAMERA_LABELS = {
    CameraID.SCIENCE_PAYLOAD.value: "Science Payload Camera",
    CameraID.ARM_CAM_1.value: "Arm Camera 1",
    CameraID.ARM_CAM_2.value: "Arm Camera 2",
    CameraID.BIRDS_EYE.value: "Bird's Eye Camera",
}


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
    camera_frame            = pyqtSignal(str, object, int, float)  # (camera_id, frame, frame_bytes, timestamp)
    gnss_fix                = pyqtSignal(float, float)
    battery_update          = pyqtSignal(float)
    imu_update              = pyqtSignal(object)
    diagnostics_update      = pyqtSignal(object)
    subsystem_status_update = pyqtSignal(str, str)  # (subsystem, status)
    heartbeat               = pyqtSignal()          # comms liveness pulse, no payload
    software_enable_ack     = pyqtSignal(bool)      # confirmed enabled/disabled state
    estop_confirmed         = pyqtSignal(bool)      # True = confirmed stopped, False = reset

    # Science Mission sequence telemetry — see send_science_sequence_command
    # below for the outbound (launch/stop) side. `sequence` is always one
    # of "BRADFORD_CACHE"/"NPK"/"PANORAMA"/"STRATIGRAPHY", multiplexed onto
    # shared signals the same way camera_frame multiplexes on camera_id
    # and subsystem_status_update multiplexes on subsystem — one signal
    # per data shape rather than one per sequence, so widgets/the data
    # store can listen once and dispatch by tag.
    science_sequence_status = pyqtSignal(str, str, str)          # (sequence, status, message)
    science_gnss_fix        = pyqtSignal(str, float, float)      # (sequence, lat, lon) -- sample-site coords reported BY the rover, distinct from gnss_fix (the rover's own live position)
    science_image           = pyqtSignal(str, object, int, float)  # (sequence, frame, frame_bytes, timestamp) -- frame is the same SimpleNamespace(encoding, data, height, width) shape as camera_frame
    science_reading         = pyqtSignal(str, object)            # (sequence, reading: dict) -- opaque key/value payload, shape is rover-defined; widgets/store treat it generically rather than assuming fields

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
    #
    # camera_frame's frame argument is always SimpleNamespace(encoding,
    # data, height, width) — the same fields sensor_msgs/Image exposes,
    # duck-typed so CameraFeedWidget's decode code (numpy/cv2, no
    # cv_bridge) works unchanged regardless of source. camera_id is one
    # of the CameraID enum's string values. frame_bytes/timestamp are
    # emitted alongside every frame (not polled separately) so both
    # backends can drive CameraFeedWidget's rolling data-rate average
    # the same way; frame_bytes is provided explicitly (rather than
    # widgets reading len(frame.data) themselves) so the rate calc
    # doesn't depend on frame's exact shape.


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
    def enable_camera(self, camera_id: str):
        """Start receiving frames for the given camera (a CameraID value).

        Manual, per-camera, and independent of MissionState — the MUX
        panel is the only thing that calls this, there is no automatic
        enable tied to the active mission (see handoff: same philosophy
        as the Diagnostics tab decoupling). Idempotent: enabling an
        already-enabled camera is a no-op.
        """
        raise NotImplementedError

    @abstractmethod
    def disable_camera(self, camera_id: str):
        """Stop receiving frames for the given camera (a CameraID value).

        Must actually stop the data flow (RosDataSource tears down the
        subscription via destroy_subscription, not just stop forwarding
        frames to widgets) — the point is to reclaim bandwidth, not just
        hide the feed in the UI. Idempotent: disabling an already-disabled
        camera is a no-op.
        """
        raise NotImplementedError

    @abstractmethod
    def send_science_sequence_command(self, sequence: str, action: str, mode: str = ""):
        """Request a Science Mission sequence be launched or stopped.

        sequence: "BRADFORD_CACHE", "NPK", "PANORAMA", or "STRATIGRAPHY".
        action: "launch" or "stop". Panorama and Stratigraphic Photo are
        start-only sequences (no operator-initiated abort) — callers
        never send action="stop" for them.

        mode only applies to sequence="BRADFORD_CACHE" with action="launch":
        "CACHE" (lower drill, collect sample into the cache -- no mixer/
        vials/spectrometer reading) or "SPECTRO" (lower drill, collect
        sample into the mixer, pipe into vials, read on the onboard
        spectrometer). A site can only do one or the other -- the cache
        and the spectrometer/vials are each a site-exclusive resource,
        same as each other, just two separate ones -- never both and
        never neither. Implementations should ignore mode for any other
        sequence.

        Like send_subsystem_command, real sequence execution lives on
        the rover — implementations just log/no-op on this for now,
        no launch topic/service exists yet. Progress comes back
        asynchronously via signals.science_sequence_status and the
        science_gnss_fix/science_image/science_reading data signals.
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
