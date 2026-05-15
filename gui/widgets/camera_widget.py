from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt
from cv_bridge import CvBridge


class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.bridge = CvBridge()
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
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')
            h, w, ch = cv_image.shape
            qt_image = QImage(cv_image.data, w, h, ch * w, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image).scaled(
                self.label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.label.setPixmap(pixmap)
        except Exception as e:
            self.label.setText(f'Camera error: {e}')
