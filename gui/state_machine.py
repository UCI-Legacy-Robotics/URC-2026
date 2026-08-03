"""
Mission and Health state machines for the base station GUI.
 
These are plain QObjects (not ROS nodes) — MainWindow owns them, and they
emit Qt signals on transition. Widgets/tabs listen to those signals to
enable/disable themselves; they never mutate state directly.
 
Topic subscribe/unsubscribe logic is NOT handled here yet — this is just
the state skeleton. Wiring it to ros_node.py comes later.
"""

from enum import Enum, auto
from PyQt6.QtCore import QObject, pyqtSignal


class MissionState(Enum):
    DIAGNOSTICS = auto()
    IDLE = auto()
    SCIENCE = auto()
    DELIVERY = auto()
    EQUIPMENT_SERVICING = auto()
    AUTONOMOUS_NAV = auto()


class HealthState(Enum):
    HEALTHY = auto()
    DEGRADED = auto()
    LOST = auto()
 
 
# States considered "mission in progress" — used to decide what gets locked.
_MISSION_STATES = frozenset({
    MissionState.SCIENCE,
    MissionState.DELIVERY,
    MissionState.EQUIPMENT_SERVICING,
    MissionState.AUTONOMOUS_NAV,
})
 
# Allowed transitions: from_state -> set of valid to_states.
# Mission states can only return to IDLE (mission complete/aborted) —
# no jumping directly from one mission to another.
_ALLOWED_TRANSITIONS = {
    MissionState.IDLE: {
        MissionState.DIAGNOSTICS,
        MissionState.SCIENCE,
        MissionState.DELIVERY,
        MissionState.EQUIPMENT_SERVICING,
        MissionState.AUTONOMOUS_NAV,
    },
    MissionState.DIAGNOSTICS: {
        MissionState.IDLE,
    },
    MissionState.SCIENCE: {MissionState.IDLE},
    MissionState.DELIVERY: {MissionState.IDLE},
    MissionState.EQUIPMENT_SERVICING: {MissionState.IDLE},
    MissionState.AUTONOMOUS_NAV: {MissionState.IDLE},
}
 
 
class InvalidTransitionError(Exception):
    def __init__(self, from_state: MissionState, to_state: MissionState):
        super().__init__(
            f"Invalid mission transition: {from_state.name} -> {to_state.name}"
        )
        self.from_state = from_state
        self.to_state = to_state


class MissionStateMachine(QObject):
    """
    Owns the current MissionState and enforces valid transitions.
 
    Signals:
        state_changed(MissionState, MissionState): emitted (old, new) on
            every successful transition.
        mission_started(MissionState): emitted when entering a mission state.
        mission_ended(MissionState): emitted when leaving a mission state
            back to IDLE (the mission that just ended is passed along).
    """
 
    state_changed = pyqtSignal(object, object)   # (old_state, new_state)
    mission_started = pyqtSignal(object)          # MissionState
    mission_ended = pyqtSignal(object)             # MissionState
 
    def __init__(self, initial_state: MissionState = MissionState.IDLE):
        super().__init__()
        self._state = initial_state
 
    @property
    def state(self) -> MissionState:
        return self._state
 
    def is_mission_active(self) -> bool:
        return self._state in _MISSION_STATES
 
    def can_transition_to(self, to_state: MissionState) -> bool:
        return to_state in _ALLOWED_TRANSITIONS.get(self._state, set())
 
    def transition_to(self, to_state: MissionState):
        if not self.can_transition_to(to_state):
            raise InvalidTransitionError(self._state, to_state)
 
        old_state = self._state
        self._state = to_state
        self.state_changed.emit(old_state, to_state)
 
        if to_state in _MISSION_STATES:
            self.mission_started.emit(to_state)
        elif old_state in _MISSION_STATES and to_state == MissionState.IDLE:
            self.mission_ended.emit(old_state)
 
 
class HealthStateMachine(QObject):
    """
    Placeholder skeleton — tracks link health separately from mission state.
    No real transition logic yet; wire this up once we have a heartbeat /
    link-quality signal from ros_node.py to drive it.
    """
 
    state_changed = pyqtSignal(object, object)  # (old_state, new_state)
 
    def __init__(self, initial_state: HealthState = HealthState.HEALTHY):
        super().__init__()
        self._state = initial_state
 
    @property
    def state(self) -> HealthState:
        return self._state
 
    def set_state(self, new_state: HealthState):
        if new_state == self._state:
            return
        old_state = self._state
        self._state = new_state
        self.state_changed.emit(old_state, new_state)