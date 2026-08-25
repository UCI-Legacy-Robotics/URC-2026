"""
Shared camera-frame decode helper.

Extracted out of widgets/camera_feed_widget.py's _frame_to_pixmap so
non-widget code (science_data_store.py, saving a science_image event to
disk) can decode the same normalized frame payload without importing a
QWidget subclass just to reach a free function.
"""

import cv2
import numpy as np


def decode_frame_to_rgb(frame) -> np.ndarray:
    """Decode a normalized camera_frame/science_image payload
    (SimpleNamespace with encoding/data/height/width — see
    DataSourceSignals in data_source.py) into an RGB numpy array.
    Manual numpy/cv2 decode, no cv_bridge (cv_bridge isn't used
    anywhere in the GUI process)."""
    enc = frame.encoding.lower()
    arr = np.frombuffer(frame.data, dtype=np.uint8)

    if enc in ('rgb8', 'rgb'):
        rgb = arr.reshape((frame.height, frame.width, 3))
    elif enc in ('bgr8', 'bgr'):
        rgb = cv2.cvtColor(arr.reshape((frame.height, frame.width, 3)), cv2.COLOR_BGR2RGB)
    elif enc in ('mono8', '8uc1'):
        rgb = cv2.cvtColor(arr.reshape((frame.height, frame.width)), cv2.COLOR_GRAY2RGB)
    elif enc in ('yuv422', 'yuv422_yuy2', 'yuyv'):
        rgb = cv2.cvtColor(arr.reshape((frame.height, frame.width, 2)), cv2.COLOR_YUV2RGB_YUYV)
    elif enc in ('mono16', '16uc1'):
        gray16 = arr.view(np.uint16).reshape((frame.height, frame.width))
        gray8 = (gray16 >> 8).astype(np.uint8)
        rgb = cv2.cvtColor(gray8, cv2.COLOR_GRAY2RGB)
    else:
        raise ValueError(f'Unsupported encoding: {frame.encoding}')

    return np.ascontiguousarray(rgb)
