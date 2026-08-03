"""
Wires a DataSource's heartbeat signal to HealthStateMachine.

Uses two StaleDataWatchers (stale_data.py) at different timeouts rather
than a single fresh/stale flag, since HealthStateMachine has three states:
no heartbeat for a short while means DEGRADED, no heartbeat for longer
means LOST. Thresholds are placeholders — TBD with systems/electrical
once a real heartbeat topic/rate is defined.

Subscribe/unsubscribe prioritization based on health state (dropping
low-priority topics when comms is DEGRADED) is a later step, not handled
here — this just gets the state machine transitioning correctly.
"""

from state_machine import HealthState, HealthStateMachine
from stale_data import StaleDataWatcher

_DEGRADED_TIMEOUT_MS = 2000
_LOST_TIMEOUT_MS = 5000


class CommsHealthController:

    def __init__(self, health_state_machine: HealthStateMachine):
        self.health_state_machine = health_state_machine

        self._degraded_watcher = StaleDataWatcher(_DEGRADED_TIMEOUT_MS)
        self._lost_watcher = StaleDataWatcher(_LOST_TIMEOUT_MS)

        self._degraded_watcher.became_stale.connect(self._on_degraded_timeout)
        self._lost_watcher.became_stale.connect(self._on_lost_timeout)

    def on_heartbeat(self):
        """Connect directly to DataSource.signals.heartbeat."""
        self._degraded_watcher.notify()
        self._lost_watcher.notify()
        self.health_state_machine.set_state(HealthState.HEALTHY)

    def _on_degraded_timeout(self):
        if self.health_state_machine.state == HealthState.HEALTHY:
            self.health_state_machine.set_state(HealthState.DEGRADED)

    def _on_lost_timeout(self):
        self.health_state_machine.set_state(HealthState.LOST)
