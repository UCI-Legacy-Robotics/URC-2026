import argparse
import signal
import sys
import threading

import rclpy
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from graphs_config_loader import load_graphs_config
from ros_node import TuningNode
from ui.main_window import MainWindow

_STYLESHEET = """
    QWidget {
        background-color: #0a0a0a;
        color: #e0e0e0;
    }
    QPushButton {
        background: #1e1e1e;
        border: 1px solid #2a2a2a;
        padding: 6px 16px;
    }
    QPushButton:hover {
        background: #2a2a2a;
    }
    QLabel {
        background: transparent;
    }
"""


def _parse_args():
    parser = argparse.ArgumentParser(description='ROS2 Tuning Dashboard')
    parser.add_argument(
        '--config', type=str, default=None, metavar='PATH',
        help='Path to a graphs_config.json to use instead of the default '
             '(tuning_dashboard/graphs_config.json).',
    )
    return parser.parse_args()


def main():
    args = _parse_args()
    config = load_graphs_config(args.config)

    app = QApplication(sys.argv)
    app.setApplicationName('Tuning Dashboard')
    app.setStyleSheet(_STYLESHEET)

    # Same Ctrl+C fix as gui/main.py -- Qt's blocking event loop otherwise
    # swallows SIGINT.
    signal.signal(signal.SIGINT, lambda *_: app.quit())
    _sigint_pump = QTimer()
    _sigint_pump.timeout.connect(lambda: None)
    _sigint_pump.start(200)

    rclpy.init()
    node = TuningNode(config)
    ros_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    ros_thread.start()

    window = MainWindow(config)
    node.signals.sample.connect(window.on_sample)
    window.resize(1600, 900)
    window.show()

    exit_code = app.exec()

    node.destroy_node()
    rclpy.shutdown()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
