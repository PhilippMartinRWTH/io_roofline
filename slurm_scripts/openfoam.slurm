#!/usr/local/bin/zsh

#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --ntasks-per-node=96
#SBATCH --output=/home/author/roofline/results/openfoam-lustre-%j.txt
#SBATCH --time=01:00:00

FS=${HPCWORK}

ml load foss
ml load OpenFOAM/v2406

mkdir -p ${FS}/openfoam

cp -r /home/author/roofline/openFOAM/Large/v1912/* ${FS}/openfoam

cd ${FS}/openfoam

export DARSHAN_CONFIG_PATH=/home/author/roofline/openFOAM/Large/darshan.cfg
export LD_PRELOAD=/home/author/software/darshan-foss/install/lib/libdarshan.so
time ./AllmeshL
time ./Allrun
