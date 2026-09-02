"""
Resolves the string-typed pieces of a graphs_config.json entry into
actual Python objects: the ROS message class itself, the numeric value
inside a message instance, and (when present) its header timestamp.

Kept dependency-free from Qt/rclpy specifics on purpose -- ros_node.py and
graphs_config_loader.py both import this, and the loader needs to use it
without a live ROS graph.
"""

import functools
import importlib


def resolve_msg_type(msg_type: str):
    """"pkg/msg/Type" -> the message class, e.g. "std_msgs/msg/Float32"
    -> std_msgs.msg.Float32. Raises ValueError (not ImportError/
    AttributeError) on anything malformed, so callers can surface one
    exception type regardless of what went wrong."""
    parts = msg_type.split("/")
    if len(parts) != 3:
        raise ValueError(f"msg_type {msg_type!r} must look like 'pkg/msg/Type'")
    package, middle, type_name = parts
    module_name = f"{package}.{middle}"
    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        raise ValueError(f"msg_type {msg_type!r}: cannot import {module_name!r} ({e})")
    try:
        return getattr(module, type_name)
    except AttributeError:
        raise ValueError(f"msg_type {msg_type!r}: {module_name!r} has no {type_name!r}")


def get_field(msg, field: str):
    """Dotted-path attribute lookup, e.g. field="twist.twist.linear.x".
    Raises ValueError (not AttributeError) on a missing attribute."""
    try:
        return functools.reduce(getattr, field.split("."), msg)
    except AttributeError as e:
        raise ValueError(f"field {field!r} not found on {type(msg).__name__} ({e})")


def set_field(msg, field: str, value):
    """Dotted-path attribute set, the write-side counterpart to
    get_field -- used by test_publisher.py to fill in the same field
    path a graph's config says to read. Raises ValueError (not
    AttributeError) on a missing attribute, same convention as get_field."""
    parts = field.split(".")
    try:
        target = functools.reduce(getattr, parts[:-1], msg)
        setattr(target, parts[-1], value)
    except AttributeError as e:
        raise ValueError(f"field {field!r} not found on {type(msg).__name__} ({e})")


def get_header_stamp(msg):
    """Returns the message's header timestamp in seconds (float), or None
    if it has no std_msgs/Header -- most of this rover's own telemetry
    messages (ControllerStatus, ODriveStatus, ...) don't carry one, so
    None is the expected common case, not an error."""
    header = getattr(msg, "header", None)
    stamp = getattr(header, "stamp", None)
    if stamp is None:
        return None
    return stamp.sec + stamp.nanosec * 1e-9
