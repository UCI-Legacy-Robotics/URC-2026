import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/pi/Legacy/URC-2026/drive_ros2_ws/install/drive_manager'
