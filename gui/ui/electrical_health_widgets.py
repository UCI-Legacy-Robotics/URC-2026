"""
Electrical Health cluster — 7 always-visible indicators, stretched across
the remaining width of the top strip.

Six of the seven (everything but battery) are driven off
DataSource.signals.diagnostics_update — a list of
{"name", "level", "message", "values"} dicts (see data_source.py for the
exact shape). Threshold/mismatch logic (thermal WARN/ERROR, contactor
commanded-vs-actual, precharge stuck) lives at the publishing side
(RosDataSource/SimulationDataSource), not here — this widget just trusts
"level" for color and renders "values" for display, the same way a real
diagnostics aggregator would be the thing computing severity, not the
GUI. Battery is the one exception: it has its own dedicated
battery_update(float) signal rather than going through diagnostics, so
its ~23V stop threshold is evaluated here.

Comms health is a placeholder for now — it just tracks the "comms" dict
entry like everything else. Real HealthStateMachine wiring (heartbeat ->
HEALTHY/DEGRADED/LOST) is Step 10.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy

from ui.health_indicator_widget import HealthIndicatorWidget

_LEVEL_COLORS = {
    "OK": "#1b5e20",
    "WARN": "#8a6d1a",
    "ERROR": "#7a1f1f",
    "STALE": "#4a4a2a",
}

# FAULT_LATCHED gets a distinctly brighter red than the rest of the
# cluster on latch — per the handoff, this is the most safety-critical
# indicator here and needs to visually stand out from an ordinary ERROR.
_FAULT_LATCHED_COLOR = "#d32f2f"

_BATTERY_STOP_VOLTAGE = 23.0
_BATTERY_WARN_VOLTAGE = 24.5

# How long without an update before an indicator flags itself stale.
# Placeholder — real thresholds are TBD with systems/electrical.
_STALE_TIMEOUT_MS = 5000


class ElectricalHealthCluster(QWidget):
    """Single row of electrical/safety indicators, stretched to fill all
    remaining width in the top strip (from the right edge of Subsystem
    Launch to the right edge of the window). Thermal lives here at
    mission-critical visibility per team decision, rather than being
    buried in the Diagnostics tab."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.fault_latched = HealthIndicatorWidget("FAULT\nLATCHED", _STALE_TIMEOUT_MS)
        self.contactor_status = HealthIndicatorWidget("CONTACTOR\ncmd vs actual", _STALE_TIMEOUT_MS)
        self.current_limiter_fault = HealthIndicatorWidget("I_LIMITER\nFAULT", _STALE_TIMEOUT_MS)
        self.precharge_state = HealthIndicatorWidget("PRECHARGE\nSTATE", _STALE_TIMEOUT_MS)
        self.battery_voltage = HealthIndicatorWidget("BATTERY\nV / SOC", _STALE_TIMEOUT_MS)
        self.comms_health = HealthIndicatorWidget("COMMS\nHEALTH", _STALE_TIMEOUT_MS)
        self.thermal = HealthIndicatorWidget("THERMAL\n(THERM1-3)", _STALE_TIMEOUT_MS)

        for w in (
            self.fault_latched,
            self.contactor_status,
            self.current_limiter_fault,
            self.precharge_state,
            self.battery_voltage,
            self.comms_health,
            self.thermal,
        ):
            w.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            layout.addWidget(w, 1)

    def bind_data_source(self, data_source):
        data_source.signals.diagnostics_update.connect(self._on_diagnostics_update)
        data_source.signals.battery_update.connect(self._on_battery_update)

    # -- internal -----------------------------------------------------

    def _on_diagnostics_update(self, statuses):
        by_name = {s["name"]: s for s in statuses}

        if "fault_latched" in by_name:
            s = by_name["fault_latched"]
            latched = s["level"] != "OK"
            self.fault_latched.update_value(
                "LATCHED" if latched else "OK",
                _FAULT_LATCHED_COLOR if latched else _LEVEL_COLORS["OK"],
            )

        if "contactor" in by_name:
            s = by_name["contactor"]
            values = s.get("values", {})
            commanded = values.get("commanded", "?")
            actual = values.get("actual", "?")
            text = commanded if commanded == actual else f"{commanded}/{actual}"
            self.contactor_status.update_value(
                text, _LEVEL_COLORS.get(s["level"], _LEVEL_COLORS["OK"])
            )

        if "i_limiter_fault" in by_name:
            s = by_name["i_limiter_fault"]
            self.current_limiter_fault.update_value(
                "FAULT" if s["level"] != "OK" else "OK",
                _LEVEL_COLORS.get(s["level"], _LEVEL_COLORS["OK"]),
            )

        if "precharge_state" in by_name:
            s = by_name["precharge_state"]
            state = s.get("values", {}).get("state", "?")
            self.precharge_state.update_value(
                state, _LEVEL_COLORS.get(s["level"], _LEVEL_COLORS["OK"])
            )

        if "thermal" in by_name:
            s = by_name["thermal"]
            values = s.get("values", {})
            text = (
                f"{values.get('therm1', '?')}/"
                f"{values.get('therm2', '?')}/"
                f"{values.get('therm3', '?')}°C"
            )
            self.thermal.update_value(
                text, _LEVEL_COLORS.get(s["level"], _LEVEL_COLORS["OK"])
            )

        if "comms" in by_name:
            s = by_name["comms"]
            self.comms_health.update_value(
                s["level"], _LEVEL_COLORS.get(s["level"], _LEVEL_COLORS["OK"])
            )

    def _on_battery_update(self, voltage):
        if voltage <= _BATTERY_STOP_VOLTAGE:
            color = _LEVEL_COLORS["ERROR"]
        elif voltage <= _BATTERY_WARN_VOLTAGE:
            color = _LEVEL_COLORS["WARN"]
        else:
            color = _LEVEL_COLORS["OK"]
        self.battery_voltage.update_value(f"{voltage:.1f}V", color)
