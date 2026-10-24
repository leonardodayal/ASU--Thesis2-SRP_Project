# Corrected Fine-Grid Three-Sheet Control

Purpose: matched zero-resistance baseline for the corrected fine-grid active case.

- Executable SHA-256: `d3f92b1f970ebe4ad9f6042abfd758b9fe2a052f8bf67568c7d567c1674687d2`
- Command: `mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input`
- Mesh / decomposition: `384 x 96 x 96` / `4 x 1 x 1`
- Resistance: `alpha = 1e30`, `C2 = 0`
- Steps / final time: `2000 / 4`
- Ensight output: disabled
- Wall time: about `56.0 min`

The run terminated normally at `t = 4`. Pair-level corrected results and numerical checks are documented in `../2026-10-20_stacked_three_sheet_fine_fractional/RUN_NOTES.md`.
