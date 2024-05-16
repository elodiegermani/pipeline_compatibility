#!/bin/bash

. /etc/profile.d/modules.sh

set -x

module load spack/octave/5.2.0 


spm_path="/srv/tempdd/egermani/spm12-r7771"
src_path="/srv/tempdd/egermani/hcp_pipelines_compatibility/src/lib"
contrast='right-hand'

for f in 5
do 
	for m in 0
	do
		for h in 0 1
		do
			datasetA=spm-5-24-"$h"
			datasetB=spm-8-0-"$h"
			octave --eval "addpath $spm_path; addpath $src_path; second_level_analysis('$datasetA', '$datasetB')"
done
done
done

for f in 5
do 
	for m in 0 6 24
	do
		for h in 0
		do
			datasetA=spm-5-"$m"-0
			datasetB=spm-8-"$m"-1
			octave --eval "addpath $spm_path; addpath $src_path; second_level_analysis('$datasetA', '$datasetB')"
done
done
done