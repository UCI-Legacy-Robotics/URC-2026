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
│   ├── data.yaml               # stable train/val/test descriptor
│   └── URC-2024-.../           # (gitignored) actual dataset
│       └── data.yaml
├── src/
│   ├── train.py                # training entry point
│   ├── export.py               # .pt → ONNX → TensorRT engine
│   ├── evaluate.py             # held-out test-set metrics
│   ├── failure_analysis.py     # annotated FP/FN/low-confidence cases
│   ├── benchmark.py            # latency and FPS benchmarking
│   ├── dataset_validation.py   # dataset integrity/leakage checks
│   └── inference.py            # load .engine, run detection (Jetson/ROS2)
├── scripts/
│   ├── download_data.slurm     # HPC3 job: fetch dataset
│   ├── run_hpc3.slurm          # HPC3 job: train model
│   └── tune_hpc3.slurm         # HPC3 job: evolutionary tuning
├── configs/
│   └── train_config.yaml       # hyperparameters, paths, model size
├── logs/                       # SLURM stdout/stderr
├── runs/                       # (gitignored) training outputs / weights
└── models/                     # (gitignored) exported .onnx / .engine
```

## Quick Start

1. Copy `.env.example` → `.env` and add your Roboflow API key.
2. Install dependencies: `pip install -r requirements.txt`
3. Download the dataset: `python data/data.py`
4. Validate the dataset: `python src/dataset_validation.py`
5. Train: `python src/train.py`
6. Evaluate on the held-out test split: `python src/evaluate.py --weights runs/yolo11s_baseline/weights/best.pt`
7. Export for Jetson: `python src/export.py --weights runs/yolo11s_baseline/weights/best.pt --format engine --half`

## HPC3 Usage

```bash
cd object_detection
sbatch scripts/download_data.slurm   # download dataset on HPC3
sbatch scripts/run_hpc3.slurm        # submit training job
sbatch scripts/tune_hpc3.slurm       # submit tuning job
```

Before submitting jobs, verify the partition names on HPC3 with `sinfo` and
adjust the `#SBATCH --partition=...` lines if needed.
