#!/bin/bash
#SBATCH --job-name=urc-tune
#SBATCH --partition=free-gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --gres=gpu:1
#SBATCH --time=08:00:00
#SBATCH --output=logs/tune_%j.out
#SBATCH --error=logs/tune_%j.err

# HPC3 job: short evolutionary hyperparameter tuning.
# TODO: Verify the partition name on HPC3 with `sinfo` before submitting.

module load python/3.10
module load cuda/12.1
source ~/.venvs/urc/bin/activate   # adjust to your venv path

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
mkdir -p "$PROJECT_ROOT/logs"
cd "$PROJECT_ROOT"

python src/train.py \
  --config "${TRAIN_CONFIG:-configs/train_config.yaml}" \
  --tune \
  --iterations "${TUNE_ITERATIONS:-30}" \
  --tune-epochs "${TUNE_EPOCHS:-30}" \
  "$@"

echo "Tuning complete."
