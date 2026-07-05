"""
Roboflow dataset download logic.

Downloads the URC dataset from Roboflow using the API key
stored in .env and saves it to the data/ directory.
"""

import argparse
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
STABLE_DATA_YAML = DATA_DIR / "data.yaml"

load_dotenv(ROOT / ".env")


def get_roboflow_api_key() -> str:
    """Read the Roboflow API key from the environment with no fallback value."""
    try:
        return os.environ["ROBOFLOW_API_KEY"]
    except KeyError as exc:
        raise RuntimeError(
            "ROBOFLOW_API_KEY not set. Copy .env.example to .env and add your key."
        ) from exc


def write_stable_data_yaml(dataset_dir: Path) -> Path:
    """
    Create data/data.yaml with paths relative to object_detection/data.

    Roboflow exports can include split paths that are relative to a different
    working directory. This stable descriptor is what training/evaluation use.
    """
    source_yaml = dataset_dir / "data.yaml"
    if not source_yaml.exists():
        raise FileNotFoundError(f"Downloaded dataset is missing {source_yaml}")

    with open(source_yaml) as f:
        source_config = yaml.safe_load(f) or {}

    split_dirs = {
        "train": dataset_dir / "train" / "images",
        "val": dataset_dir / "valid" / "images",
        "test": dataset_dir / "test" / "images",
    }
    for split, path in split_dirs.items():
        if not path.exists():
            raise FileNotFoundError(f"Downloaded dataset is missing {split} images at {path}")

    stable_config = {
        split: os.path.relpath(path, DATA_DIR)
        for split, path in split_dirs.items()
    }
    for key in ("nc", "names", "roboflow"):
        if key in source_config:
            stable_config[key] = source_config[key]

    with open(STABLE_DATA_YAML, "w") as f:
        yaml.safe_dump(stable_config, f, sort_keys=False)

    return STABLE_DATA_YAML


def download_dataset(
    workspace: str = "monash-nova-rover",
    project: str = "urc-2024-object-detection",
    version: int = 6,
    model_format: str = "yolov11",
) -> Path:
    """Download dataset from Roboflow.

    Args:
        workspace: Roboflow workspace name.
        project: Roboflow project name.
        version: Dataset version number.
        model_format: Export format.

    Returns:
        Path to the downloaded dataset directory.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    from roboflow import Roboflow

    rf = Roboflow(api_key=get_roboflow_api_key())
    project_obj = rf.workspace(workspace).project(project)
    version_obj = project_obj.version(version)
    target_dir = DATA_DIR / f"{project}-{version}"
    try:
        dataset = version_obj.download(model_format, location=str(target_dir))
    except TypeError:
        original_cwd = Path.cwd()
        os.chdir(DATA_DIR)
        try:
            dataset = version_obj.download(model_format)
        finally:
            os.chdir(original_cwd)

    dataset_dir = Path(dataset.location).resolve()
    stable_yaml = write_stable_data_yaml(dataset_dir)

    print(f"Dataset downloaded to: {dataset_dir}")
    print(f"Stable training descriptor written to: {stable_yaml}")
    return dataset_dir


def main():
    parser = argparse.ArgumentParser(description="Download the Roboflow dataset")
    parser.add_argument("--workspace", default="monash-nova-rover", help="Roboflow workspace name")
    parser.add_argument("--project", default="urc-2024-object-detection", help="Roboflow project name")
    parser.add_argument("--version", type=int, default=6, help="Roboflow dataset version")
    parser.add_argument("--format", default="yolov11", help="Roboflow export format")
    args = parser.parse_args()

    download_dataset(
        workspace=args.workspace,
        project=args.project,
        version=args.version,
        model_format=args.format,
    )


if __name__ == "__main__":
    main()
