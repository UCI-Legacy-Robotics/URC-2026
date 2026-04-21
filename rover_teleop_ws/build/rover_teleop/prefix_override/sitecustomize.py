import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/lenat/URC-2026/rover_teleop_ws/install/rover_teleop'
