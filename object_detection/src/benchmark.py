"""
Benchmark YOLO inference latency for deployable model formats.

Run this on the Jetson for deployment-relevant numbers. HPC or laptop results
are still useful for smoke testing but should not drive rover model selection.

Usage:
    python src/benchmark.py --models runs/yolo11s_baseline/weights/best.pt
    python src/benchmark.py --models models/best.onnx models/best.engine --source data/test/images
"""

import argparse
import csv
import json
import statistics
import time
from pathlib import Path

import torch
import yaml
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "configs" / "train_config.yaml"
DEFAULT_OUTPUT_DIR = ROOT / "runs" / "benchmark"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


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


def collect_images(source: Path, data_yaml: Path, max_images: int) -> list[Path]:
    if source:
        source = source.resolve()
    else:
        source = resolve_split_images(data_yaml)

    if source.is_file():
        paths = [source]
    else:
        paths = sorted(
            path
            for path in source.rglob("*")
            if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
        )

    if max_images:
        paths = paths[:max_images]
    if not paths:
        raise FileNotFoundError(f"No benchmark images found under {source}")
    return paths


def sync_device(device: str) -> None:
    if device != "cpu" and torch.cuda.is_available():
        torch.cuda.synchronize()


def percentile(values: list[float], percent: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, round((percent / 100) * (len(ordered) - 1)))
    return ordered[index]


def metric_value(metrics, key: str) -> float:
    results_dict = getattr(metrics, "results_dict", {}) or {}
    if key in results_dict:
        return float(results_dict[key])

    box = getattr(metrics, "box", None)
    fallback_attrs = {
        "metrics/mAP50(B)": "map50",
        "metrics/mAP50-95(B)": "map",
    }
    attr = fallback_attrs.get(key)
    if box is not None and attr and hasattr(box, attr):
        return float(getattr(box, attr))
    return 0.0


def benchmark_model(
    model_path: Path,
    images: list[Path],
    data_yaml: Path,
    imgsz: int,
    conf: float,
    device: str,
    warmup: int,
    repeats: int,
    with_map: bool,
) -> dict:
    if repeats <= 0:
        raise ValueError("--repeats must be greater than 0")

    model = YOLO(str(model_path))
    warmup_images = images[: max(1, min(warmup, len(images)))]
    for image_path in warmup_images:
        model.predict(source=str(image_path), imgsz=imgsz, conf=conf, device=device, verbose=False)
    sync_device(device)

    latencies_ms = []
    for _ in range(repeats):
        for image_path in images:
            sync_device(device)
            start = time.perf_counter()
            model.predict(source=str(image_path), imgsz=imgsz, conf=conf, device=device, verbose=False)
            sync_device(device)
            latencies_ms.append((time.perf_counter() - start) * 1000)

    mean_ms = statistics.mean(latencies_ms)
    row = {
        "model": str(model_path),
        "format": model_path.suffix.lstrip(".") or "unknown",
        "device": device,
        "imgsz": imgsz,
        "images": len(images),
        "samples": len(latencies_ms),
        "mean_ms": mean_ms,
        "median_ms": statistics.median(latencies_ms),
        "p95_ms": percentile(latencies_ms, 95),
        "fps": 1000 / mean_ms if mean_ms else 0.0,
        "map50": None,
        "map50_95": None,
    }

    if with_map:
        metrics = model.val(
            data=str(data_yaml),
            split="test",
            imgsz=imgsz,
            device=device,
            plots=False,
            verbose=False,
        )
        row["map50"] = metric_value(metrics, "metrics/mAP50(B)")
        row["map50_95"] = metric_value(metrics, "metrics/mAP50-95(B)")

    return row


def write_results(output_dir: Path, rows: list[dict]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "benchmark.json", "w") as f:
        json.dump(rows, f, indent=2)

    with open(output_dir / "benchmark.csv", "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "model",
                "format",
                "device",
                "imgsz",
                "images",
                "samples",
                "mean_ms",
                "median_ms",
                "p95_ms",
                "fps",
                "map50",
                "map50_95",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def print_table(rows: list[dict]) -> None:
    print("model, format, mean_ms, p95_ms, fps, mAP50, mAP50-95")
    for row in rows:
        map50 = "" if row["map50"] is None else f"{row['map50']:.4f}"
        map50_95 = "" if row["map50_95"] is None else f"{row['map50_95']:.4f}"
        print(
            f"{row['model']}, {row['format']}, {row['mean_ms']:.2f}, "
            f"{row['p95_ms']:.2f}, {row['fps']:.2f}, {map50}, {map50_95}"
        )


def main():
    parser = argparse.ArgumentParser(description="Benchmark YOLO inference latency")
    parser.add_argument("--models", type=Path, nargs="+", required=True, help="One or more .pt/.onnx/.engine models")
    parser.add_argument("--data", type=Path, default=load_default_data_yaml(), help="Path to data.yaml")
    parser.add_argument("--source", type=Path, default=None, help="Image file or directory; defaults to test split")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_DIR, help="Output directory")
    parser.add_argument("--imgsz", type=int, default=640, help="Inference image size")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold")
    parser.add_argument("--device", type=str, default="0", help="Device, e.g. 0 or cpu")
    parser.add_argument("--warmup", type=int, default=10, help="Warmup images before timing")
    parser.add_argument("--repeats", type=int, default=3, help="Timed passes through the image set")
    parser.add_argument("--max-images", type=int, default=100, help="Maximum images to benchmark; 0 means all")
    parser.add_argument("--with-map", action="store_true", help="Also run test mAP for each model")
    args = parser.parse_args()

    images = collect_images(args.source, args.data, args.max_images)
    rows = [
        benchmark_model(
            model_path=model_path,
            images=images,
            data_yaml=args.data,
            imgsz=args.imgsz,
            conf=args.conf,
            device=args.device,
            warmup=args.warmup,
            repeats=args.repeats,
            with_map=args.with_map,
        )
        for model_path in args.models
    ]

    write_results(args.output, rows)
    print_table(rows)
    print(f"Saved benchmark artifacts to: {args.output}")


if __name__ == "__main__":
    main()
