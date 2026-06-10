#!/bin/bash
#PBS -l select=1:ncpus=1:mem=64gb
#PBS -l walltime=120:00:00
#PBS -N htc-N8-0.17
#PBS -j oe

cd $PBS_O_WORKDIR
date > timeneeded.${PBS_JOBID}
python3 TDSE_dynamics.py
date >> timeneeded.${PBS_JOBID}
