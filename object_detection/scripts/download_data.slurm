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
# TODO: Verify the partition name on HPC3 with `sinfo` before submitting.

module load python/3.10
source ~/.venvs/urc/bin/activate   # adjust to your venv path

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
mkdir -p "$PROJECT_ROOT/logs"
cd "$PROJECT_ROOT"

python data/data.py

echo "Download complete."
