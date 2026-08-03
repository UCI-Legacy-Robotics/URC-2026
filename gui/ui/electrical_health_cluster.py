"""
Electrical Health cluster — composes the individual indicator widgets
from electrical_health_widgets.py into one row, stretched across the
remaining width of the top strip (from the right edge of Subsystem
Launch to the right edge of the window).
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy

from ui.electrical_health_widgets import (
    FaultLatchedIndicator,
    ContactorIndicator,
    CurrentLimiterFaultIndicator,
    PrechargeStateIndicator,
    ThermalProbeIndicator,
    CommsHealthIndicator,
    BatteryIndicator,
)

# How long without an update before an indicator flags itself stale.
# Placeholder — real thresholds are TBD with systems/electrical.
_STALE_TIMEOUT_MS = 5000


class ElectricalHealthCluster(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.fault_latched = FaultLatchedIndicator(_STALE_TIMEOUT_MS)
        self.contactor_status = ContactorIndicator(_STALE_TIMEOUT_MS)
        self.current_limiter_fault = CurrentLimiterFaultIndicator(_STALE_TIMEOUT_MS)
        self.precharge_state = PrechargeStateIndicator(_STALE_TIMEOUT_MS)
        self.battery_voltage = BatteryIndicator(_STALE_TIMEOUT_MS)
        self.comms_health = CommsHealthIndicator(_STALE_TIMEOUT_MS)
        self.therm1 = ThermalProbeIndicator("THERM1", "therm1", _STALE_TIMEOUT_MS)
        self.therm2 = ThermalProbeIndicator("THERM2", "therm2", _STALE_TIMEOUT_MS)
        self.therm3 = ThermalProbeIndicator("THERM3", "therm3", _STALE_TIMEOUT_MS)

        ordered_widgets = (
            self.fault_latched,
            self.contactor_status,
            self.current_limiter_fault,
            self.precharge_state,
            self.battery_voltage,
            self.comms_health,
            self.therm1,
            self.therm2,
            self.therm3,
        )
        # Everything except battery reads off diagnostics_update; battery
        # has its own dedicated signal (see bind_data_source below).
        self._diagnostics_indicators = (
            self.fault_latched,
            self.contactor_status,
            self.current_limiter_fault,
            self.precharge_state,
            self.comms_health,
            self.therm1,
            self.therm2,
            self.therm3,
        )

        for w in ordered_widgets:
            w.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            layout.addWidget(w, 1)

    def bind_data_source(self, data_source):
        data_source.signals.diagnostics_update.connect(self._on_diagnostics_update)
        data_source.signals.battery_update.connect(self.battery_voltage.on_battery_update)

    def _on_diagnostics_update(self, statuses):
        for indicator in self._diagnostics_indicators:
            indicator.on_diagnostics_update(statuses)
