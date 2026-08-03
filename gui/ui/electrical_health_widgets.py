"""
Individual Electrical Health cluster indicator widgets.

Each class is a small, self-contained indicator wired to one named entry
from DataSource.signals.diagnostics_update's payload, via
DiagnosticsStatusIndicator (health_indicator_widget.py) — except
BatteryIndicator (its own dedicated battery_update(float) signal instead
of going through diagnostics) and CommsHealthIndicator (driven by
HealthStateMachine, not diagnostics — see comms_health_controller.py).
All the "how do I read my status" logic lives here, one place per
indicator; ElectricalHealthCluster (electrical_health_cluster.py) just
composes and lays these out.

Threshold/mismatch logic (thermal WARN/ERROR, contactor mismatch,
precharge stuck) is computed at the publishing side
(RosDataSource/SimulationDataSource) except for battery voltage, which
isn't part of the diagnostics contract and so is evaluated here.
"""

from ui.health_indicator_widget import DiagnosticsStatusIndicator, HealthIndicatorWidget
from ui.mode_badge_widget import ModeBadgeWidget
from state_machine import HealthState

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


class FaultLatchedIndicator(DiagnosticsStatusIndicator):

    def __init__(self, stale_timeout_ms: int, parent=None):
        super().__init__("FAULT\nLATCHED", "fault_latched", stale_timeout_ms, parent)

    def _render_status(self, status):
        latched = status["level"] != "OK"
        color = _FAULT_LATCHED_COLOR if latched else _LEVEL_COLORS["OK"]
        return ("LATCHED" if latched else "OK"), color


class ContactorIndicator(DiagnosticsStatusIndicator):

    def __init__(self, stale_timeout_ms: int, parent=None):
        super().__init__("CONTACTOR\ncmd vs actual", "contactor", stale_timeout_ms, parent)

    def _render_status(self, status):
        values = status.get("values", {})
        commanded = values.get("commanded", "?")
        actual = values.get("actual", "?")
        text = commanded if commanded == actual else f"{commanded}/{actual}"
        return text, _LEVEL_COLORS.get(status["level"], _LEVEL_COLORS["OK"])


class CurrentLimiterFaultIndicator(DiagnosticsStatusIndicator):

    def __init__(self, stale_timeout_ms: int, parent=None):
        super().__init__("I_LIMITER\nFAULT", "i_limiter_fault", stale_timeout_ms, parent)

    def _render_status(self, status):
        faulted = status["level"] != "OK"
        return ("FAULT" if faulted else "OK"), _LEVEL_COLORS.get(status["level"], _LEVEL_COLORS["OK"])


class PrechargeStateIndicator(DiagnosticsStatusIndicator):

    def __init__(self, stale_timeout_ms: int, parent=None):
        super().__init__("PRECHARGE\nSTATE", "precharge_state", stale_timeout_ms, parent)

    def _render_status(self, status):
        state = status.get("values", {}).get("state", "?")
        return state, _LEVEL_COLORS.get(status["level"], _LEVEL_COLORS["OK"])


class ThermalProbeIndicator(DiagnosticsStatusIndicator):
    """One box per physical probe (THERM1/2/3) — each is its own
    diagnostics entry with its own level, so one probe overheating or
    dropping out doesn't get averaged away by or masked by the other two."""

    def __init__(self, label: str, diagnostics_name: str, stale_timeout_ms: int, parent=None):
        super().__init__(label, diagnostics_name, stale_timeout_ms, parent)

    def _render_status(self, status):
        temp_c = status.get("values", {}).get("temp_c", "?")
        return f"{temp_c}°C", _LEVEL_COLORS.get(status["level"], _LEVEL_COLORS["OK"])


_HEALTH_COLORS = {
    "HEALTHY": _LEVEL_COLORS["OK"],
    "DEGRADED": _LEVEL_COLORS["WARN"],
    "LOST": _LEVEL_COLORS["ERROR"],
}


class CommsHealthIndicator(ModeBadgeWidget):
    """Mirrors HealthStateMachine.state (HEALTHY/DEGRADED/LOST), driven by
    CommsHealthController off the heartbeat signal — not diagnostics_update
    like the other indicators here. HealthStateMachine's own state *is*
    the liveness signal (that's what CommsHealthController's two
    StaleDataWatchers are for), so unlike the others this doesn't need its
    own separate staleness tracking — hence ModeBadgeWidget rather than
    HealthIndicatorWidget."""

    def __init__(self, parent=None):
        super().__init__(
            title="COMMS\nHEALTH",
            colors=_HEALTH_COLORS,
            default_mode=HealthState.HEALTHY.name,
            parent=parent,
        )

    def set_health_state(self, state: HealthState):
        self.set_mode(state.name)


class BatteryIndicator(HealthIndicatorWidget):
    """The one indicator not driven by diagnostics_update — battery has
    its own dedicated signal, so voltage thresholds are evaluated here
    directly rather than through `_render_status`."""

    def __init__(self, stale_timeout_ms: int, parent=None):
        super().__init__("BATTERY\nV / SOC", stale_timeout_ms, parent)

    def on_battery_update(self, voltage: float):
        if voltage <= _BATTERY_STOP_VOLTAGE:
            color = _LEVEL_COLORS["ERROR"]
        elif voltage <= _BATTERY_WARN_VOLTAGE:
            color = _LEVEL_COLORS["WARN"]
        else:
            color = _LEVEL_COLORS["OK"]
        self.update_value(f"{voltage:.1f}V", color)
