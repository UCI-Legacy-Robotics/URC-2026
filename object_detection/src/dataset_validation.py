"""
Validate a YOLO dataset before training.

Checks for corrupt images, missing/empty/malformed labels, class imbalance, and
train/val/test leakage by image content hash.

Usage:
    python src/dataset_validation.py
    python src/dataset_validation.py --data data/data.yaml
"""

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Optional

import cv2
import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data" / "data.yaml"
DEFAULT_OUTPUT = ROOT / "runs" / "dataset_validation"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def load_data_yaml(data_yaml: Path) -> dict:
    if not data_yaml.exists():
        raise FileNotFoundError(f"Dataset descriptor not found: {data_yaml}")
    with open(data_yaml) as f:
        return yaml.safe_load(f) or {}


def resolve_split_dir(data_yaml: Path, split_value: str) -> Path:
    path = Path(split_value)
    if path.is_absolute():
        return path
    return (data_yaml.parent / path).resolve()


def label_path_for(image_path: Path) -> Path:
    parts = list(image_path.parts)
    if "images" in parts:
        parts[parts.index("images")] = "labels"
        return Path(*parts).with_suffix(".txt")
    return image_path.parent.parent / "labels" / f"{image_path.stem}.txt"


def image_hash(image_path: Path) -> str:
    digest = hashlib.sha256()
    with open(image_path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_label_row(row: str, nc: int) -> tuple[Optional[int], Optional[str]]:
    values = row.split()
    if len(values) != 5:
        return None, "wrong_field_count"

    try:
        class_id = int(float(values[0]))
        coords = [float(value) for value in values[1:]]
    except ValueError:
        return None, "non_numeric"

    if class_id < 0 or class_id >= nc:
        return class_id, "class_out_of_range"
    if any(value < 0.0 or value > 1.0 for value in coords):
        return class_id, "box_out_of_range"
    if coords[2] <= 0.0 or coords[3] <= 0.0:
        return class_id, "non_positive_box_size"
    return class_id, None


def validate_dataset(data_yaml: Path, output_dir: Path) -> dict:
    config = load_data_yaml(data_yaml)
    names = config.get("names", [])
    nc = int(config.get("nc", len(names)))
    splits = {
        "train": resolve_split_dir(data_yaml, config["train"]),
        "val": resolve_split_dir(data_yaml, config["val"]),
        "test": resolve_split_dir(data_yaml, config["test"]),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    issues = []
    class_counts: Counter[int] = Counter()
    split_counts = {}
    hashes: dict[str, list[tuple[str, str]]] = defaultdict(list)

    for split, images_dir in splits.items():
        if not images_dir.exists():
            issues.append({"split": split, "path": str(images_dir), "issue": "missing_images_dir"})
            split_counts[split] = 0
            continue

        images = sorted(
            path
            for path in images_dir.rglob("*")
            if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
        )
        split_counts[split] = len(images)

        for image_path in images:
            image = cv2.imread(str(image_path))
            if image is None:
                issues.append({"split": split, "path": str(image_path), "issue": "corrupt_image"})
                continue

            hashes[image_hash(image_path)].append((split, str(image_path)))
            label_path = label_path_for(image_path)
            if not label_path.exists():
                issues.append({"split": split, "path": str(label_path), "issue": "missing_label"})
                continue

            rows = [row.strip() for row in label_path.read_text().splitlines() if row.strip()]
            if not rows:
                issues.append({"split": split, "path": str(label_path), "issue": "empty_label"})
                continue

            for line_number, row in enumerate(rows, start=1):
                class_id, issue = validate_label_row(row, nc)
                if class_id is not None and issue is None:
                    class_counts[class_id] += 1
                elif class_id is not None and 0 <= class_id < nc:
                    class_counts[class_id] += 1
                if issue:
                    issues.append(
                        {
                            "split": split,
                            "path": str(label_path),
                            "line": line_number,
                            "issue": issue,
                        }
                    )

    for entries in hashes.values():
        present_splits = {split for split, _ in entries}
        if len(present_splits) > 1:
            issues.append(
                {
                    "split": ",".join(sorted(present_splits)),
                    "path": " | ".join(path for _, path in entries),
                    "issue": "split_leakage_duplicate_image",
                }
            )

    class_summary = {
        str(class_id): {
            "name": names[class_id] if isinstance(names, list) and class_id < len(names) else str(class_id),
            "instances": class_counts[class_id],
        }
        for class_id in range(nc)
    }
    summary = {
        "data_yaml": str(data_yaml),
        "split_image_counts": split_counts,
        "class_counts": class_summary,
        "issue_count": len(issues),
    }

    with open(output_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    with open(output_dir / "issues.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["split", "path", "line", "issue"])
        writer.writeheader()
        writer.writerows(issues)

    print(f"Validated dataset: {data_yaml}")
    print(f"Image counts: {split_counts}")
    print(f"Issues found: {len(issues)}")
    print(f"Saved validation artifacts to: {output_dir}")
    return summary


def main():
    parser = argparse.ArgumentParser(description="Validate YOLO dataset integrity")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA, help="Path to data.yaml")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output directory")
    args = parser.parse_args()

    validate_dataset(args.data, args.output)


if __name__ == "__main__":
    main()
