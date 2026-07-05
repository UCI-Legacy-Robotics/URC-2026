"""
Evaluate a trained YOLO checkpoint on the held-out test split.

Usage:
    python src/evaluate.py --weights runs/yolo11s_baseline/weights/best.pt
    python src/evaluate.py --weights runs/yolo11s_baseline/weights/best.pt --data data/URC-2024-Object-Detection-6/data.yaml
"""

import argparse
import csv
import json
import shutil
from pathlib import Path

import yaml
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "configs" / "train_config.yaml"
DEFAULT_OUTPUT_DIR = ROOT / "runs" / "evaluation"
PLOT_NAMES = {
    "confusion_matrix.png",
    "confusion_matrix_normalized.png",
    "F1_curve.png",
    "P_curve.png",
    "PR_curve.png",
    "R_curve.png",
}


def load_default_data_yaml() -> Path:
    """Resolve the configured data.yaml, falling back to the first dataset yaml."""
    if DEFAULT_CONFIG.exists():
        with open(DEFAULT_CONFIG) as f:
            config = yaml.safe_load(f) or {}
        configured = ROOT / config.get("data", "data/data.yaml")
        if configured.exists():
            return configured

    candidates = sorted((ROOT / "data").glob("**/data.yaml"))
    if candidates:
        return candidates[0]

    return ROOT / "data" / "data.yaml"


def metric_value(metrics, key: str) -> float:
    """Read an Ultralytics metrics value across minor API differences."""
    results_dict = getattr(metrics, "results_dict", {}) or {}
    if key in results_dict:
        return float(results_dict[key])

    box = getattr(metrics, "box", None)
    fallback_attrs = {
        "metrics/precision(B)": "mp",
        "metrics/recall(B)": "mr",
        "metrics/mAP50(B)": "map50",
        "metrics/mAP50-95(B)": "map",
    }
    attr = fallback_attrs.get(key)
    if box is not None and attr and hasattr(box, attr):
        return float(getattr(box, attr))
    return 0.0


def class_metric_values(metrics) -> list[dict]:
    """Return one row per class with precision, recall, mAP50, and mAP50-95."""
    names = getattr(metrics, "names", {}) or {}
    box = getattr(metrics, "box", None)
    if box is None or not hasattr(box, "maps"):
        return []

    rows = []
    maps = list(getattr(box, "maps", []) or [])
    class_indices = sorted(names) if isinstance(names, dict) else range(len(maps))
    for class_index in class_indices:
        name = names[class_index] if isinstance(names, dict) else str(class_index)
        row = {
            "class_id": int(class_index),
            "class_name": name,
            "map50_95": float(maps[class_index]) if class_index < len(maps) else 0.0,
        }

        for metric_name, source_attr in (
            ("precision", "p"),
            ("recall", "r"),
            ("map50", "ap50"),
        ):
            values = getattr(box, source_attr, None)
            try:
                row[metric_name] = float(values[class_index])
            except (TypeError, IndexError, ValueError):
                row[metric_name] = 0.0
        rows.append(row)
    return rows


def copy_plots(source_dir: Path, output_dir: Path) -> None:
    """Copy Ultralytics validation plots into the evaluation output folder."""
    if not source_dir.exists():
        return

    plots_dir = output_dir / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    for path in source_dir.iterdir():
        if path.name in PLOT_NAMES and path.is_file():
            shutil.copy2(path, plots_dir / path.name)


def write_outputs(output_dir: Path, headline: dict, class_rows: list[dict]) -> None:
    """Persist headline metrics and per-class metrics as JSON and CSV."""
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "metrics.json", "w") as f:
        json.dump({"headline": headline, "per_class": class_rows}, f, indent=2)

    with open(output_dir / "per_class_metrics.csv", "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["class_id", "class_name", "precision", "recall", "map50", "map50_95"],
        )
        writer.writeheader()
        writer.writerows(class_rows)


def evaluate(weights: Path, data_yaml: Path, output_dir: Path, imgsz: int, device: str) -> dict:
    """Run YOLO validation on the test split and save summary artifacts."""
    model = YOLO(str(weights))
    metrics = model.val(
        data=str(data_yaml),
        split="test",
        imgsz=imgsz,
        device=device,
        plots=True,
        project=str(output_dir.parent),
        name=output_dir.name,
        exist_ok=True,
    )

    headline = {
        "precision": metric_value(metrics, "metrics/precision(B)"),
        "recall": metric_value(metrics, "metrics/recall(B)"),
        "map50": metric_value(metrics, "metrics/mAP50(B)"),
        "map50_95": metric_value(metrics, "metrics/mAP50-95(B)"),
    }
    class_rows = class_metric_values(metrics)
    save_dir = Path(getattr(metrics, "save_dir", output_dir))

    write_outputs(output_dir, headline, class_rows)
    copy_plots(save_dir, output_dir)

    print("Test-set metrics")
    for key, value in headline.items():
        print(f"  {key}: {value:.4f}")
    print(f"Saved evaluation artifacts to: {output_dir}")
    return headline


def main():
    parser = argparse.ArgumentParser(description="Evaluate YOLO weights on the test split")
    parser.add_argument("--weights", type=Path, required=True, help="Path to trained best.pt")
    parser.add_argument("--data", type=Path, default=load_default_data_yaml(), help="Path to data.yaml")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_DIR, help="Output directory")
    parser.add_argument("--imgsz", type=int, default=640, help="Evaluation image size")
    parser.add_argument("--device", type=str, default="0", help="Device, e.g. 0 or cpu")
    args = parser.parse_args()

    evaluate(
        weights=args.weights,
        data_yaml=args.data,
        output_dir=args.output,
        imgsz=args.imgsz,
        device=args.device,
    )


if __name__ == "__main__":
    main()
