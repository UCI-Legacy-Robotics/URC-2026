"""
Public inference API for ROS2 / Jetson integration.

This module is the boundary between the training pipeline and anything that
consumes a trained model. Callers get plain dataclasses back, never Ultralytics
objects, so a ROS node can depend on this module without depending on
Ultralytics or on how the model was trained.

Usage:
    from object_detection.detector_api import Detector

    # Load once, e.g. in a ROS node's __init__.
    detector = Detector("models/best.engine", conf=0.25, imgsz=640, device=0)

    # Call per frame, e.g. in an image callback.
    for detection in detector.detect(frame):   # frame: BGR numpy array
        print(detection.class_name, detection.confidence, detection.bbox)

For standalone CLI testing outside ROS, use src/inference.py instead.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Union

import numpy as np


@dataclass
class Detection:
    """One detected object, in pixel coordinates.

    Plain data with no Ultralytics types, so it converts trivially into a ROS
    message (e.g. vision_msgs/Detection2D) or any serialization format.
    """

    class_name: str
    class_id: int
    confidence: float
    bbox: tuple[int, int, int, int]  # x1, y1, x2, y2


def _class_name(names: Any, class_id: int) -> str:
    """Look up a class name, tolerating the dict or list forms Ultralytics uses."""
    if isinstance(names, dict):
        return str(names.get(class_id, class_id))
    try:
        return str(names[class_id])
    except (TypeError, IndexError, KeyError):
        return str(class_id)


class Detector:
    """A loaded YOLO model that runs detection on individual frames.

    The model is loaded once in __init__ rather than per call: loading takes
    seconds, which is unusable in a ROS callback running at 15-30 Hz.
    """

    def __init__(
        self,
        model_path: Union[str, Path],
        conf: float = 0.25,
        imgsz: int = 640,
        device: Union[int, str] = 0,
    ) -> None:
        """
        Args:
            model_path: Path to a .pt, .onnx, or .engine model. Ultralytics
                picks the runtime from the file extension, so the same call
                works for a PyTorch checkpoint, ONNX, or a TensorRT engine.
            conf: Confidence threshold. Detections below this are dropped.
            imgsz: Inference input resolution. For a .engine file this must
                match the imgsz the model was exported with.
            device: GPU index (0), or "cpu" / "mps" where no CUDA device exists.
        """
        # Imported here rather than at module scope so importing the package
        # stays cheap — same reasoning as yolo_model_factory.create_model().
        from ultralytics import YOLO

        self.model_path = Path(model_path)
        self.conf = conf
        self.imgsz = imgsz
        self.device = device
        self.model = YOLO(str(self.model_path))

    def detect(self, image: np.ndarray) -> list[Detection]:
        """Run detection on a single frame.

        Args:
            image: BGR numpy array, e.g. from
                cv_bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8"). Passed
                straight through, so there is no filesystem round-trip.

        Returns:
            One Detection per object above the confidence threshold. Empty list
            when nothing is detected.
        """
        results = self.model.predict(
            source=image,
            imgsz=self.imgsz,
            conf=self.conf,
            device=self.device,
            verbose=False,  # per-frame Ultralytics output would flood ROS logs
        )
        return self._parse_results(results)

    @staticmethod
    def _parse_results(results) -> list[Detection]:
        """Convert Ultralytics Results into plain Detection records."""
        detections: list[Detection] = []
        for result in results:
            boxes = getattr(result, "boxes", None)
            if boxes is None:
                continue
            names = getattr(result, "names", {})
            for box in boxes:
                class_id = int(box.cls)
                x1, y1, x2, y2 = (int(value) for value in box.xyxy[0])
                detections.append(
                    Detection(
                        class_name=_class_name(names, class_id),
                        class_id=class_id,
                        confidence=float(box.conf),
                        bbox=(x1, y1, x2, y2),
                    )
                )
        return detections
