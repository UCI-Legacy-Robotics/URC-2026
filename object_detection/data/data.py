"""
Roboflow dataset download logic.

Downloads the URC dataset from Roboflow using the API key
stored in .env and saves it to the data/ directory.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from roboflow import Roboflow

# Load environment variables
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY", "")
DATA_DIR = Path(__file__).resolve().parent


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
        model_format: Export format (default: yolov8).

    Returns:
        Path to the downloaded dataset directory.
    """
    if not ROBOFLOW_API_KEY:
        raise ValueError(
            "ROBOFLOW_API_KEY not set. "
            "Copy .env.example → .env and add your key."
        )

    rf = Roboflow(api_key=ROBOFLOW_API_KEY)
    proj = rf.workspace(workspace).project(project)
    dataset = proj.version(version).download(model_format, location=str(DATA_DIR))

    print(f"Dataset downloaded to: {dataset.location}")
    return Path(dataset.location)


if __name__ == "__main__":
    download_dataset()
