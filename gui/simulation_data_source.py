"""
Synthetic DataSource for running the GUI without ROS or real hardware.

Each signal has its own QTimer so update rates can differ (GNSS drifts
slower than IMU jitters, for instance) and so new fake streams — e.g.
mission-specific fake ArUco detections — can be bolted on later without
touching the existing ones.
"""

import random
import time
from types import SimpleNamespace

import numpy as np
from PyQt6.QtCore import QTimer

from data_source import DataSource, CameraID

# UCI campus — matches the offline map tiles downloaded into
# assets/gnss_map/tiles/ and app.js's DEFAULT_CENTER, so the sim rover
# actually drifts over real map imagery instead of blank/untiled area.
# Not the real competition site (MDRS, Utah) — swap both together
# whenever real competition-area tiles get downloaded.
_BASE_LATITUDE = 33.6405
_BASE_LONGITUDE = -117.8443

_BATTERY_START_VOLTAGE = 29.0
_BATTERY_MIN_VOLTAGE = 22.0
_BATTERY_DECAY_PER_TICK = 0.01

# How long a fake subsystem launch/shutdown takes to confirm.
_SUBSYSTEM_STARTUP_MS = 2000
_SUBSYSTEM_SHUTDOWN_MS = 1500

_HEARTBEAT_INTERVAL_MS = 500

# How long a fake software enable/disable command takes to confirm.
_SOFTWARE_ENABLE_ACK_MS = 800

# How long a fake E-Stop request takes to confirm, when not withheld.
_ESTOP_CONFIRM_MS = 1000

# Spacing between chained fake status messages within a science sequence,
# and how long a fake abort takes to confirm STOPPING -> STOPPED.
_SCIENCE_STEP_INTERVAL_MS = 900
_SCIENCE_STOP_CONFIRM_MS = 800

# Fake camera frames: small resolution + ~5fps is plausible for a
# bandwidth-limited field link, and keeps the encode/emit cost trivial.
_CAMERA_FRAME_INTERVAL_MS = 200
_CAMERA_FRAME_HEIGHT = 240
_CAMERA_FRAME_WIDTH = 320

# Solid background per camera, purely so the 4 feeds are visually
# distinguishable in --sim.
_CAMERA_COLORS = {
    CameraID.SCIENCE_PAYLOAD.value: (40, 120, 40),
    CameraID.ARM_CAM_1.value: (40, 40, 120),
    CameraID.ARM_CAM_2.value: (120, 40, 120),
    CameraID.BIRDS_EYE.value: (120, 90, 20),
}


def _make_fake_camera_frame(camera_id: str, counter: int) -> SimpleNamespace:
    """Solid-color test pattern with a sweeping bar so it reads as live,
    not a static image. Same SimpleNamespace(encoding, data, height,
    width) shape RosDataSource normalizes real frames into, so
    CameraFeedWidget's decode path can't tell the two apart."""
    color = _CAMERA_COLORS.get(camera_id, (80, 80, 80))
    arr = np.full((_CAMERA_FRAME_HEIGHT, _CAMERA_FRAME_WIDTH, 3), color, dtype=np.uint8)
    bar_x = (counter * 4) % _CAMERA_FRAME_WIDTH
    arr[:, bar_x:bar_x + 10] = (255, 255, 255)
    return SimpleNamespace(
        encoding='rgb8',
        data=arr.tobytes(),
        height=_CAMERA_FRAME_HEIGHT,
        width=_CAMERA_FRAME_WIDTH,
    )


class SimulationDataSource(DataSource):
    """Fakes plausible telemetry on the same signal contract as
    RosDataSource, so widgets can't tell the difference."""

    def __init__(self):
        super().__init__()

        self._latitude = _BASE_LATITUDE
        self._longitude = _BASE_LONGITUDE
        self._voltage = _BATTERY_START_VOLTAGE
        self._yaw_deg = 0.0
        self._software_enabled = True
        self._withhold_estop_confirmation = False

        # Cameras start disabled (no timers running) — same "opt in via
        # MUX" behavior as RosDataSource's subscriptions, so --sim
        # exercises the same enable/disable lifecycle as real hardware.
        self._camera_timers = {}
        self._camera_frame_counters = {}

        # Science sequences: each sequence's chain of fake QTimers, kept
        # around (rather than using static QTimer.singleShot calls) so a
        # "stop" request can actually cancel whatever's still pending --
        # see _cancel_science_timers.
        self._science_timers = {}
        self._science_image_counters = {}

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

        self._heartbeat_timer = QTimer()
        self._heartbeat_timer.setInterval(_HEARTBEAT_INTERVAL_MS)
        self._heartbeat_timer.timeout.connect(self.signals.heartbeat.emit)

        self._timers = (
            self._gnss_timer,
            self._battery_timer,
            self._imu_timer,
            self._diagnostics_timer,
            self._heartbeat_timer,
        )

    def start(self):
        for timer in self._timers:
            timer.start()
        # Announce current state on connect, same as real hardware would.
        self.signals.software_enable_ack.emit(self._software_enabled)

    def stop(self):
        for timer in self._timers:
            timer.stop()
        for timer in self._camera_timers.values():
            timer.stop()
        for timers in self._science_timers.values():
            for timer in timers:
                timer.stop()

    def enable_camera(self, camera_id: str):
        if camera_id in self._camera_timers:
            return  # already enabled
        timer = QTimer()
        timer.setInterval(_CAMERA_FRAME_INTERVAL_MS)
        timer.timeout.connect(lambda: self._emit_camera_frame(camera_id))
        self._camera_timers[camera_id] = timer
        timer.start()

    def disable_camera(self, camera_id: str):
        timer = self._camera_timers.pop(camera_id, None)
        if timer is not None:
            timer.stop()

    def _emit_camera_frame(self, camera_id: str):
        counter = self._camera_frame_counters.get(camera_id, 0) + 1
        self._camera_frame_counters[camera_id] = counter
        frame = _make_fake_camera_frame(camera_id, counter)
        self.signals.camera_frame.emit(camera_id, frame, len(frame.data), time.time())

    def set_heartbeat_enabled(self, enabled: bool):
        """Testing/demo hook to simulate a comms dropout — stops just the
        heartbeat pulse so CommsHealthController's watchers time out into
        DEGRADED then LOST, without touching any other fake telemetry."""
        if enabled:
            self._heartbeat_timer.start()
        else:
            self._heartbeat_timer.stop()

    def set_withhold_estop_confirmation(self, withhold: bool):
        """Testing/demo hook to exercise EstopWidget's "no confirmation
        received" timeout path — makes send_estop_request() never confirm,
        simulating a lost/dropped confirmation."""
        self._withhold_estop_confirmation = withhold

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

        # Each thermal probe is its own diagnostics entry with its own
        # level — a physical sensor is independent of its neighbors, so
        # one running hot shouldn't be averaged away by the other two.
        thermal_entries = [
            self._fake_thermal_entry(f"therm{i}")
            for i in (1, 2, 3)
        ]

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
            *thermal_entries,
        ]
        self.signals.diagnostics_update.emit(diagnostics)

    @staticmethod
    def _fake_thermal_entry(name: str):
        temp_c = round(35 + random.uniform(-2, 8), 1)
        if temp_c > 55:
            level = "ERROR"
        elif temp_c > 45:
            level = "WARN"
        else:
            level = "OK"
        return {
            "name": name,
            "level": level,
            "message": f"{name} probe",
            "values": {"temp_c": str(temp_c)},
        }

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

    def send_software_enable_command(self, enabled: bool):
        print(f"[sim] software enable command: {enabled}")

        def _confirm():
            self._software_enabled = enabled
            self.signals.software_enable_ack.emit(enabled)

        QTimer.singleShot(_SOFTWARE_ENABLE_ACK_MS, _confirm)

    def send_estop_request(self):
        print(f"[sim] estop request (withheld={self._withhold_estop_confirmation})")
        if self._withhold_estop_confirmation:
            return  # simulate a lost confirmation for testing the timeout path
        QTimer.singleShot(
            _ESTOP_CONFIRM_MS,
            lambda: self.signals.estop_confirmed.emit(True),
        )

    # -- science sequences -------------------------------------------------

    def send_science_sequence_command(self, sequence: str, action: str, collect_to_cache: bool = False):
        print(f"[sim] science sequence command: {sequence} -> {action} (collect_to_cache={collect_to_cache})")
        if action == "launch":
            self._cancel_science_timers(sequence)
            if sequence == "SPECTROMETER":
                self._launch_spectrometer_sequence()
            elif sequence == "NPK":
                self._launch_npk_sequence()
        elif action == "stop":
            self._abort_science_sequence(sequence)

    def _cancel_science_timers(self, sequence: str):
        for timer in self._science_timers.pop(sequence, []):
            timer.stop()

    def _schedule_science_step(self, sequence: str, delay_ms: int, fn):
        """Cancelable equivalent of QTimer.singleShot — kept on
        self._science_timers[sequence] so _cancel_science_timers can stop
        anything still pending if the operator aborts mid-sequence."""
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(fn)
        self._science_timers.setdefault(sequence, []).append(timer)
        timer.start(delay_ms)

    def _abort_science_sequence(self, sequence: str):
        self._cancel_science_timers(sequence)
        self.signals.science_sequence_status.emit(sequence, "STOPPING", "")
        self._schedule_science_step(
            sequence, _SCIENCE_STOP_CONFIRM_MS,
            lambda: self.signals.science_sequence_status.emit(sequence, "STOPPED", ""),
        )

    def _launch_spectrometer_sequence(self):
        sequence = "SPECTROMETER"
        self.signals.science_sequence_status.emit(sequence, "STARTING", "lowering drill")

        running_messages = (
            "drill lowered, loading sample into cache",
            "sample loaded into mixer",
            "mixer emptying into spectrometer vials",
            "spectrometer reading in progress",
        )
        delay = _SCIENCE_STEP_INTERVAL_MS
        for message in running_messages:
            self._schedule_science_step(
                sequence, delay,
                lambda m=message: self.signals.science_sequence_status.emit(sequence, "RUNNING", m),
            )
            delay += _SCIENCE_STEP_INTERVAL_MS

        self._schedule_science_step(sequence, delay, lambda: self._emit_spectrometer_results(sequence))
        delay += _SCIENCE_STEP_INTERVAL_MS
        self._schedule_science_step(
            sequence, delay,
            lambda: self.signals.science_sequence_status.emit(sequence, "STOPPED", "sequence complete"),
        )

    def _emit_spectrometer_results(self, sequence: str):
        # Sample-site GNSS, reported by the rover -- not sampled from the
        # base station's own gnss_fix stream, per the "rover is source of
        # truth for the sample site" requirement.
        lat = self._latitude + random.uniform(-0.0001, 0.0001)
        lon = self._longitude + random.uniform(-0.0001, 0.0001)
        self.signals.science_gnss_fix.emit(sequence, lat, lon)

        counter = self._science_image_counters.get(sequence, 0) + 1
        self._science_image_counters[sequence] = counter
        frame = _make_fake_camera_frame(CameraID.SCIENCE_PAYLOAD.value, counter)
        self.signals.science_image.emit(sequence, frame, len(frame.data), time.time())

        reading = {
            "peak_wavelength_nm": round(random.uniform(400, 700), 1),
            "absorbance": round(random.uniform(0.0, 2.0), 3),
        }
        self.signals.science_reading.emit(sequence, reading)

    def _launch_npk_sequence(self):
        # Shorter than Spectrometer -- just lowering a probe and reading
        # back soil data, no cache/mixer/vial steps -- and independently
        # keyed in _science_timers, so it can run concurrently alongside
        # Spectrometer without either interfering with the other.
        sequence = "NPK"
        self.signals.science_sequence_status.emit(sequence, "STARTING", "lowering NPK probe")

        delay = _SCIENCE_STEP_INTERVAL_MS
        self._schedule_science_step(
            sequence, delay,
            lambda: self.signals.science_sequence_status.emit(sequence, "RUNNING", "probe in soil, reading"),
        )
        delay += _SCIENCE_STEP_INTERVAL_MS
        self._schedule_science_step(sequence, delay, lambda: self._emit_npk_results(sequence))
        delay += _SCIENCE_STEP_INTERVAL_MS
        self._schedule_science_step(
            sequence, delay,
            lambda: self.signals.science_sequence_status.emit(sequence, "STOPPED", "sequence complete"),
        )

    def _emit_npk_results(self, sequence: str):
        reading = {
            "nitrogen_ppm": round(random.uniform(5, 60), 1),
            "phosphorus_ppm": round(random.uniform(2, 40), 1),
            "potassium_ppm": round(random.uniform(5, 80), 1),
        }
        self.signals.science_reading.emit(sequence, reading)


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
    sim.signals.heartbeat.connect(lambda: print("heartbeat"))
    sim.signals.estop_confirmed.connect(
        lambda confirmed: print(f"estop_confirmed: {confirmed}"))

    sim.start()
    QTimer.singleShot(500, lambda: sim.send_subsystem_command("SCIENCE", "launch"))
    QTimer.singleShot(2000, lambda: sim.set_heartbeat_enabled(False))
    QTimer.singleShot(2500, sim.send_estop_request)
    QTimer.singleShot(6000, app.quit)
    app.exec()
