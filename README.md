# PDSW 2026 Artifact

This repository consists of two parts:
* Reproduction of the presented data
* Raw data and graph creation

The reproduction part allows the user to reproduce the paper's data on their own system.

The data part contains the raw data from the authors' system that was used to create the graphs in the paper (and more) as well as plotting scripts to visualise the data.

## Reproduction
### Prerequisites
There are some prerequisites that will have to be installed independently of this repository:
* openFOAM (the authors used the [ESI-OpenCFD](https://www.openfoam.com) version 2406)
* SLURM (if you are using another workload manager, you will have to manually adjust the other scripts)
* git (for fetching some prerequisites)
* Python version >= 3.10
* The ImageNet ILSVRC2012 dataset
** Note that pyTorch expects this to be in a particular format. Check out https://raw.githubusercontent.com/pytorch/examples/refs/heads/main/imagenet/extract_ILSVRC.sh for more information
** We recommend holding the dataset in a tarball and unpacking it on the target filesystem rather than copying directly. If you have a different setup, you will have to change the `imagenet.slurm` batch script.

The `get_prerequisites.sh` shell script will install the rest of the necessary software and datasets:
* [IOR](https://github.com/hpc/ior)
* [Darshan](https://www.mcs.anl.gov/research/projects/darshan/download/)
* The script at https://github.com/pytorch/examples/tree/main/imagenet
* The script at https://github.com/weiaicunzai/pytorch-cifar100

```
cd reproduction
./get_prerequisites.sh
```

### Execution / Scheduling
Before you execute the script, please make sure that any module/environment variables are set up correctly.
For reference, the authors executed the commands with the following compilers and toolchains:

If necessary, replace the lines
```
ml load foss
ml load openFOAM/v2406
```
in the `*.slurm` scripts.

In order to run the reproduction, you will have to provide some information to the `schedule_jobs.sh` script:
```
cd reproduction
./schedule_jobs.sh --fs-path </PATH/TO/FS/ROOT> --fs-name <FS_NAME> --imagenet-path </PATH/TO/IMAGENET>
```
Here,
* `--fs-path` requires the full path to a folder on the filesystem you want to test
* `--fs-name` refers to the name of that filesystem (required for proper analysis later)
* `--imagenet-path` requires the full path to the root folder of the ImageNet ILSVRC2012 dataset

Note that reproduction is on a per-filesystem basis, i.e. if you want to test different filesystems (as in the paper), you will have to execute the `schedule_jobs.sh` script for each filesystem.

### Analysis
Once all the jobs have completed, you should have a number of output text files in the `outputs` directory and darshan binary files in the `darshan_outputs` directory.
Execute `process_data.py` to process the data from these files into `*.csv` format.

You can then either manually inspect that data or refer to the Data section below on how to produce graphs like in the paper from that data.

## Data
The data/ directory contains all measurement data relevant for the submission and plotting scripts to create different plots.

### Plotting
