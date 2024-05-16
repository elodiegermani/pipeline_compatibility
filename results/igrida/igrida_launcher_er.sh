#!/bin/bash

# Parameters
expe_name="preproc"
main_script=/srv/tempdd/egermani/hcp_pipelines_compatibility/results/singularity_launcher_er.sh


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

module load spack/singularity
singularity exec -B /srv/tempdd/egermani -B /nfs/nas-empenn/data/share/users/egermani/hcp_pipelines_compatibility /srv/tempdd/egermani/open_pipeline_latest.sif $main_script