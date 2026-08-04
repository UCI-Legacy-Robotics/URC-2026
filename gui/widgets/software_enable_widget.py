"""
Software Enable/Disable toggle — sidebar, bottom row.

Distinct from E-Stop (estop_widget.py, Step 12): this only tells the
rover to start/stop listening to GUI/joystick commands — it does not cut
power or comms. Never merge their logic or UI state.

Tracks requested-vs-confirmed state the same way subsystem launch does
(Step 8): pressing the button sends a request and shows a pending state;
the button only reflects ENABLED/DISABLED once DataSource confirms it via
software_enable_ack. Visually lower severity than E-Stop — green/blue,
never red — since this isn't a hardware-equivalent safety action.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal

from widgets.color_coded_label import ColorCodedLabel

_COLOR_ENABLED = "#1b5e20"
_COLOR_DISABLED = "#0d47a1"
_COLOR_PENDING = "#8a6d1a"


class SoftwareEnableWidget(QWidget):

    enable_requested = pyqtSignal(bool)  # True = enable, False = disable

    def __init__(self, parent=None):
        super().__init__(parent)
        self._confirmed_enabled = True  # assume enabled until told otherwise
        self._pending_target = None     # None if not awaiting a confirmation

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)

        title_label = QLabel("SOFTWARE\nENABLE/DISABLE")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #888; font-size: 10px;")
        layout.addWidget(title_label)

        self._status_label = ColorCodedLabel()
        layout.addWidget(self._status_label)

        self._button = QPushButton()
        self._button.clicked.connect(self._on_button_clicked)
        layout.addWidget(self._button)

        self._refresh()

    # -- public API, called by MainWindow --------------------------------

    def set_ack(self, enabled: bool):
        """Wire to DataSource.signals.software_enable_ack."""
        self._confirmed_enabled = enabled
        self._pending_target = None
        self._refresh()

    # -- internal -----------------------------------------------------

    def _on_button_clicked(self):
        target = not self._confirmed_enabled
        self._pending_target = target
        self._refresh()
        self.enable_requested.emit(target)

    def _refresh(self):
        if self._pending_target is not None:
            text = "Requesting Enable..." if self._pending_target else "Requesting Disable..."
            color = _COLOR_PENDING
        else:
            text = "ENABLED" if self._confirmed_enabled else "DISABLED"
            color = _COLOR_ENABLED if self._confirmed_enabled else _COLOR_DISABLED
        self._status_label.set_state(text, color)

        self._button.setEnabled(self._pending_target is None)
        if self._pending_target is None:
            self._button.setText("Disable" if self._confirmed_enabled else "Enable")
        else:
            self._button.setText("Requesting...")
