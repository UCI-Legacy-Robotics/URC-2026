"""
Surface actionable YOLO failures on the held-out test split.

The script compares predictions against YOLO-format labels and saves annotated
examples for false positives, false negatives, and low-confidence matches.

Usage:
    python src/failure_analysis.py --weights runs/yolo11s_baseline/weights/best.pt
"""

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import cv2
import yaml
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "configs" / "train_config.yaml"
DEFAULT_OUTPUT_DIR = ROOT / "runs" / "failure_analysis"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


@dataclass
class Box:
    class_id: int
    xyxy: tuple[float, float, float, float]
    confidence: Optional[float] = None


def load_default_data_yaml() -> Path:
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


def load_dataset_config(data_yaml: Path) -> dict:
    with open(data_yaml) as f:
        return yaml.safe_load(f) or {}


def resolve_split_images(data_yaml: Path, split: str = "test") -> Path:
    config = load_dataset_config(data_yaml)
    raw_path = Path(config[split])
    if raw_path.is_absolute():
        return raw_path

    candidates = [
        (data_yaml.parent / raw_path).resolve(),
        (ROOT / raw_path).resolve(),
        (data_yaml.parent / split / "images").resolve(),
        (ROOT / "data" / split / "images").resolve(),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def image_paths(images_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in images_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def label_path_for(image_path: Path) -> Path:
    parts = list(image_path.parts)
    if "images" in parts:
        parts[parts.index("images")] = "labels"
        return Path(*parts).with_suffix(".txt")
    return image_path.parent.parent / "labels" / f"{image_path.stem}.txt"


def read_labels(label_path: Path, image_shape: tuple[int, int, int]) -> tuple[list[Box], int]:
    height, width = image_shape[:2]
    boxes = []
    invalid_count = 0
    if not label_path.exists():
        return boxes, invalid_count

    for line in label_path.read_text().splitlines():
        values = line.strip().split()
        if len(values) != 5:
            invalid_count += 1
            continue
        try:
            class_id = int(float(values[0]))
            x_center, y_center, box_width, box_height = map(float, values[1:])
        except ValueError:
            invalid_count += 1
            continue
        x1 = (x_center - box_width / 2) * width
        y1 = (y_center - box_height / 2) * height
        x2 = (x_center + box_width / 2) * width
        y2 = (y_center + box_height / 2) * height
        boxes.append(Box(class_id=class_id, xyxy=(x1, y1, x2, y2)))
    return boxes, invalid_count


def prediction_boxes(result) -> list[Box]:
    if result.boxes is None:
        return []

    xyxy = result.boxes.xyxy.cpu().tolist()
    classes = result.boxes.cls.cpu().tolist()
    confidences = result.boxes.conf.cpu().tolist()
    return [
        Box(class_id=int(class_id), xyxy=tuple(coords), confidence=float(confidence))
        for coords, class_id, confidence in zip(xyxy, classes, confidences)
    ]


def iou(first: Box, second: Box) -> float:
    ax1, ay1, ax2, ay2 = first.xyxy
    bx1, by1, bx2, by2 = second.xyxy
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    intersection = max(0.0, ix2 - ix1) * max(0.0, iy2 - iy1)
    first_area = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    second_area = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    union = first_area + second_area - intersection
    return intersection / union if union else 0.0


def match_boxes(labels: list[Box], predictions: list[Box], iou_threshold: float) -> tuple[list[tuple[int, int, float]], set[int], set[int]]:
    candidates = []
    for label_index, label in enumerate(labels):
        for prediction_index, prediction in enumerate(predictions):
            if label.class_id != prediction.class_id:
                continue
            overlap = iou(label, prediction)
            if overlap >= iou_threshold:
                candidates.append((overlap, label_index, prediction_index))

    matches = []
    matched_labels: set[int] = set()
    matched_predictions: set[int] = set()
    for overlap, label_index, prediction_index in sorted(candidates, reverse=True):
        if label_index in matched_labels or prediction_index in matched_predictions:
            continue
        matched_labels.add(label_index)
        matched_predictions.add(prediction_index)
        matches.append((label_index, prediction_index, overlap))

    return matches, matched_labels, matched_predictions


def draw_box(image, box: Box, label: str, color: tuple[int, int, int]) -> None:
    x1, y1, x2, y2 = [int(round(value)) for value in box.xyxy]
    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
    cv2.putText(
        image,
        label,
        (x1, max(16, y1 - 6)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        color,
        2,
        cv2.LINE_AA,
    )


def class_name(names, class_id: int) -> str:
    if isinstance(names, dict):
        return str(names.get(class_id, class_id))
    if isinstance(names, list) and class_id < len(names):
        return str(names[class_id])
    return str(class_id)


def save_case(
    image_path: Path,
    image,
    labels: list[Box],
    predictions: list[Box],
    issue: str,
    output_dir: Path,
    names,
) -> Path:
    annotated = image.copy()
    for label in labels:
        draw_box(annotated, label, f"gt {class_name(names, label.class_id)}", (0, 180, 0))
    for prediction in predictions:
        pred_label = f"pred {class_name(names, prediction.class_id)} {prediction.confidence:.2f}"
        draw_box(annotated, prediction, pred_label, (0, 140, 255))

    destination = output_dir / issue / image_path.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(destination), annotated)
    return destination


def analyze_failures(
    weights: Path,
    data_yaml: Path,
    output_dir: Path,
    imgsz: int,
    conf: float,
    iou_threshold: float,
    low_confidence: float,
    device: str,
    max_cases: int,
) -> dict:
    images_dir = resolve_split_images(data_yaml)
    paths = image_paths(images_dir)
    if not paths:
        raise FileNotFoundError(f"No test images found under {images_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    model = YOLO(str(weights))
    names = model.names
    case_rows = []
    summary = {
        "images": 0,
        "false_positive_images": 0,
        "false_negative_images": 0,
        "low_confidence_images": 0,
        "false_positives": 0,
        "false_negatives": 0,
        "low_confidence_matches": 0,
        "invalid_label_rows": 0,
    }

    for image_path in paths:
        if max_cases and len(case_rows) >= max_cases:
            break

        image = cv2.imread(str(image_path))
        if image is None:
            continue

        result = model.predict(
            source=str(image_path),
            imgsz=imgsz,
            conf=conf,
            device=device,
            verbose=False,
        )[0]
        labels, invalid_label_rows = read_labels(label_path_for(image_path), image.shape)
        predictions = prediction_boxes(result)
        matches, matched_labels, matched_predictions = match_boxes(labels, predictions, iou_threshold)

        false_negatives = [labels[index] for index in range(len(labels)) if index not in matched_labels]
        false_positives = [predictions[index] for index in range(len(predictions)) if index not in matched_predictions]
        low_confidence_matches = [
            predictions[prediction_index]
            for _, prediction_index, _ in matches
            if (predictions[prediction_index].confidence or 0.0) < low_confidence
        ]

        issues = {
            "false_negatives": false_negatives,
            "false_positives": false_positives,
            "low_confidence": low_confidence_matches,
        }
        saved = []
        for issue, boxes in issues.items():
            if not boxes:
                continue
            if max_cases and len(case_rows) >= max_cases:
                break
            saved_path = save_case(image_path, image, labels, predictions, issue, output_dir, names)
            saved.append(str(saved_path.relative_to(output_dir)))
            case_rows.append(
                {
                    "image": str(image_path),
                    "issue": issue,
                    "count": len(boxes),
                    "artifact": str(saved_path),
                }
            )

        summary["images"] += 1
        summary["false_positives"] += len(false_positives)
        summary["false_negatives"] += len(false_negatives)
        summary["low_confidence_matches"] += len(low_confidence_matches)
        summary["invalid_label_rows"] += invalid_label_rows
        summary["false_positive_images"] += int(bool(false_positives))
        summary["false_negative_images"] += int(bool(false_negatives))
        summary["low_confidence_images"] += int(bool(low_confidence_matches))

    with open(output_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    with open(output_dir / "cases.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["image", "issue", "count", "artifact"])
        writer.writeheader()
        writer.writerows(case_rows)

    print(f"Analyzed {summary['images']} test images")
    print(f"False positives: {summary['false_positives']}")
    print(f"False negatives: {summary['false_negatives']}")
    print(f"Low-confidence matches: {summary['low_confidence_matches']}")
    print(f"Invalid label rows: {summary['invalid_label_rows']}")
    print(f"Saved failure artifacts to: {output_dir}")
    return summary


def main():
    parser = argparse.ArgumentParser(description="Find and annotate YOLO test-set failures")
    parser.add_argument("--weights", type=Path, required=True, help="Path to trained best.pt")
    parser.add_argument("--data", type=Path, default=load_default_data_yaml(), help="Path to data.yaml")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_DIR, help="Output directory")
    parser.add_argument("--imgsz", type=int, default=640, help="Inference image size")
    parser.add_argument("--conf", type=float, default=0.001, help="Prediction confidence threshold")
    parser.add_argument("--iou", type=float, default=0.5, help="IoU threshold for a correct detection")
    parser.add_argument("--low-conf", type=float, default=0.25, help="Matched detections below this confidence are flagged")
    parser.add_argument("--device", type=str, default="0", help="Device, e.g. 0 or cpu")
    parser.add_argument("--max-cases", type=int, default=200, help="Maximum annotated case rows to save; 0 means no limit")
    args = parser.parse_args()

    analyze_failures(
        weights=args.weights,
        data_yaml=args.data,
        output_dir=args.output,
        imgsz=args.imgsz,
        conf=args.conf,
        iou_threshold=args.iou,
        low_confidence=args.low_conf,
        device=args.device,
        max_cases=args.max_cases,
    )


if __name__ == "__main__":
    main()
