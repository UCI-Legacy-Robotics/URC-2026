"""
Inference with a TensorRT engine or ONNX model.

Designed for deployment on Jetson / ROS2 nodes.

Usage:
    python src/inference.py --model models/best.engine --source 0
    python src/inference.py --model models/best.onnx --source image.jpg
"""

import argparse
from pathlib import Path

from ultralytics import YOLO


def run_inference(
    model_path: Path,
    source: str = "0",
    imgsz: int = 640,
    conf: float = 0.25,
    device: int = 0,
    show: bool = False,
) -> list:
    """Run object detection inference.

    Args:
        model_path: Path to .engine, .onnx, or .pt model.
        source: Image path, video path, or camera index (as string).
        imgsz: Inference image size.
        conf: Confidence threshold.
        device: GPU device index.
        show: Display results in a window.

    Returns:
        List of ultralytics Results objects.
    """
    model = YOLO(str(model_path))
    results = model.predict(
        source=source,
        imgsz=imgsz,
        conf=conf,
        device=device,
        show=show,
    )
    return results


def main():
    parser = argparse.ArgumentParser(description="Run YOLO inference")
    parser.add_argument(
        "--model",
        type=Path,
        required=True,
        help="Path to model (.engine, .onnx, or .pt)",
    )
    parser.add_argument(
        "--source",
        type=str,
        default="0",
        help="Image/video path or camera index",
    )
    parser.add_argument("--imgsz", type=int, default=640, help="Image size")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold")
    parser.add_argument("--device", type=int, default=0, help="GPU device")
    parser.add_argument("--show", action="store_true", help="Display results")
    args = parser.parse_args()

    results = run_inference(
        model_path=args.model,
        source=args.source,
        imgsz=args.imgsz,
        conf=args.conf,
        device=args.device,
        show=args.show,
    )

    for r in results:
        print(r.boxes)


if __name__ == "__main__":
    main()
