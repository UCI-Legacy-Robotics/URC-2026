"""
Fake-data publisher for exercising the tuning dashboard without any rover
hardware. Reads the same graphs_config.json the dashboard does and
publishes a waveform on every configured topic: a sine wave whose
amplitude slowly breathes in and out, so the dashboard's Y auto-scaling
is visibly exercised, not just its X-axis scrolling.

Generic over msg_type/field, same as ros_node.py -- if a config entry
gets swapped to a real message type that has a std_msgs/Header, this
stamps it (via the node's clock) the same way ros_node.py's
get_header_stamp reads it; today's std_msgs/Float32 placeholders don't
have one, so publishing falls back to relying on the dashboard's own
wall-clock-arrival timestamping, same as it would for this rover's real
(headerless) motor-controller telemetry.
"""

import argparse
import math
import time

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from graphs_config_loader import load_graphs_config
from msg_resolve import resolve_msg_type, set_field

# Rough per-unit amplitude so the fake waveforms land in a believable
# range for each quantity -- purely cosmetic, falls back to 1.0 for any
# units not listed here.
_AMPLITUDE_BY_UNITS = {
    "deg": 90.0,
    "m": 0.3,
    "m/s": 1.5,
    "cm/s": 10.0,
    "A": 5.0,
}


class TestPublisherNode(Node):
    def __init__(self, config: dict, rate_hz: float):
        super().__init__('tuning_dashboard_test_publisher')
        self._start_time = time.time()
        self._entries = []

        for i, graph in enumerate(config["graphs"]):
            msg_class = resolve_msg_type(graph["msg_type"])
            # BEST_EFFORT, matching TuningNode's subscriptions -- see
            # ros_node.py's docstring for why RELIABLE's heartbeat/
            # acknack overhead matters here.
            publisher = self.create_publisher(msg_class, graph["topic"], qos_profile_sensor_data)
            self._entries.append({
                "graph": graph,
                "msg_class": msg_class,
                "publisher": publisher,
                # Stagger phase/frequency per graph so tiles don't all
                # move in lockstep -- easier to visually distinguish.
                "phase": i * 0.7,
                "freq_hz": 0.1 + 0.03 * (i % 5),
                "amplitude": _AMPLITUDE_BY_UNITS.get(graph["units"], 1.0),
            })

        self.create_timer(1.0 / rate_hz, self._publish_all)
        self.get_logger().info(
            f"Test publisher started, {len(self._entries)} topics at {rate_hz} Hz")

    def _publish_all(self):
        t = time.time() - self._start_time
        for entry in self._entries:
            graph = entry["graph"]
            envelope = 1.0 + 0.4 * math.sin(t / 15.0 + entry["phase"])
            value = entry["amplitude"] * envelope * math.sin(
                2 * math.pi * entry["freq_hz"] * t + entry["phase"])

            msg = entry["msg_class"]()
            set_field(msg, graph["field"], value)
            if hasattr(msg, "header"):
                msg.header.stamp = self.get_clock().now().to_msg()
            entry["publisher"].publish(msg)


def _parse_args():
    parser = argparse.ArgumentParser(description='Tuning Dashboard test data publisher')
    parser.add_argument(
        '--config', type=str, default=None, metavar='PATH',
        help='Path to a graphs_config.json to use instead of the default.',
    )
    parser.add_argument(
        '--rate', type=float, default=20.0, metavar='HZ',
        help='Publish rate per topic, in Hz. Default: 20.',
    )
    return parser.parse_args()


def main():
    args = _parse_args()
    config = load_graphs_config(args.config)

    rclpy.init()
    node = TestPublisherNode(config, args.rate)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
