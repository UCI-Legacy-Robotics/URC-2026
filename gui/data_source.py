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

    Mirrors RosSignals in ros_node.py. Kept as its own class rather than
    reusing RosSignals so this module has zero ROS dependency.
    """
    camera_frame       = pyqtSignal(object)
    gnss_fix           = pyqtSignal(float, float)
    battery_update     = pyqtSignal(float)
    imu_update         = pyqtSignal(object)
    diagnostics_update = pyqtSignal(object)


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
