# Optimising HPC Filesystem Choices with Bandwidth-Centric I/O Rooflines
This is the data repository for the paper "Optimising HPC Filesystem Choices with Bandwidth-Centric I/O Rooflines", submitted to HPC Asia 2026.

## Reproduction
To reproduce the experiments, install [mdtest](https://github.com/hpc/ior) and the [ESI-OpenCFD](https://www.openfoam.com/) version 2406 of OpenFOAM.
Then, refer to the SLURM Scripts.

## Data
The data/ directory contains all measurement data relevant for the submission and a plotting script to create different plots.
Each entry in the filesystems.csv file corresponds to the averages of 10 mdtest runs.
The entries in openfoam.csv correspond to the results found in the darshan files in the data/darshan directory

## SLURM Scripts
The slurm_scripts directory contains sample scripts of how the data was generated.
