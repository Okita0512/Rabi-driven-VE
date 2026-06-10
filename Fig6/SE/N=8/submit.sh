#!/bin/bash
# Submit all N=8 TDSE jobs to PBS queue.
# Run this script from the N=8 directory: bash submit.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for dir in \
    0.16 0.17 0.18 0.19 \
    0.195 0.196 0.197 0.198 0.199 \
    0.20 0.201 0.202 0.203 \
    0.21 0.22 0.23 0.24
do
    cd "${SCRIPT_DIR}/${dir}"
    JOB_ID=$(qsub sbatch_python.sh)
    echo "Submitted ${dir}: ${JOB_ID}"
done
