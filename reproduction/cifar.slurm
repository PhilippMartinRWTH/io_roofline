#!/usr/local/bin/zsh

### Node Configuration
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --ntasks-per-node=4

### Request GPUs
#SBATCH --gres=gpu:4
#SBATCH --partition=c23g

#SBATCH --time=05:00:00
#SBATCH --output=__OUTPUT_PATH__/cifar-__FS_NAME__-%j.txt

### MAKE SURE THE CORRECT TOOLCHAIN FOR YOUR ENVIRONMENT IS LOADED
ml load foss
ml load Python

FS=__FS_PATH__
BASEDIR=${PWD}

### Preparing the input data
mkdir -p ${FS}/imagenet
cp -r __IMAGENET_PATH__/* ${FS}/imagenet
cd ${FS}/imagenet

### Load the venv
source ${BASEDIR}/prerequisites/cifar/cifar_venv/bin/activate

### Darshan Configuration
export DARSHAN_CONFIG_PATH=${BASEDIR}/config/darshan_cifar.conf
export DARSHAN_LOGPATH=${BASEDIR}/darshan_outputs
export DARSHAN_ENABLE_NONMPI=1
export LD_PRELOAD=${BASEDIR}/prerequisites/darshan/install/lib/libdarshan.so

python ${BASEDIR}/prerequisites/cifar/train.py -net resnet18 -gpu
