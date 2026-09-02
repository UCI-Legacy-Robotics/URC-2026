"""
ROS2 side of the tuning dashboard.

TuningNode is a plain rclpy.Node -- no Qt dependency at all. It runs in
its own OS process (see ros_worker.py), separate from the Qt GUI
process.

Context: with 19 live subscriptions, the GUI thread was observed
stalling for 500ms-1.8s at a time (buttons unresponsive, window
wouldn't close). Redraw throttling, executor type (Single- vs
MultiThreadedExecutor), publish rate (5 vs 20Hz), GIL switch interval,
and BEST_EFFORT QoS (below) were all tried; none fully resolved it in
isolated sandbox testing, though each is a real improvement kept on its
own merits. Running ROS in a separate process removes GIL-sharing with
Qt as a possible contributor, but wasn't confirmed as a complete fix
either -- this needs verifying against the real windowed app, not just
these synthetic tests.
"""

import time

from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from msg_resolve import resolve_msg_type, get_field, get_header_stamp


class TuningNode(Node):
    """Subscribes to every graph in the loaded config and calls
    on_sample(graph_id, t_relative, value) for each message received.

    t_relative is zeroed independently per graph_id, against that
    graph's own first-received timestamp -- not a single dashboard-wide
    zero point -- since different topics can start publishing at
    different times (e.g. a subsystem node starting late). Uses the
    message's header stamp when present, else wall-clock arrival time
    (the common case for this rover's telemetry -- see msg_resolve.py).
    """

    def __init__(self, config: dict, on_sample):
        super().__init__('tuning_dashboard')
        self._on_sample = on_sample
        self._first_t = {}  # graph_id -> first timestamp (seconds), for zeroing t_relative

        for graph in config['graphs']:
            msg_class = resolve_msg_type(graph['msg_type'])
            # BEST_EFFORT, not the RELIABLE default -- a lost sample on a
            # rolling tuning display doesn't matter, and it avoids
            # RELIABLE's per-endpoint heartbeat/acknack protocol
            # overhead (which runs continuously regardless of whether
            # new data is published) as a possible contributor to the
            # GUI-thread stalls described in this module's docstring.
            # Same QoS gui/ros_node.py already uses for its own
            # high-rate IMU subscription -- correct for this kind of
            # data regardless of whether it turns out to be the fix.
            self.create_subscription(
                msg_class, graph['topic'],
                self._make_handler(graph['id'], graph['field']),
                qos_profile_sensor_data)

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
            self._on_sample(graph_id, t - first_t, float(value))
        return handler
