"""
Training / tuning entry point for YOLOv11 object detection.

Usage:
    # Normal training (uses every hyperparameter in the config):
    python src/train.py
    python src/train.py --config configs/train_config.yaml

    # Evolutionary hyperparameter search (writes best_hyperparameters.yaml):
    python src/train.py --tune
    python src/train.py --tune --iterations 30 --tune-epochs 30

    # Final training from tuned results:
    python src/train.py --config runs/tune/best_hyperparameters.yaml
"""

import argparse
from pathlib import Path

import yaml
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "configs" / "train_config.yaml"

# Keys that tell THIS script what to do — they are not YOLO hyperparameters,
# so we consume them here and do NOT forward them to model.train()/model.tune().
CONTROL_KEYS = {"model", "data"}


def load_config(config_path: Path) -> dict:
    """Load configuration from YAML."""
    with open(config_path) as f:
        return yaml.safe_load(f)


def split_config(config: dict) -> tuple[str, str, dict]:
    """
    Separate the config into (model_name, data_path, hyperparameters).

    Everything that is NOT a control key is treated as a hyperparameter and
    forwarded verbatim to Ultralytics. This is what makes the whole config
    take effect — cos_lr, patience, optimizer, amp, loss gains, augmentation,
    etc. all flow through instead of being silently dropped.
    """
    model_name = config.get("model", "yolo11s.pt")
    data_yaml = str(ROOT / config.get("data", "data/data.yaml"))

    hyp = {k: v for k, v in config.items() if k not in CONTROL_KEYS}
    # Resolve project path to an absolute path if present.
    if "project" in hyp:
        hyp["project"] = str(ROOT / hyp["project"])
    return model_name, data_yaml, hyp


def train(config: dict) -> None:
    """Run a normal training pass, forwarding ALL config hyperparameters."""
    model_name, data_yaml, hyp = split_config(config)
    model = YOLO(model_name)
    model.train(data=data_yaml, **hyp)


def tune(config: dict, iterations: int, tune_epochs: int) -> None:
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
    model_name, data_yaml, hyp = split_config(config)

    # Remove full-run-only keys so they don't fight the short trial budget.
    dropped = []
    for k in ("epochs", "patience", "save_period", "name"):
        if k in hyp:
            dropped.append(k)
            hyp.pop(k)
    if dropped:
        print(f"Tuning override: dropped full-run config keys: {', '.join(dropped)}")

    model = YOLO(model_name)
    model.tune(
        data=data_yaml,
        epochs=tune_epochs,     # SHORT per-trial budget (search cost control)
        iterations=iterations,  # number of trials
        plots=True,             # fitness curve = your empirical justification
        save=False,             # don't keep every trial's weights (saves disk)
        val=True,
        **hyp,                  # forward augmentation/optimizer/etc. as the seed
    )


def main():
    parser = argparse.ArgumentParser(description="Train or tune a YOLO model")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Path to config YAML (training defaults OR tuned best_hyperparameters).",
    )
    parser.add_argument(
        "--tune",
        action="store_true",
        help="Run evolutionary hyperparameter search instead of training.",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=30,
        help="Number of tuning trials (only used with --tune).",
    )
    parser.add_argument(
        "--tune-epochs",
        type=int,
        default=30,
        help="Epochs per tuning trial — keep SHORT (only used with --tune).",
    )
    args = parser.parse_args()

    config = load_config(args.config)

    if args.tune:
        tune(config, iterations=args.iterations, tune_epochs=args.tune_epochs)
    else:
        train(config)


if __name__ == "__main__":
    main()
