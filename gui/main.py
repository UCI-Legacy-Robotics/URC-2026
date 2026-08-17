import argparse
import os
import signal
import sys
import threading
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.camera_window import CameraWindow

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
    parser.add_argument(
        '--primary-screen', type=int, default=0, metavar='N',
        help='Screen index for the primary window (see --list-screens). Default: 0.',
    )
    parser.add_argument(
        '--camera-screen', type=int, default=1, metavar='N',
        help='Screen index for the camera window (see --list-screens). Default: 1.',
    )
    parser.add_argument(
        '--list-screens', action='store_true',
        help='List detected screens (index, name, resolution) and exit — use this '
             'to find the right indices for --primary-screen/--camera-screen when '
             'more than 2 monitors are connected (e.g. a laptop plus two externals).',
    )
    return parser.parse_args()


def _print_screens(app):
    primary = app.primaryScreen()
    for i, screen in enumerate(app.screens()):
        geo = screen.availableGeometry()
        marker = '  (OS primary)' if screen is primary else ''
        print(f'  [{i}] {screen.name()}  {geo.width()}x{geo.height()}+{geo.x()}+{geo.y()}{marker}')


def main():
    args = _parse_args()

    app = QApplication(sys.argv)
    app.setApplicationName('Rover Base Station')
    app.setStyleSheet(_STYLESHEET)

    if args.list_screens:
        _print_screens(app)
        sys.exit(0)

    # Qt's event loop is a blocking C++ call, so Python never gets a
    # chance to run a signal handler while app.exec() is running —
    # Ctrl+C is silently swallowed by default. quit() on SIGINT plus a
    # no-op periodic timer (just to hand control back to the Python
    # interpreter regularly) is the standard PyQt fix.
    signal.signal(signal.SIGINT, lambda *_: app.quit())
    _sigint_pump = QTimer()
    _sigint_pump.timeout.connect(lambda: None)
    _sigint_pump.start(200)

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
    camera_window = CameraWindow(data_source)

    screens = app.screens()
    primary_idx, camera_idx = args.primary_screen, args.camera_screen
    indices_valid = (
        0 <= primary_idx < len(screens)
        and 0 <= camera_idx < len(screens)
        and primary_idx != camera_idx
    )

    if indices_valid:
        # Real deployment (2, or 3+ with explicit --primary-screen/
        # --camera-screen — e.g. a laptop plus two external monitors):
        # each window fullscreen on its own chosen monitor. Move-then-
        # maximize rather than a direct setScreen() call, since a
        # widget has no native window (and hence no assignable
        # QScreen) until it's shown — moving first onto the target
        # screen's geometry is what makes showMaximized() land there
        # instead of wherever Qt would otherwise default to.
        window.move(screens[primary_idx].availableGeometry().topLeft())
        window.showMaximized()
        camera_window.move(screens[camera_idx].availableGeometry().topLeft())
        camera_window.showMaximized()
    else:
        # Dev machines often don't have a second monitor, and a bad
        # --primary-screen/--camera-screen index (run --list-screens to
        # see valid ones) shouldn't crash — tile both windows side by
        # side on one screen so the camera window is still usable/
        # testable rather than fully hidden behind the maximized
        # primary window.
        if len(screens) <= 1:
            print('WARNING: only one screen detected — tiling camera window '
                  'next to the primary window instead of a second monitor.')
        else:
            print(f'WARNING: --primary-screen={primary_idx}/--camera-screen={camera_idx} '
                  f'invalid for {len(screens)} detected screens (run --list-screens to see '
                  f'valid indices) — falling back to tiling both windows on one screen.')
        avail = screens[0].availableGeometry()
        half_width = avail.width() // 2
        window.setGeometry(avail.x(), avail.y(), half_width, avail.height())
        window.show()
        camera_window.setGeometry(
            avail.x() + half_width, avail.y(), avail.width() - half_width, avail.height())
        camera_window.show()

    exit_code = app.exec()

    data_source.stop()
    if rclpy is not None:
        rclpy.shutdown()

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
