#!/bin/bash
#SBATCH -p preempt
#SBATCH -o output.log
#SBATCH --mem=8GB
#SBATCH --time=2-00:00:00
#SBATCH --cpus-per-task=1
#SBATCH --job-name=HTC

time ../../bin/rhot ./input.json

