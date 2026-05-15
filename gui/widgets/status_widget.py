from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit


class StatusWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        title = QLabel('System Status')
        title.setStyleSheet('font-size: 18px; font-weight: bold;')
        layout.addWidget(title)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setStyleSheet('background: #111; color: #0f0; font-family: monospace;')
        layout.addWidget(self.log)

    def on_diagnostics(self, msg):
        lines = [f'[{s.name}] {s.message}' for s in msg.status]
        self.log.append('\n'.join(lines))
