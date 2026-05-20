import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt


def _ros_image_to_pixmap(msg) -> QPixmap:
    """Convert a sensor_msgs/Image to QPixmap without cv_bridge."""
    arr = np.frombuffer(msg.data, dtype=np.uint8).reshape((msg.height, msg.width, -1))

    enc = msg.encoding.lower()
    if enc in ('bgr8', 'bgr'):
        arr = arr[:, :, ::-1]  # BGR -> RGB
    elif enc in ('mono8', '8uc1'):
        arr = np.stack([arr[:, :, 0]] * 3, axis=-1)
    # rgb8 / rgb is already correct

    arr = np.ascontiguousarray(arr)
    qt_image = QImage(arr.data, msg.width, msg.height, 3 * msg.width,
                      QImage.Format.Format_RGB888)
    # fromImage copies the pixel data so arr can be freed after this line
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
