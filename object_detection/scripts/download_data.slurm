#!/bin/bash
#SBATCH --job-name=urc-download
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=00:30:00
#SBATCH --output=logs/download_%j.out
#SBATCH --error=logs/download_%j.err

# ── HPC3 job: Download dataset from Roboflow ──

module load python/3.10
source ~/.venvs/urc/bin/activate   # adjust to your venv path

cd "$SLURM_SUBMIT_DIR/.."

python data/data.py

echo "Download complete."
