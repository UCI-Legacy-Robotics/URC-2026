"""Config-driven training / tuning entry point for YOLO object detection.

Usage:
    # Train from config:
    python src/train.py --config configs/train_config.yaml

    # Override model, dataset, and common train args from the terminal:
    python src/train.py --model yolo11n.pt --data /path/to/dataset/data.yaml --epochs 100 --device 0

    # Pass any Ultralytics train() argument with --set:
    python src/train.py --set lr0=0.005 --set mosaic=0.5 --set model.source=yolo11m.pt

    # Evolutionary hyperparameter search:
    python src/train.py --tune --iterations 30 --tune-epochs 30
"""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from .yolo_model_factory import (
        ROOT,
        apply_cli_overrides,
        create_model,
        load_training_config,
        split_training_config,
    )
except ImportError:
    from yolo_model_factory import (
        ROOT,
        apply_cli_overrides,
        create_model,
        load_training_config,
        split_training_config,
    )

DEFAULT_CONFIG = ROOT / "configs" / "train_config.yaml"


def train(config: dict) -> None:
    """Run a normal training pass from the resolved config."""
    model_config, data_yaml, train_args, _ = split_training_config(config)
    model = create_model(model_config)
    model.train(data=str(data_yaml), **train_args)


def tune(config: dict, iterations: int | None, tune_epochs: int | None) -> None:
    """
    Run evolutionary hyperparameter search.

    Each of `iterations` trials trains a SHORT model (`tune_epochs` epochs) with
    a mutated hyperparameter set, scores it on validation mAP, and evolves toward
    the best values. Result is written to runs/tune/best_hyperparameters.yaml.

    We deliberately override a few keys for the search:
      - epochs -> short (trials are cheap comparisons, not final models)
      - patience/save_period -> dropped (irrelevant for short trials)
      - plots/val kept sensible for a search
    """
    model_config, data_yaml, train_args, tune_config = split_training_config(config)
    iterations = iterations if iterations is not None else int(tune_config.get("iterations", 30))
    tune_epochs = tune_epochs if tune_epochs is not None else int(
        tune_config.get("epochs", tune_config.get("tune_epochs", 30))
    )

    tune_args = train_args.copy()
    extra_tune_args = tune_config.get("args", {})
    if extra_tune_args:
        if not isinstance(extra_tune_args, dict):
            raise TypeError("'tune.args' must be a mapping when provided.")
        tune_args.update(extra_tune_args)

    # Remove full-run-only keys so they don't fight the short trial budget.
    dropped = []
    drop_keys = tune_config.get("drop_keys", ("epochs", "patience", "save_period", "name"))
    for key in drop_keys:
        if key in tune_args:
            dropped.append(key)
            tune_args.pop(key)
    if dropped:
        print(f"Tuning override: dropped full-run config keys: {', '.join(dropped)}")

    tune_args.setdefault("plots", True)
    tune_args.setdefault("save", False)
    tune_args.setdefault("val", True)

    model = create_model(model_config)
    model.tune(
        data=str(data_yaml),
        epochs=tune_epochs,
        iterations=iterations,
        **tune_args,
    )


def main():
    parser = argparse.ArgumentParser(description="Train or tune a YOLO model")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Path to config YAML (training defaults OR tuned best_hyperparameters).",
    )
    parser.add_argument("--model", type=str, default=None, help="Override model source, e.g. yolo11n.pt")
    parser.add_argument("--data", type=str, default=None, help="Override dataset data.yaml path or dataset directory")
    parser.add_argument("--project", type=str, default=None, help="Override output project directory")
    parser.add_argument("--name", type=str, default=None, help="Override run name")
    parser.add_argument("--epochs", type=int, default=None, help="Override training epochs")
    parser.add_argument("--batch", type=str, default=None, help="Override batch size, e.g. 16 or -1")
    parser.add_argument("--imgsz", type=int, default=None, help="Override image size")
    parser.add_argument("--device", type=str, default=None, help="Override device, e.g. 0, cpu, mps, or auto")
    parser.add_argument("--workers", type=int, default=None, help="Override dataloader workers")
    parser.add_argument(
        "--resume",
        nargs="?",
        const=True,
        default=None,
        help="Resume training. Use without a value for latest run, or pass a checkpoint path.",
    )
    parser.add_argument(
        "--set",
        dest="set_values",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Override any config/train value. Dot notation is supported, e.g. model.source=yolo11m.pt.",
    )
    parser.add_argument(
        "--tune",
        action="store_true",
        help="Run evolutionary hyperparameter search instead of training.",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=None,
        help="Number of tuning trials (only used with --tune).",
    )
    parser.add_argument(
        "--tune-epochs",
        type=int,
        default=None,
        help="Epochs per tuning trial — keep SHORT (only used with --tune).",
    )
    args = parser.parse_args()

    config = apply_cli_overrides(
        load_training_config(args.config, DEFAULT_CONFIG),
        model=args.model,
        data=args.data,
        project=args.project,
        name=args.name,
        epochs=args.epochs,
        batch=args.batch,
        imgsz=args.imgsz,
        device=args.device,
        workers=args.workers,
        resume=args.resume,
        set_values=args.set_values,
    )

    if args.tune:
        tune(config, iterations=args.iterations, tune_epochs=args.tune_epochs)
    else:
        train(config)


if __name__ == "__main__":
    main()
