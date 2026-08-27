#!/usr/bin/env/zsh

### Node Configuration
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=96
#SBATCH --exclusive

#SBATCH --time=01:00:00
#SBATCH --output=__OUTPUT_PATH__/openfoam-__FS_NAME__-%j.txt

### MAKE SURE THE CORRECT TOOLCHAIN FOR YOUR ENVIRONMENT IS LOADED
### ADJUST MODULE NAME FOR OPENFOAM IF REQUIRED
ml load foss
ml load OpenFOAM/v2406

FS=__FS_PATH__
BASEDIR=${PWD}

### Preparing the input data
mkdir -p ${FS}/openfoam
cp -r ${BASEDIR}/prerequisites/openFOAM/Large/v1912/* ${FS}/openfoam

### Darshan Configuration
export DARSHAN_CONFIG_PATH=${BASEDIR}/config/darshan_openfoam.conf
export DARSHAN_LOGPATH=${BASEDIR}/darshan_outputs
export LD_PRELOAD=${BASEDIR}/prerequisites/darshan/install/lib/libdarshan.so

### Running openFOAM
cd ${FS}/openfoam
time ./AllmeshL
time ./Allrun
