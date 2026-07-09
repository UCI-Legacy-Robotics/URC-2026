"""Config-driven YOLO model construction and training option handling."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]

CONTROL_KEYS = {"model", "data", "train", "tune"}
REQUIRED_CONFIG_KEYS = ("model", "data")
SUPPORTED_MODEL_TYPES = {"yolo", "ultralytics", "ultralytics-yolo"}


def load_config(config_path: Path) -> dict[str, Any]:
    """Load training configuration from YAML."""
    path = Path(config_path).expanduser()
    if not path.is_absolute() and not path.exists():
        root_candidate = ROOT / path
        if root_candidate.exists():
            path = root_candidate

    if not path.exists():
        raise FileNotFoundError(f"Training config not found: {path}")
    with open(path) as f:
        config = yaml.safe_load(f) or {}
    if not isinstance(config, dict):
        raise TypeError(f"Training config root must be a mapping: {path}")
    return config


def merge_configs(base_config: dict[str, Any], override_config: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge an override config onto a copied base config."""
    merged = deepcopy(base_config)
    for key, value in override_config.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_configs(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged


def missing_required_config_keys(config: dict[str, Any]) -> list[str]:
    """Return required training config keys absent from a config mapping."""
    return [key for key in REQUIRED_CONFIG_KEYS if key not in config]


def load_training_config(config_path: Path, base_config_path: Path) -> dict[str, Any]:
    """
    Load a full training config, or overlay tuned hyperparameters onto a base.

    Ultralytics writes best_hyperparameters.yaml as train kwargs only. Treat that
    shape as an overlay on configs/train_config.yaml so the model and dataset
    remain defined while tuned values replace the defaults.
    """
    config = load_config(config_path)
    missing_keys = missing_required_config_keys(config)
    if config and len(missing_keys) == len(REQUIRED_CONFIG_KEYS):
        config = merge_configs(load_config(base_config_path), config)
    return config


def parse_value(raw_value: str) -> Any:
    """Parse CLI override values using YAML scalar/list/dict syntax."""
    try:
        return yaml.safe_load(raw_value)
    except yaml.YAMLError:
        return raw_value


def set_nested(config: dict[str, Any], dotted_key: str, value: Any) -> None:
    """Set a nested config value using dot notation, e.g. train.epochs=100."""
    keys = [key for key in dotted_key.split(".") if key]
    if not keys:
        raise ValueError("Override key cannot be empty")

    cursor = config
    for key in keys[:-1]:
        existing = cursor.get(key)
        if existing is None:
            existing = {}
            cursor[key] = existing
        if not isinstance(existing, dict):
            raise ValueError(f"Cannot set nested override under non-mapping key: {key}")
        cursor = existing
    cursor[keys[-1]] = value


def apply_cli_overrides(
    config: dict[str, Any],
    *,
    model: str | None = None,
    data: str | None = None,
    project: str | None = None,
    name: str | None = None,
    epochs: int | None = None,
    batch: str | None = None,
    imgsz: int | None = None,
    device: str | None = None,
    workers: int | None = None,
    resume: str | bool | None = None,
    set_values: list[str] | None = None,
) -> dict[str, Any]:
    """
    Merge terminal overrides into a copied config.

    Explicit top-level CLI flags are convenience shortcuts. ``--set`` accepts
    any Ultralytics train() argument or nested model/config key.
    """
    merged = deepcopy(config)

    if model is not None:
        model_config = merged.get("model")
        if isinstance(model_config, dict):
            model_config["source"] = model
        else:
            merged["model"] = {"type": "yolo", "source": model}

    if data is not None:
        merged["data"] = data

    shortcut_train_values = {
        "train.project": project,
        "train.name": name,
        "train.epochs": epochs,
        "train.batch": parse_value(batch) if batch is not None else None,
        "train.imgsz": imgsz,
        "train.device": device,
        "train.workers": workers,
        "train.resume": resume,
    }
    for key, value in shortcut_train_values.items():
        if value is not None:
            set_nested(merged, key, value)

    for item in set_values or []:
        if "=" not in item:
            raise ValueError(f"Invalid override '{item}'. Expected KEY=VALUE.")
        key, raw_value = item.split("=", 1)
        set_nested(merged, key.strip(), parse_value(raw_value.strip()))

    return merged


def resolve_path(path_value: str | Path, *, must_be_data_yaml: bool = False) -> Path:
    """
    Resolve config paths consistently from object_detection/.

    If a relative CLI path already exists from the current working directory,
    use that. Otherwise treat it as relative to the object_detection root.
    """
    path = Path(path_value).expanduser()
    if not path.is_absolute():
        cwd_candidate = path.resolve()
        root_candidate = (ROOT / path).resolve()
        path = cwd_candidate if cwd_candidate.exists() else root_candidate

    if must_be_data_yaml and path.is_dir():
        path = path / "data.yaml"
    return path


def resolve_model_source(source: str | Path) -> str:
    """
    Resolve local model paths while leaving Ultralytics model names untouched.

    Examples:
      - object_detection/yolo11s.pt exists -> absolute path
      - yolo11n.pt missing locally -> "yolo11n.pt" so Ultralytics can download
    """
    source_path = Path(str(source)).expanduser()
    if source_path.is_absolute() and source_path.exists():
        return str(source_path)

    if not source_path.is_absolute():
        cwd_candidate = source_path.resolve()
        root_candidate = (ROOT / source_path).resolve()
        if cwd_candidate.exists():
            return str(cwd_candidate)
        if root_candidate.exists():
            return str(root_candidate)

    return str(source)


def normalize_model_config(model_config: str | dict[str, Any] | None) -> dict[str, Any]:
    """Normalize shorthand and structured model configuration."""
    if model_config is None:
        raise ValueError("Missing required 'model' entry in the training config.")

    if isinstance(model_config, str):
        return {"type": "yolo", "source": model_config}

    if not isinstance(model_config, dict):
        raise TypeError("'model' must be a string or mapping.")

    normalized = deepcopy(model_config)
    normalized["type"] = str(normalized.get("type", "yolo")).lower()

    if "source" not in normalized:
        for alias in ("weights", "checkpoint", "cfg", "architecture"):
            if alias in normalized:
                normalized["source"] = normalized[alias]
                break

    if "source" not in normalized:
        family = normalized.get("family")
        size = normalized.get("size")
        if family and size:
            suffix = normalized.get("suffix", "pt")
            normalized["source"] = f"{family}{size}.{suffix}"

    if "source" not in normalized:
        raise ValueError(
            "Model config needs 'source' (or weights/checkpoint/cfg/architecture, "
            "or family + size)."
        )
    return normalized


def create_model(model_config: str | dict[str, Any]):
    """Create an Ultralytics YOLO model from config."""
    normalized = normalize_model_config(model_config)
    model_type = normalized["type"]
    if model_type not in SUPPORTED_MODEL_TYPES:
        raise ValueError(f"Unsupported model type '{model_type}'. Supported: {sorted(SUPPORTED_MODEL_TYPES)}")

    from ultralytics import YOLO

    source = resolve_model_source(normalized["source"])
    task = normalized.get("task")
    model = YOLO(source, task=task) if task else YOLO(source)

    pretrained = normalized.get("pretrained")
    if isinstance(pretrained, str):
        model.load(resolve_model_source(pretrained))
    return model


def split_training_config(config: dict[str, Any]) -> tuple[dict[str, Any], Path, dict[str, Any], dict[str, Any]]:
    """
    Return model config, data.yaml path, train kwargs, and tune config.

    Supports both the current flat config format and a nested ``train:`` block.
    Top-level non-control keys are treated as Ultralytics train() kwargs for
    backward compatibility.
    """
    missing_keys = missing_required_config_keys(config)
    if missing_keys:
        quoted = ", ".join(f"'{key}'" for key in missing_keys)
        noun = "entry" if len(missing_keys) == 1 else "entries"
        raise ValueError(f"Missing required {quoted} {noun} in the training config.")

    train_args: dict[str, Any] = {key: value for key, value in config.items() if key not in CONTROL_KEYS}

    nested_train = config.get("train", {})
    if nested_train:
        if not isinstance(nested_train, dict):
            raise TypeError("'train' must be a mapping when provided.")
        train_args.update(deepcopy(nested_train))

    if "project" in train_args:
        train_args["project"] = str(resolve_path(train_args["project"]))

    tune_config = config.get("tune", {})
    if tune_config and not isinstance(tune_config, dict):
        raise TypeError("'tune' must be a mapping when provided.")

    data_yaml = resolve_path(config["data"], must_be_data_yaml=True)
    return normalize_model_config(config["model"]), data_yaml, train_args, deepcopy(tune_config)
