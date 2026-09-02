"""
ROS2 side of the tuning dashboard.

TuningNode is a plain rclpy.Node (no Qt inheritance) -- same split as
gui/ros_node.py's BaseStationNode -- that builds one subscription per
graphs_config.json entry and emits everything through a single
multiplexed Qt signal, the same multiplexing convention gui/data_source.py
uses for camera_frame/science_reading (one signal shape, tagged by id,
rather than one signal per topic).
"""

import time

from PyQt6.QtCore import QObject, pyqtSignal
from rclpy.node import Node

from msg_resolve import resolve_msg_type, get_field, get_header_stamp


class TuningDashboardSignals(QObject):
    # (graph_id, t_relative_seconds, value)
    sample = pyqtSignal(str, float, float)


class TuningNode(Node):
    """Subscribes to every graph in the loaded config and emits
    signals.sample for each message received.

    t_relative is zeroed independently per graph_id, against that
    graph's own first-received timestamp -- not a single dashboard-wide
    zero point -- since different topics can start publishing at
    different times (e.g. a subsystem node starting late). Uses the
    message's header stamp when present, else wall-clock arrival time
    (the common case for this rover's telemetry -- see msg_resolve.py).
    """

    def __init__(self, config: dict):
        super().__init__('tuning_dashboard')
        self.signals = TuningDashboardSignals()
        self._first_t = {}  # graph_id -> first timestamp (seconds), for zeroing t_relative

        for graph in config['graphs']:
            msg_class = resolve_msg_type(graph['msg_type'])
            self.create_subscription(
                msg_class, graph['topic'],
                self._make_handler(graph['id'], graph['field']), 10)

        self.get_logger().info(
            f"Tuning dashboard node started, {len(config['graphs'])} subscriptions")

    def _make_handler(self, graph_id: str, field: str):
        def handler(msg):
            t = get_header_stamp(msg)
            if t is None:
                t = time.time()

            first_t = self._first_t.get(graph_id)
            if first_t is None:
                first_t = t
                self._first_t[graph_id] = first_t

            value = get_field(msg, field)
            self.signals.sample.emit(graph_id, t - first_t, float(value))
        return handler
