#!/usr/bin/env zsh

POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    --fs-path)
      FS_PATH="$2"
      shift # past argument
      shift # past value
      ;;
    --fs-name)
      FS_NAME="$2"
      shift # past argument
      shift # past value
      ;;
    --imagenet-path)
      IMAGENET_PATH="$2"
      shift # past argument
      shift # past value
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      shift # past argument
      ;;
  esac
done

set -- "${POSITIONAL_ARGS[@]}"

if [ -z "${FS_PATH}" ]; then
    echo "ERROR! No --fs-path provided"
    exit 1
fi

if [ -z "${FS_NAME}" ]; then
    echo "ERROR! No --fs-name provided"
    exit 1
fi

if [ -z "${IMAGENET_PATH}" ]; then
    echo "ERROR! No --imagenet-path provided"
    exit 1
fi

OUTPUT_PATH=${PWD}/outputs

for tasks (1 4 8 16 32 48 96); do
    sbatch <(awk -v r1="${FS_PATH}" -v t1="__FS_PATH__" -v r2="${FS_NAME}" -v t2="__FS_NAME__" -v r3="${OUTPUT_PATH}" -v t3="__OUTPUT_PATH__" -v r4="${tasks}" -v t4="__TASK_NUM__" '{ gsub(t1,r1); gsub(t2,r2); gsub(t3,r3); gsub(t4,r4); print }' roofline.slurm)
done

sbatch <(awk -v r1="${FS_PATH}" -v t1="__FS_PATH__" -v r2="${FS_NAME}" -v t2="__FS_NAME__" -v r3="${OUTPUT_PATH}" -v t3="__OUTPUT_PATH__" '{ gsub(t1,r1); gsub(t2,r2); gsub(t3,r3); print }' openfoam.slurm)
sbatch <(awk -v r1="${FS_PATH}" -v t1="__FS_PATH__" -v r2="${FS_NAME}" -v t2="__FS_NAME__" -v r3="${OUTPUT_PATH}" -v t3="__OUTPUT_PATH__" '{ gsub(t1,r1); gsub(t2,r2); gsub(t3,r3); print }' cifar.slurm)
sbatch <(awk -v r1="${FS_PATH}" -v t1="__FS_PATH__" -v r2="${FS_NAME}" -v t2="__FS_NAME__" -v r3="${OUTPUT_PATH}" -v t3="__OUTPUT_PATH__" -v r4="${IMAGENET_PATH}" -v t4="__IMAGENET_PATH__" '{ gsub(t1,r1); gsub(t2,r2); gsub(t3,r3); gsub(t4,r4); print }' imagenet.slurm)
