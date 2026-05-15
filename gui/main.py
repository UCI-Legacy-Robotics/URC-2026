import sys
import threading
import rclpy
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ros_node import BaseStationNode


def main():
    rclpy.init()

    app = QApplication(sys.argv)
    app.setApplicationName('Rover Base Station')

    node = BaseStationNode()
    window = MainWindow(node)
    window.show()

    ros_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    ros_thread.start()

    exit_code = app.exec()

    node.destroy_node()
    rclpy.shutdown()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
