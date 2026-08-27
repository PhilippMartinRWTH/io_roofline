#!/usr/bin/env zsh
set -e
BASEDIR=${PWD}

get_darshan () {
    cd ${BASEDIR}/prerequisites
    wget https://github.com/darshan-hpc/darshan/releases/download/3.5.0/darshan-3.5.0.tar.gz
    tar xzf darshan-3.5.0.tar.gz
    mv darshan-3.5.0 darshan
    cd darshan
    mkdir build
    cd build

    ../configure --with-log-path-by-env=DARSHAN_LOGPATH --with-jobid-env=SLURM_JOB_ID --prefix=${BASEDIR}/prerequisites/darshan/install CC=${MPICC}
    make -j8 install

    cd ${BASEDIR}
}

get_ior () {
    cd ${BASEDIR}/prerequisites
    wget https://github.com/hpc/ior/releases/download/4.0.0/ior-4.0.0.tar.gz
    tar xzf ior-4.0.0.tar.gz
    mv ior-4.0.0 ior
    cd ior
    mkdir build
    cd build

    CC=${MPICC} ../configure --prefix=${BASEDIR}/prerequisites/ior/install
    CC=${MPICC} make -j8 install

    cd ${BASEDIR}
}

get_cifar () {
    cd ${BASEDIR}/prerequisites
    git clone https://github.com/weiaicunzai/pytorch-cifar100.git
    mv pytorch-cifar100 cifar
    cd cifar

    python -m venv cifar_venv
    source cifar_venv/bin/activate

    pip install torch
    pip install torchvision
    pip install numpy
    deactivate

    cd ${BASEDIR}
}

get_imagenet () {
    cd ${BASEDIR}/prerequisites
    mkdir imagenet
    cd imagenet

    wget https://raw.githubusercontent.com/pytorch/examples/refs/heads/main/imagenet/main.py
    wget https://raw.githubusercontent.com/pytorch/examples/refs/heads/main/imagenet/requirements.txt
    wget https://raw.githubusercontent.com/pytorch/examples/refs/heads/main/imagenet/extract_ILSVRC.sh
    chmod +x extract_ILSVRC.sh

    python -m venv imagenet_venv
    source imagenet_venv/bin/activate

    pip install -r requirements.txt
    deactivate

    cd ${BASEDIR}
}

get_openfoam () {
    cd ${BASEDIR}/prerequisites
    mkdir openfoam
    cd openfoam
    git init
    git remote add -f origin https://develop.openfoam.com/committees/hpc.git
    git config core.sparseCheckout true
    echo "incompressible/simpleFoam/HPC_motorbike/Large/v1912" >> .git/info/sparse-checkout

    git pull origin develop
    cd ${BASEDIR}
}

# setup environment
ml purge
ml load foss
ml load Python

# create necessary folders
mkdir -p prerequisites
mkdir -p outputs
mkdir -p darshan_outputs

get_darshan
get_ior
get_cifar
get_imagenet
get_openfoam
