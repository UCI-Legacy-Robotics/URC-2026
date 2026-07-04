# Object Detection — URC 2026

YOLOv8/v11 object detection pipeline for the University Rover Challenge.

## Directory Structure

```
object_detection/
├── .gitignore
├── .env.example
├── README.md
├── requirements.txt
├── __init__.py
├── data/
│   ├── data.py                 # Roboflow download logic
│   ├── load_data.ipynb         # exploration / sanity-check notebook
│   └── URC-2024-.../           # (gitignored) actual dataset
│       └── data.yaml
├── src/
│   ├── train.py                # training entry point
│   ├── export.py               # .pt → ONNX → TensorRT engine
│   └── inference.py            # load .engine, run detection (Jetson/ROS2)
├── scripts/
│   ├── download_data.slurm     # HPC3 job: fetch dataset
│   └── run_hpc3.slurm          # HPC3 job: train model
├── configs/
│   └── train_config.yaml       # hyperparameters, paths, model size
├── runs/                       # (gitignored) training outputs / weights
└── models/                     # (gitignored) exported .onnx / .engine
```

## Quick Start

1. Copy `.env.example` → `.env` and add your Roboflow API key.
2. Install dependencies: `pip install -r requirements.txt`
3. Download the dataset: `python data/data.py`
4. Train: `python src/train.py`
5. Export for Jetson: `python src/export.py`

## HPC3 Usage

```bash
sbatch scripts/download_data.slurm   # download dataset on HPC3
sbatch scripts/run_hpc3.slurm        # submit training job
```
