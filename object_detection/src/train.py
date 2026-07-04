"""
Training entry point for YOLOv8/v11 object detection.

Usage:
    python src/train.py
    python src/train.py --config configs/train_config.yaml
"""

import argparse
from pathlib import Path

import yaml
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "configs" / "train_config.yaml"


def load_config(config_path: Path) -> dict:
    """Load training configuration from YAML."""
    with open(config_path) as f:
        return yaml.safe_load(f)


def train(config: dict) -> None:
    """Run YOLO training with the given config."""
    model_name = config.get("model", "yolov8n.pt")
    data_yaml = ROOT / config.get("data", "data/data.yaml")
    epochs = config.get("epochs", 100)
    imgsz = config.get("imgsz", 640)
    batch = config.get("batch", 16)
    project = str(ROOT / config.get("project", "runs"))
    name = config.get("name", "train")
    device = config.get("device", 0)

    model = YOLO(model_name)
    model.train(
        data=str(data_yaml),
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        project=project,
        name=name,
        device=device,
    )


def main():
    parser = argparse.ArgumentParser(description="Train YOLO model")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Path to training config YAML",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    train(config)


if __name__ == "__main__":
    main()
