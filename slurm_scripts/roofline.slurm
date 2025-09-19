#!/usr/local_rwth/bin/zsh

#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --ntasks-per-node=96
#SBATCH --job-name=roofline_lustre
#SBATCH --output=/home/author/roofline/results/beeond-%a-%A.txt
#SBATCH --time=01:00:00
#SBATCH --array=1-12%1

#SBATCH --beeond

(( FILES = (1024 * 256 / 96) / (2 ** (${SLURM_ARRAY_TASK_ID}-1)) ))
(( BYTES = (4608 * 1024 * 1024) / (${FILES} * 96) ))

echo "BYTES=${BYTES}"

mkdir -p ${BEEOND}/roofline/${SLURM_ARRAY_TASK_ID}
cd ${BEEOND}/roofline/${SLURM_ARRAY_TASK_ID}

$MPIEXEC $FLAGS_MPI_BATCH /home/author/roofline/ior/install/bin/mdtest -P -L -F -N=1 -i 10 -n $FILES -w $BYTES -e $BYTES -d ${BEEOND}/roofline/${SLURM_ARRAY_TASK_ID}
