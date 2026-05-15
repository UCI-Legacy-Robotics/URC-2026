import sys
import threading
import rclpy
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ros_node import BaseStationNode

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


def main():
    rclpy.init()

    app = QApplication(sys.argv)
    app.setApplicationName('Rover Base Station')
    app.setStyleSheet(_STYLESHEET)

    node = BaseStationNode()
    window = MainWindow(node)
    window.showFullScreen()

    ros_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    ros_thread.start()

    exit_code = app.exec()

    node.destroy_node()
    rclpy.shutdown()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
