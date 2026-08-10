import argparse
import os
import sys
import threading
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

# WSL2: Fast-DDS shared memory transport segfaults; force UDP-only.
os.environ.setdefault(
    'FASTRTPS_DEFAULT_PROFILES_FILE',
    os.path.join(os.path.dirname(__file__), 'fastdds_no_shm.xml'),
)

# WSL2: QtWebEngine's GPU compositor (used by the GNSS map widget) fails
# to share buffers over WSL2's virtualized GPU ("Failed to get native
# pixmap due to dma_buf acquisition failure", "Backend texture is not a
# Vulkan texture") — force software rendering. setdefault so a machine
# with working GPU passthrough can still override this before launch.
os.environ.setdefault('QTWEBENGINE_CHROMIUM_FLAGS', '--disable-gpu')

_STYLESHEET = """
    QWidget {
        background-color: #0a0a0a;
        color: #e0e0e0;
    }
    QTabWidget::pane {
        border: 1px solid #2a2a2a;
    }
    QTabBar::tab {
        background: #141414;
        color: #777;
        padding: 8px 24px;
        border: 1px solid #2a2a2a;
    }
    QTabBar::tab:selected {
        background: #1e1e1e;
        color: #ffffff;
        border-bottom: 2px solid #4a9eff;
    }
    QTabBar::tab:hover:!selected {
        background: #1a1a1a;
        color: #aaa;
    }
    QLabel {
        background: transparent;
    }
    QTextEdit {
        border: 1px solid #2a2a2a;
    }
"""


def _parse_args():
    parser = argparse.ArgumentParser(description='Rover Base Station GUI')
    parser.add_argument(
        '--sim', action='store_true',
        help='Run against SimulationDataSource instead of live ROS '
             '(no rclpy/ROS install required).',
    )
    return parser.parse_args()


def main():
    args = _parse_args()

    app = QApplication(sys.argv)
    app.setApplicationName('Rover Base Station')
    app.setStyleSheet(_STYLESHEET)

    rclpy = None
    ros_thread = None

    if args.sim:
        from simulation_data_source import SimulationDataSource
        data_source = SimulationDataSource()
    else:
        import rclpy
        from ros_node import RosDataSource
        rclpy.init()
        data_source = RosDataSource()
        ros_thread = threading.Thread(
            target=rclpy.spin, args=(data_source.node,), daemon=True)
        ros_thread.start()

    data_source.start()

    window = MainWindow(data_source)
    window.showMaximized()

    exit_code = app.exec()

    data_source.stop()
    if rclpy is not None:
        rclpy.shutdown()

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
