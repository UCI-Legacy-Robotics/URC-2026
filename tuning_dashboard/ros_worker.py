"""
Entry point run in a separate OS process (spawned by main.py via
multiprocessing.Process) -- owns rclpy and TuningNode entirely on its
own, with no Qt involved at all. Every sample is pushed onto a
multiprocessing.Queue as a plain (graph_id, t_relative, value) tuple;
the Qt process drains it on a timer (see main.py). This is the fix for
the GIL-starvation issue described in ros_node.py's docstring -- ROS
and Qt no longer share a interpreter, so 19 live subscriptions can't
starve the GUI thread.
"""

import rclpy

from ros_node import TuningNode


def run(config: dict, queue):
    rclpy.init()
    node = TuningNode(config, on_sample=lambda gid, t, v: queue.put((gid, t, v)))
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
