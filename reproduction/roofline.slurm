#!/usr/bin/env zsh

### Node Configuration
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=__TASK_NUM__
#SBATCH --exclusive

#SBATCH --time=01:00:00
#SBATCH --output=__OUTPUT_PATH__/mdtest-__FS_NAME__-%a-%A.txt

#SBATCH --array=1-29%1

### MAKE SURE THE CORRECT TOOLCHAIN FOR YOUR ENVIRONMENT IS LOADED
ml load foss

### Adjusting file number and byte counts
(( FILES = (1000 / __TASK_NUM__) ))
(( BYTES = (2 ** (${SLURM_ARRAY_TASK_ID}-1)) ))

FS=__FS_PATH__
BASEDIR=${PWD}

### Preparing the folder structure
mkdir -p ${FS}/roofline/${SLURM_ARRAY_TASK_ID}
cd ${FS}/roofline/${SLURM_ARRAY_TASK_ID}

### Running MDTest
echo "BYTES=${BYTES}"
$MPIEXEC $FLAGS_MPI_BATCH ${BASEDIR}/prerequisites/ior/install/bin/mdtest -P -L -F -N=1 -i 10 -n $FILES -w $BYTES -e $BYTES -d ${FS}/roofline/${SLURM_ARRAY_TASK_ID}
