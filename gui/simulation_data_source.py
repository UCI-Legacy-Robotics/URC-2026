"""
Synthetic DataSource for running the GUI without ROS or real hardware.

Each signal has its own QTimer so update rates can differ (GNSS drifts
slower than IMU jitters, for instance) and so new fake streams — e.g.
mission-specific fake ArUco detections — can be bolted on later without
touching the existing ones.
"""

import random
from types import SimpleNamespace

from PyQt6.QtCore import QTimer

from data_source import DataSource

# Arbitrary starting point in the general vicinity of URC (Mars Desert
# Research Station, Utah) — just a plausible-looking default, not real
# telemetry.
_BASE_LATITUDE = 38.4060
_BASE_LONGITUDE = -110.7918

_BATTERY_START_VOLTAGE = 29.0
_BATTERY_MIN_VOLTAGE = 22.0
_BATTERY_DECAY_PER_TICK = 0.01

# How long a fake subsystem launch/shutdown takes to confirm.
_SUBSYSTEM_STARTUP_MS = 2000
_SUBSYSTEM_SHUTDOWN_MS = 1500


class SimulationDataSource(DataSource):
    """Fakes plausible telemetry on the same signal contract as
    RosDataSource, so widgets can't tell the difference."""

    def __init__(self):
        super().__init__()

        self._latitude = _BASE_LATITUDE
        self._longitude = _BASE_LONGITUDE
        self._voltage = _BATTERY_START_VOLTAGE
        self._yaw_deg = 0.0

        self._gnss_timer = QTimer()
        self._gnss_timer.setInterval(1000)
        self._gnss_timer.timeout.connect(self._emit_gnss)

        self._battery_timer = QTimer()
        self._battery_timer.setInterval(2000)
        self._battery_timer.timeout.connect(self._emit_battery)

        self._imu_timer = QTimer()
        self._imu_timer.setInterval(200)
        self._imu_timer.timeout.connect(self._emit_imu)

        self._diagnostics_timer = QTimer()
        self._diagnostics_timer.setInterval(3000)
        self._diagnostics_timer.timeout.connect(self._emit_diagnostics)

        self._timers = (
            self._gnss_timer,
            self._battery_timer,
            self._imu_timer,
            self._diagnostics_timer,
        )

    def start(self):
        for timer in self._timers:
            timer.start()

    def stop(self):
        for timer in self._timers:
            timer.stop()

    # -- fake data generators -------------------------------------------

    def _emit_gnss(self):
        self._latitude += random.uniform(-0.00003, 0.00003)
        self._longitude += random.uniform(-0.00003, 0.00003)
        self.signals.gnss_fix.emit(self._latitude, self._longitude)

    def _emit_battery(self):
        self._voltage -= _BATTERY_DECAY_PER_TICK
        if self._voltage < _BATTERY_MIN_VOLTAGE:
            self._voltage = _BATTERY_START_VOLTAGE  # loop for demo purposes
        self.signals.battery_update.emit(round(self._voltage, 2))

    def _emit_imu(self):
        self._yaw_deg = (self._yaw_deg + random.uniform(-2.0, 2.0)) % 360.0
        imu = SimpleNamespace(
            roll_deg=random.uniform(-2.0, 2.0),
            pitch_deg=random.uniform(-2.0, 2.0),
            yaw_deg=self._yaw_deg,
        )
        self.signals.imu_update.emit(imu)

    def _emit_diagnostics(self):
        # Contactor: commanded state rarely fails to match actual, to
        # exercise the mismatch-alert path in the electrical health cluster.
        contactor_cmd = "CLOSED"
        contactor_actual = "CLOSED" if random.random() > 0.05 else "OPEN"
        contactor_level = "OK" if contactor_cmd == contactor_actual else "ERROR"

        therm1 = round(35 + random.uniform(-2, 8), 1)
        therm2 = round(35 + random.uniform(-2, 8), 1)
        therm3 = round(35 + random.uniform(-2, 8), 1)
        max_therm = max(therm1, therm2, therm3)
        if max_therm > 55:
            thermal_level = "ERROR"
        elif max_therm > 45:
            thermal_level = "WARN"
        else:
            thermal_level = "OK"

        diagnostics = [
            {"name": "fault_latched", "level": "OK", "message": "no latched faults", "values": {}},
            {
                "name": "contactor",
                "level": contactor_level,
                "message": "contactor commanded vs actual",
                "values": {"commanded": contactor_cmd, "actual": contactor_actual},
            },
            {"name": "i_limiter_fault", "level": "OK", "message": "no current limiter fault", "values": {}},
            {
                "name": "precharge_state",
                "level": "OK",
                "message": "precharge complete",
                "values": {"state": "COMPLETE"},
            },
            {
                "name": "thermal",
                "level": thermal_level,
                "message": "thermal probes",
                "values": {"therm1": str(therm1), "therm2": str(therm2), "therm3": str(therm3)},
            },
            {"name": "comms", "level": "OK", "message": "link healthy", "values": {}},
        ]
        self.signals.diagnostics_update.emit(diagnostics)

    # -- outbound commands ------------------------------------------------

    def send_subsystem_command(self, subsystem: str, action: str):
        print(f"[sim] subsystem command: {subsystem} -> {action}")
        if action == "launch":
            self.signals.subsystem_status_update.emit(subsystem, "STARTING")
            QTimer.singleShot(
                _SUBSYSTEM_STARTUP_MS,
                lambda: self.signals.subsystem_status_update.emit(subsystem, "RUNNING"),
            )
        elif action == "stop":
            self.signals.subsystem_status_update.emit(subsystem, "STOPPING")
            QTimer.singleShot(
                _SUBSYSTEM_SHUTDOWN_MS,
                lambda: self.signals.subsystem_status_update.emit(subsystem, "STOPPED"),
            )


if __name__ == '__main__':
    import sys
    from PyQt6.QtCore import QCoreApplication

    app = QCoreApplication(sys.argv)
    sim = SimulationDataSource()

    sim.signals.gnss_fix.connect(
        lambda lat, lon: print(f"gnss_fix: {lat:.6f}, {lon:.6f}"))
    sim.signals.battery_update.connect(
        lambda v: print(f"battery_update: {v}V"))
    sim.signals.imu_update.connect(
        lambda imu: print(f"imu_update: yaw={imu.yaw_deg:.1f}"))
    sim.signals.diagnostics_update.connect(
        lambda d: print(f"diagnostics_update: {d}"))
    sim.signals.subsystem_status_update.connect(
        lambda name, status: print(f"subsystem_status_update: {name} -> {status}"))

    sim.start()
    QTimer.singleShot(500, lambda: sim.send_subsystem_command("SCIENCE", "launch"))
    QTimer.singleShot(6000, app.quit)
    app.exec()
