#!/bin/bash

# Parameters
expe_name="hcp_pipelines"
main_script=/srv/tempdd/egermani/hcp_pipelines/src/second_level_analysis_non_param.m


echo "Create dir for log"
CURRENTDATE=`date +"%Y-%m-%d"`
echo "currentDate :"
echo $CURRENTDATE
PATHLOG="/srv/tempdd/egermani/Logs/${CURRENTDATE}_OARID_${OAR_JOB_ID}/"
echo "path log :"
echo $PATHLOG
mkdir $PATHLOG
chmod 777 $PATHLOG

. /etc/profile.d/modules.sh

set -x

module load spack/octave/5.2.0 


spm_path="/srv/tempdd/egermani/spm12-r7771"
src_path="/srv/tempdd/egermani/hcp_pipelines/src/lib"
contrast='rh'
for f1 in 8
do 
	for p1 in 0
	do 
		for h1 in 0
		do
			datasetA="DATASET_SOFT_SPM_FWHM_${f1}_MC_PARAM_${p1}_HRF_${h1}"
			datasetB="DATASET_SOFT_SPM_FWHM_${f1}_MC_PARAM_${p1}_HRF_${h1}"
			result_dir="/srv/tempdd/egermani/hcp_pipelines/figures/ER_${datasetA}_VS_${datasetB}"
			data_path1="/srv/tempdd/egermani/pipeline_transition/data/original/subject_level/${datasetA}/original"
			data_path2="/srv/tempdd/egermani/pipeline_transition/data/original/subject_level/${datasetB}/original"
			groups_file="/srv/tempdd/egermani/hcp_pipelines/figures/groups.csv"
			octave --eval "addpath $spm_path; addpath $src_path; second_level_analysis('$datasetA', '$datasetB', '$contrast')"
done
done
done

