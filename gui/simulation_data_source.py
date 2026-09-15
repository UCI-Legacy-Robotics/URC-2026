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

# Same spacing/abort-confirm idea, for Equipment Servicing's sequences
# (Autonomous Typing, USB read) -- kept as its own pair of constants
# rather than reusing the science ones since the two tabs' pacing is
# free to diverge independently.
_EQUIPMENT_STEP_INTERVAL_MS = 700
_EQUIPMENT_STOP_CONFIRM_MS = 800

# Equipment Servicing sequences that put the rover into AUTONOMOUS
# control for their duration (see rover_control_mode) -- just
# Autonomous Typing today. USB_READ is arm-assisted/teleoperated, not
# autonomous, so it's left out.
_AUTONOMOUS_EQUIPMENT_SEQUENCES = ("LAUNCH_KEY",)

# Same spacing/abort-confirm idea, for Autonomous Nav's navigation
# attempts -- its own pair of constants since a fake traverse should
# plausibly take a bit longer than typing a key or reading a card.
_NAV_STEP_INTERVAL_MS = 900
_NAV_STOP_CONFIRM_MS = 800

# Panorama stops and photographs at this many points around the 360
# rotation before stitching -- randomized per launch within URC's
# typical range rather than a fixed count, same "plausible, not exact"
# spirit as the other fake sequence timings.
_PANORAMA_MIN_POSITIONS = 4
_PANORAMA_MAX_POSITIONS = 6

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

        # subsystem -> last known status ("SCIENCE"/"ARM" today), kept
        # around so set_joystick_mode() can check whether ARM is actually
        # RUNNING before allowing joystick_mode to claim ARM.
        self._subsystem_statuses = {}
        self._joystick_mode = "DRIVETRAIN"

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

        # Equipment Servicing sequences (Autonomous Typing / USB read):
        # same cancelable-timer-chain shape as _science_timers, kept in a
        # separate dict since these run on their own tab with their own
        # sequence names ("LAUNCH_KEY"/"USB_READ").
        self._equipment_timers = {}

        # Autonomous Nav: same cancelable-timer-chain shape again, keyed
        # by waypoint_id instead of a fixed sequence name (see
        # autonomous_nav_status in data_source.py).
        self._autonomous_nav_timers = {}

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
        for timers in self._equipment_timers.values():
            for timer in timers:
                timer.stop()
        for timers in self._autonomous_nav_timers.values():
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
            self._set_subsystem_status(subsystem, "STARTING")
            QTimer.singleShot(
                _SUBSYSTEM_STARTUP_MS,
                lambda: self._set_subsystem_status(subsystem, "RUNNING"),
            )
        elif action == "stop":
            self._set_subsystem_status(subsystem, "STOPPING")
            QTimer.singleShot(
                _SUBSYSTEM_SHUTDOWN_MS,
                lambda: self._set_subsystem_status(subsystem, "STOPPED"),
            )

    def _set_subsystem_status(self, subsystem: str, status: str):
        self._subsystem_statuses[subsystem] = status
        self.signals.subsystem_status_update.emit(subsystem, status)
        # The joystick can't stay bound to ARM once the Arm subsystem
        # isn't RUNNING anymore -- mirrors CameraWindow auto-disabling a
        # gated camera when its subsystem stops (see ros_node.py/
        # camera_window.py), just for joystick_mode instead of a camera.
        if subsystem == "ARM" and status != "RUNNING" and self._joystick_mode == "ARM":
            self.set_joystick_mode("DRIVETRAIN")

    def set_joystick_mode(self, mode: str):
        """Testing/demo hook -- a hardware mode button on the joystick
        itself picks this on real hardware, so there's no GUI-driven
        command path (unlike subsystem launch). ARM is refused unless
        the Arm subsystem is actually RUNNING, since the joystick can't
        be bound to a subsystem that isn't launched."""
        if mode == "ARM" and self._subsystem_statuses.get("ARM") != "RUNNING":
            print("[sim] joystick mode ARM refused -- ARM subsystem not RUNNING")
            return
        self._joystick_mode = mode
        self.signals.joystick_mode.emit(mode)

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

    def send_science_sequence_command(self, sequence: str, action: str, mode: str = ""):
        print(f"[sim] science sequence command: {sequence} -> {action} (mode={mode})")
        if action == "launch":
            self._cancel_science_timers(sequence)
            if sequence == "BRADFORD_CACHE":
                self._launch_bradford_cache_sequence(mode)
            elif sequence == "NPK":
                self._launch_npk_sequence()
            elif sequence == "PANORAMA":
                self._launch_panorama_sequence()
            elif sequence == "STRATIGRAPHY":
                self._launch_stratigraphy_sequence()
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

    def _launch_bradford_cache_sequence(self, mode: str):
        # CACHE and SPECTRO are two separate site-exclusive resources
        # (see send_science_sequence_command's docstring in data_source.py)
        # with genuinely different rover-side sequences, not just a
        # bookkeeping flag on top of one shared chain: CACHE stops after
        # the drill, SPECTRO skips the cache entirely and goes straight
        # to the mixer/vials/spectrometer. Both still document the sample
        # site (GNSS + arducam image) -- only SPECTRO also produces a
        # spectrometer reading.
        sequence = "BRADFORD_CACHE"
        self.signals.science_sequence_status.emit(sequence, "STARTING", "lowering drill")

        if mode == "CACHE":
            running_messages = ("drill lowered, collecting sample into cache",)
            complete_message = "cache sequence complete"
            emit_reading = False
        else:
            running_messages = (
                "drill lowered, collecting sample into mixer",
                "mixer piping sample into spectrometer vials",
                "spectrometer reading in progress",
            )
            complete_message = "spectro sequence complete"
            emit_reading = True

        delay = _SCIENCE_STEP_INTERVAL_MS
        for message in running_messages:
            self._schedule_science_step(
                sequence, delay,
                lambda m=message: self.signals.science_sequence_status.emit(sequence, "RUNNING", m),
            )
            delay += _SCIENCE_STEP_INTERVAL_MS

        self._schedule_science_step(
            sequence, delay, lambda: self._emit_bradford_cache_results(sequence, emit_reading)
        )
        delay += _SCIENCE_STEP_INTERVAL_MS
        self._schedule_science_step(
            sequence, delay,
            lambda: self.signals.science_sequence_status.emit(sequence, "STOPPED", complete_message),
        )

    def _emit_bradford_cache_results(self, sequence: str, emit_reading: bool):
        # Sample-site GNSS, reported by the rover -- not sampled from the
        # base station's own gnss_fix stream, per the "rover is source of
        # truth for the sample site" requirement. Sent for both CACHE and
        # SPECTRO -- documenting the site is independent of which resource
        # the sample went to.
        lat = self._latitude + random.uniform(-0.0001, 0.0001)
        lon = self._longitude + random.uniform(-0.0001, 0.0001)
        self.signals.science_gnss_fix.emit(sequence, lat, lon)

        counter = self._science_image_counters.get(sequence, 0) + 1
        self._science_image_counters[sequence] = counter
        frame = _make_fake_camera_frame(CameraID.SCIENCE_PAYLOAD.value, counter)
        self.signals.science_image.emit(sequence, frame, len(frame.data), time.time())

        if not emit_reading:
            return  # CACHE mode never touches the spectrometer/vials

        reading = {
            "peak_wavelength_nm": round(random.uniform(400, 700), 1),
            "absorbance": round(random.uniform(0.0, 2.0), 3),
        }
        self.signals.science_reading.emit(sequence, reading)

    def _launch_npk_sequence(self):
        # Shorter than Bradford/Cache -- just lowering a probe and reading
        # back soil data, no cache/mixer/vial steps -- and independently
        # keyed in _science_timers, so it can run concurrently alongside
        # Bradford/Cache without either interfering with the other.
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
            "temperature_c": round(random.uniform(10, 35), 1),
            "humidity_pct": round(random.uniform(10, 90), 1),
            "ph": round(random.uniform(4.5, 8.5), 2),
        }
        self.signals.science_reading.emit(sequence, reading)

    def _launch_panorama_sequence(self):
        # Start-only -- no _abort_science_sequence path is ever reached
        # for this sequence since ScienceSequenceWidget(stoppable=False)
        # never emits a stop_requested for it. The rover self-drives the
        # rotation, so it broadcasts AUTONOMOUS for the duration and
        # hands control back to TELEOPERATION once it's done -- see
        # rover_control_mode in data_source.py.
        sequence = "PANORAMA"
        self.signals.science_sequence_status.emit(sequence, "STARTING", "beginning 360 rotation")
        self.signals.rover_control_mode.emit("AUTONOMOUS")

        # One stop-and-photograph status step per position around the
        # rotation, then a final stitching step -- not one "rotating,
        # capturing frames" step glossing over the fact that the rover
        # actually stops at each point rather than shooting on the move.
        position_count = random.randint(_PANORAMA_MIN_POSITIONS, _PANORAMA_MAX_POSITIONS)
        running_messages = [
            f"stopped at position {i}/{position_count}, capturing photo"
            for i in range(1, position_count + 1)
        ]
        running_messages.append("stitching panorama onboard")

        delay = _SCIENCE_STEP_INTERVAL_MS
        for message in running_messages:
            self._schedule_science_step(
                sequence, delay,
                lambda m=message: self.signals.science_sequence_status.emit(sequence, "RUNNING", m),
            )
            delay += _SCIENCE_STEP_INTERVAL_MS

        self._schedule_science_step(sequence, delay, lambda: self._emit_science_image_result(sequence))
        delay += _SCIENCE_STEP_INTERVAL_MS
        self._schedule_science_step(
            sequence, delay, lambda: self.signals.rover_control_mode.emit("TELEOPERATION")
        )
        self._schedule_science_step(
            sequence, delay,
            lambda: self.signals.science_sequence_status.emit(sequence, "STOPPED", "panorama complete"),
        )

    def _emit_science_image_result(self, sequence: str):
        counter = self._science_image_counters.get(sequence, 0) + 1
        self._science_image_counters[sequence] = counter
        frame = _make_fake_camera_frame(sequence, counter)
        self.signals.science_image.emit(sequence, frame, len(frame.data), time.time())

    def _launch_stratigraphy_sequence(self):
        # Shortest chain of the four -- the operator has already driven
        # the rover into position, so this is just "capture and send one
        # image", no rotation/soil-probing/cache steps like the others.
        sequence = "STRATIGRAPHY"
        self.signals.science_sequence_status.emit(sequence, "STARTING", "capturing stratigraphic photo")

        delay = _SCIENCE_STEP_INTERVAL_MS
        self._schedule_science_step(sequence, delay, lambda: self._emit_science_image_result(sequence))
        delay += _SCIENCE_STEP_INTERVAL_MS
        self._schedule_science_step(
            sequence, delay,
            lambda: self.signals.science_sequence_status.emit(sequence, "STOPPED", "photo complete"),
        )

    # -- equipment servicing sequences --------------------------------------

    def send_equipment_sequence_command(self, sequence: str, action: str, key: str = ""):
        print(f"[sim] equipment sequence command: {sequence} -> {action} (key={key})")
        if action == "launch":
            self._cancel_equipment_timers(sequence)
            if sequence == "LAUNCH_KEY":
                self._launch_launch_key_sequence(key)
            elif sequence == "USB_READ":
                self._launch_usb_read_sequence()
        elif action == "stop":
            self._abort_equipment_sequence(sequence)

    def _cancel_equipment_timers(self, sequence: str):
        for timer in self._equipment_timers.pop(sequence, []):
            timer.stop()

    def _schedule_equipment_step(self, sequence: str, delay_ms: int, fn):
        """Cancelable equivalent of QTimer.singleShot, same shape as
        _schedule_science_step -- see that method's docstring."""
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(fn)
        self._equipment_timers.setdefault(sequence, []).append(timer)
        timer.start(delay_ms)

    def _abort_equipment_sequence(self, sequence: str):
        self._cancel_equipment_timers(sequence)
        self.signals.equipment_sequence_status.emit(sequence, "STOPPING", "")
        if sequence in _AUTONOMOUS_EQUIPMENT_SEQUENCES:
            self.signals.rover_control_mode.emit("TELEOPERATION")
        self._schedule_equipment_step(
            sequence, _EQUIPMENT_STOP_CONFIRM_MS,
            lambda: self.signals.equipment_sequence_status.emit(sequence, "STOPPED", ""),
        )

    def _launch_launch_key_sequence(self, key: str):
        # Autonomous Typing: the rover reports AUTONOMOUS for the
        # duration (same rover_control_mode broadcast Panorama's
        # self-driven rotation uses), typing one status step per letter
        # of the programmed key, then hands control back. A blank key
        # (nothing programmed yet) still runs, just with a single
        # generic step, rather than refusing to launch -- the widget's
        # own validation is what should stop an op with no key from
        # ever reaching here for real hardware.
        sequence = "LAUNCH_KEY"
        self.signals.equipment_sequence_status.emit(sequence, "STARTING", "entering autonomous mode")
        self.signals.rover_control_mode.emit("AUTONOMOUS")

        letters = list(key) if key else ["?"]
        running_messages = [
            f"typing '{letter}' ({i}/{len(letters)})" for i, letter in enumerate(letters, start=1)
        ]

        delay = _EQUIPMENT_STEP_INTERVAL_MS
        for message in running_messages:
            self._schedule_equipment_step(
                sequence, delay,
                lambda m=message: self.signals.equipment_sequence_status.emit(sequence, "RUNNING", m),
            )
            delay += _EQUIPMENT_STEP_INTERVAL_MS

        self._schedule_equipment_step(
            sequence, delay, lambda: self.signals.rover_control_mode.emit("TELEOPERATION")
        )
        self._schedule_equipment_step(
            sequence, delay,
            lambda: self.signals.equipment_sequence_status.emit(sequence, "STOPPED", "launch key entered"),
        )

    def _launch_usb_read_sequence(self):
        # USB-C cable into the lander's card slot, then read GNSS
        # coordinates back off the memory card's text file -- no
        # autonomous-mode toggle (arm-assisted/teleoperated insertion),
        # just a status chain ending in a reported fix, same shape as
        # Bradford/Cache's site-GNSS report.
        sequence = "USB_READ"
        self.signals.equipment_sequence_status.emit(sequence, "STARTING", "connecting to memory card")

        delay = _EQUIPMENT_STEP_INTERVAL_MS
        self._schedule_equipment_step(
            sequence, delay,
            lambda: self.signals.equipment_sequence_status.emit(sequence, "RUNNING", "reading GNSS file from card"),
        )
        delay += _EQUIPMENT_STEP_INTERVAL_MS
        self._schedule_equipment_step(sequence, delay, lambda: self._emit_usb_read_results(sequence))
        delay += _EQUIPMENT_STEP_INTERVAL_MS
        self._schedule_equipment_step(
            sequence, delay,
            lambda: self.signals.equipment_sequence_status.emit(sequence, "STOPPED", "read complete"),
        )

    def _emit_usb_read_results(self, sequence: str):
        lat = self._latitude + random.uniform(-0.0001, 0.0001)
        lon = self._longitude + random.uniform(-0.0001, 0.0001)
        self.signals.equipment_gnss_fix.emit(sequence, lat, lon)

    # -- autonomous nav sequences --------------------------------------------

    def send_autonomous_nav_command(self, waypoint_id: str, action: str,
                                     lat: float = 0.0, lon: float = 0.0,
                                     label: str = "", waypoint_type: str = ""):
        print(f"[sim] autonomous nav command: {waypoint_id} -> {action} "
              f"(lat={lat}, lon={lon}, label={label!r}, type={waypoint_type!r})")
        if action == "launch":
            self._cancel_nav_timers(waypoint_id)
            self._launch_nav_sequence(waypoint_id, label, waypoint_type)
        elif action == "stop":
            self._abort_nav_sequence(waypoint_id)

    def _cancel_nav_timers(self, waypoint_id: str):
        for timer in self._autonomous_nav_timers.pop(waypoint_id, []):
            timer.stop()

    def _schedule_nav_step(self, waypoint_id: str, delay_ms: int, fn):
        """Cancelable equivalent of QTimer.singleShot, same shape as
        _schedule_science_step -- see that method's docstring."""
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(fn)
        self._autonomous_nav_timers.setdefault(waypoint_id, []).append(timer)
        timer.start(delay_ms)

    def _abort_nav_sequence(self, waypoint_id: str):
        # Per the mission rules, an operator may abort at any point and
        # the rover autonomously returns/stops -- either way control
        # comes back to teleoperation, same as a normal completion.
        self._cancel_nav_timers(waypoint_id)
        self.signals.autonomous_nav_status.emit(waypoint_id, "STOPPING", "")
        self.signals.rover_control_mode.emit("TELEOPERATION")
        self._schedule_nav_step(
            waypoint_id, _NAV_STOP_CONFIRM_MS,
            lambda: self.signals.autonomous_nav_status.emit(waypoint_id, "STOPPED", "aborted"),
        )

    def _launch_nav_sequence(self, waypoint_id: str, label: str, waypoint_type: str):
        # Autonomous traverse to a GNSS-only location, a post, or an
        # object -- one fake chain regardless of type (the rules'
        # per-type tolerances/obstacle-avoidance are a rover-side
        # concern, not something this fake status feed needs to model
        # differently). Ends with ARRIVED (the rover's obvious "reached
        # the target" signal -- see set_status()'s docstring in
        # data_source.py) before handing control back and reporting
        # STOPPED, same "self-driven maneuver reports AUTONOMOUS, then
        # hands back to TELEOPERATION when done" shape Panorama uses.
        target = label or waypoint_type or "waypoint"
        self.signals.autonomous_nav_status.emit(waypoint_id, "STARTING", f"plotting route to {target}")
        self.signals.rover_control_mode.emit("AUTONOMOUS")

        running_messages = [f"en route to {target}"]
        if waypoint_type == "object":
            running_messages.append("obstacle detected, planning avoidance path")
        running_messages.append("running image detection" if waypoint_type == "object" else "approaching target")

        delay = _NAV_STEP_INTERVAL_MS
        for message in running_messages:
            self._schedule_nav_step(
                waypoint_id, delay,
                lambda m=message: self.signals.autonomous_nav_status.emit(waypoint_id, "RUNNING", m),
            )
            delay += _NAV_STEP_INTERVAL_MS

        self._schedule_nav_step(
            waypoint_id, delay,
            lambda: self.signals.autonomous_nav_status.emit(waypoint_id, "ARRIVED", f"arrived at {target}"),
        )
        delay += _NAV_STEP_INTERVAL_MS
        self._schedule_nav_step(
            waypoint_id, delay, lambda: self.signals.rover_control_mode.emit("TELEOPERATION")
        )
        self._schedule_nav_step(
            waypoint_id, delay,
            lambda: self.signals.autonomous_nav_status.emit(waypoint_id, "STOPPED", "ready for further instructions"),
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
    sim.signals.heartbeat.connect(lambda: print("heartbeat"))
    sim.signals.estop_confirmed.connect(
        lambda confirmed: print(f"estop_confirmed: {confirmed}"))

    sim.start()
    QTimer.singleShot(500, lambda: sim.send_subsystem_command("SCIENCE", "launch"))
    QTimer.singleShot(2000, lambda: sim.set_heartbeat_enabled(False))
    QTimer.singleShot(2500, sim.send_estop_request)
    QTimer.singleShot(6000, app.quit)
    app.exec()
