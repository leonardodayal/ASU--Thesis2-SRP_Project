#!/bin/bash
#SBATCH --job-name=srp-nov5-g3-viz
#SBATCH --partition=htc
#SBATCH --qos=public
#SBATCH --account=grp_mherrma1
#SBATCH --nodes=1
#SBATCH --ntasks=64
#SBATCH --cpus-per-task=1
#SBATCH --mem=128G
#SBATCH --time=00:15:00
#SBATCH --export=NONE

set -euo pipefail
module purge
module load gcc/15.2.0
module load openmpi/5.0.8-gcc-15.2.0
module load fftw/3.3.11-openmpi-5.0.8-gcc-15.2.0

exe="$HOME/ASU--Thesis2-SRP_Project/Thesis/simulations/srp_channel/nga.dp.gnu.opt.mpi.exe"
test -x "$exe"
echo "Executable: $exe"; sha256sum "$exe"
echo "Input: $(pwd)/input"; echo "Started: $(date --iso-8601=seconds)"
srun --export=ALL "$exe" -i input

test -s monitor/simulation
test "$(awk 'END {print $1}' monitor/simulation)" = "100"
test -s ensight/srp_channel/nga.case
test -s ensight/srp_channel/geometry
test -s ensight/srp_channel/geometry.fvf
test -s ensight/srp_channel/pressure/pressure.000001
test -s ensight/srp_channel/velocity/velocity.000001
test -s ensight/srp_channel/porous_mask/porous_mask.000001
if grep -RqiE 'nan|infinity|fatal|solver failure|error:' monitor; then
  echo "Failure marker found in monitor output." >&2; exit 1
fi
du -sh ensight
echo "Finished: $(date --iso-8601=seconds)"
