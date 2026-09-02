import argparse
import multiprocessing
import queue
import signal
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from graphs_config_loader import load_graphs_config
from ros_worker import run as run_ros_worker
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

# How often the Qt process drains the sample queue -- independent of
# ROS's actual publish rate, same reasoning as RollingPlotWidget's
# redraw throttling.
_QUEUE_DRAIN_INTERVAL_MS = 30
# Safety bound on samples drained per tick, in case the ROS process
# ever gets far ahead of the GUI -- keeps one tick from blocking
# indefinitely rather than assuming that can't happen.
_MAX_DRAIN_PER_TICK = 5000


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

    # ROS runs in its own process, not a thread in this one -- see
    # ros_node.py's docstring for the GUI-responsiveness investigation
    # behind this.
    sample_queue = multiprocessing.Queue()
    ros_process = multiprocessing.Process(
        target=run_ros_worker, args=(config, sample_queue), daemon=True)
    ros_process.start()

    window = MainWindow(config)
    window.resize(1600, 900)
    window.show()

    def drain_queue():
        for _ in range(_MAX_DRAIN_PER_TICK):
            try:
                graph_id, t_relative, value = sample_queue.get_nowait()
            except queue.Empty:
                return
            window.on_sample(graph_id, t_relative, value)

    drain_timer = QTimer()
    drain_timer.timeout.connect(drain_queue)
    drain_timer.start(_QUEUE_DRAIN_INTERVAL_MS)

    exit_code = app.exec()

    ros_process.terminate()
    ros_process.join(timeout=2)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
