#!/bin/bash
#SBATCH --job-name=srp-8stick-g1-smoke
#SBATCH --partition=htc
#SBATCH --qos=public
#SBATCH --account=grp_mherrma1
#SBATCH --nodes=1
#SBATCH --ntasks=128
#SBATCH --cpus-per-task=1
#SBATCH --mem=64G
#SBATCH --time=00:10:00
#SBATCH --export=NONE

set -euo pipefail

module purge
module load gcc/15.2.0
module load openmpi/5.0.8-gcc-15.2.0
module load fftw/3.3.11-openmpi-5.0.8-gcc-15.2.0

exe="$HOME/ASU--Thesis2-SRP_Project/Thesis/simulations/srp_channel/nga.dp.gnu.opt.mpi.exe"
test -x "$exe"

echo "Executable: $exe"
sha256sum "$exe"
echo "Input: $(pwd)/input"
echo "Started: $(date --iso-8601=seconds)"

srun --export=ALL "$exe" -i input

echo "Finished: $(date --iso-8601=seconds)"
