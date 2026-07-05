"""
Export trained YOLO model: .pt → ONNX → TensorRT engine.

Usage:
    python src/export.py --weights runs/train/weights/best.pt
    python src/export.py --weights runs/train/weights/best.pt --format engine
"""

import argparse
import shutil
from pathlib import Path

from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models"


def export_model(
    weights: Path,
    fmt: str = "onnx",
    imgsz: int = 640,
    half: bool = False,
    device: int = 0,
) -> Path:
    """Export a YOLO .pt checkpoint to the specified format.

    Args:
        weights: Path to .pt weights file.
        fmt: Export format — 'onnx' or 'engine' (TensorRT).
        imgsz: Input image size.
        half: Use FP16 (recommended for TensorRT on Jetson).
        device: GPU device index.

    Returns:
        Path to the exported model file.
    """
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    model = YOLO(str(weights))
    export_path = model.export(
        format=fmt,
        imgsz=imgsz,
        half=half,
        device=device,
    )

    exported = Path(export_path)
    destination = MODELS_DIR / exported.name
    if exported.resolve() != destination.resolve():
        shutil.copy2(exported, destination)

    print(f"Exported model to: {destination}")
    return destination


def main():
    parser = argparse.ArgumentParser(description="Export YOLO model")
    parser.add_argument(
        "--weights",
        type=Path,
        required=True,
        help="Path to .pt weights",
    )
    parser.add_argument(
        "--format",
        type=str,
        default="onnx",
        choices=["onnx", "engine"],
        help="Export format (default: onnx)",
    )
    parser.add_argument("--imgsz", type=int, default=640, help="Image size")
    parser.add_argument("--half", action="store_true", help="FP16 export")
    parser.add_argument("--device", type=int, default=0, help="GPU device")
    args = parser.parse_args()

    export_model(
        weights=args.weights,
        fmt=args.format,
        imgsz=args.imgsz,
        half=args.half,
        device=args.device,
    )


if __name__ == "__main__":
    main()
