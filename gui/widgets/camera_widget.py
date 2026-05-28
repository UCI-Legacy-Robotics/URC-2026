import numpy as np
import cv2
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt


def _ros_image_to_pixmap(msg) -> QPixmap:
    enc = msg.encoding.lower()
    # Copy data immediately so DDS can't reclaim the buffer under us
    arr = np.frombuffer(bytes(msg.data), dtype=np.uint8)

    if enc in ('rgb8', 'rgb'):
        rgb = arr.reshape((msg.height, msg.width, 3))
    elif enc in ('bgr8', 'bgr'):
        rgb = cv2.cvtColor(arr.reshape((msg.height, msg.width, 3)), cv2.COLOR_BGR2RGB)
    elif enc in ('mono8', '8uc1'):
        rgb = cv2.cvtColor(arr.reshape((msg.height, msg.width)), cv2.COLOR_GRAY2RGB)
    elif enc in ('yuv422', 'yuv422_yuy2', 'yuyv'):
        rgb = cv2.cvtColor(arr.reshape((msg.height, msg.width, 2)), cv2.COLOR_YUV2RGB_YUYV)
    elif enc in ('mono16', '16uc1'):
        gray16 = arr.view(np.uint16).reshape((msg.height, msg.width))
        gray8 = (gray16 >> 8).astype(np.uint8)
        rgb = cv2.cvtColor(gray8, cv2.COLOR_GRAY2RGB)
    else:
        raise ValueError(f'Unsupported encoding: {msg.encoding}')

    rgb = np.ascontiguousarray(rgb)
    h, w, _ = rgb.shape
    qt_image = QImage(rgb.data, w, h, rgb.strides[0], QImage.Format.Format_RGB888)
    return QPixmap.fromImage(qt_image)


class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(750, 750)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet('CameraWidget { background-color: #1a1a1a; border-radius: 6px; }')

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel('No camera feed')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet(
            'background: transparent; color: #333; font-size: 13px; font-family: monospace;'
        )
        layout.addWidget(self.label)

    def on_frame(self, msg):
        try:
            pixmap = _ros_image_to_pixmap(msg).scaled(
                self.label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.label.setPixmap(pixmap)
        except Exception as e:
            self.label.setText(f'Camera error: {e}')
