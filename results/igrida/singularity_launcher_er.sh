#!/bin/bash

output_file=$PATHLOG/$OAR_JOB_ID.txt

# Parameters
expe_name="preproc"
main_script=/srv/tempdd/egermani/hcp_pipelines_compatibility/results/error_rate_computation.py

echo "Create dir for log"
CURRENTDATE=`date +"%Y-%m-%d"`
echo "currentDate :"
echo $CURRENTDATE
PATHLOG="/srv/tempdd/egermani/Logs/${CURRENTDATE}_OARID_${OAR_JOB_ID}"

output_file=$PATHLOG/$OAR_JOB_ID.txt


source /opt/miniconda-latest/etc/profile.d/conda.sh
source /opt/miniconda-latest/bin/activate
conda activate neuro

for f in 5 8
do 
	for m in 0 6 24
	do
		for h in 0 1
		do 
			group1=spm-"$f"-"$m"-"$h"
			group2=fsl-"$f"-"$m"-"$h"
			r=/nfs/nas-empenn/data/share/users/egermani/hcp_pipelines_compatibility/figures/ER_"$group1"_VS_"$group2"
			c='["right-hand"]'
			i=1000
			python3 -u $main_script --result_dir $r --n_iter $i --contrast_list $c
done 
done
done

# for f in 5
# do 
# 	for m in 0 6 24
# 	do
# 		for h in 0 1
# 		do 
# 			group1=spm-5-"$m"-"$h"
# 			group2=spm-8-"$m"-"$h"
# 			r=/nfs/nas-empenn/data/share/users/egermani/hcp_pipelines_compatibility/figures/ER_"$group1"_VS_"$group2"
# 			c='["right-hand"]'
# 			i=1000
# 			python3 -u $main_script --result_dir $r --n_iter $i --contrast_list $c
# done 
# done
# done


# for f in 5 8
# do 
# 	for m in 0
# 	do
# 		for h in 0 1
# 		do 
# 			group1=spm-"$f"-24-"$h"
# 			group2=spm-"$f"-0-"$h"
# 			r=/nfs/nas-empenn/data/share/users/egermani/hcp_pipelines_compatibility/figures/ER_"$group1"_VS_"$group2"
# 			c='["right-hand"]'
# 			i=1000
# 			python3 -u $main_script --result_dir $r --n_iter $i --contrast_list $c
# done 
# done
# done

# for f in 5 8
# do 
# 	for m in 0
# 	do
# 		for h in 0 1
# 		do 
# 			group1=spm-"$f"-24-"$h"
# 			group2=spm-"$f"-6-"$h"
# 			r=/nfs/nas-empenn/data/share/users/egermani/hcp_pipelines_compatibility/figures/ER_"$group1"_VS_"$group2"
# 			c='["right-hand"]'
# 			i=1000
# 			python3 -u $main_script --result_dir $r --n_iter $i --contrast_list $c
# done 
# done
# done

# for f in 5 8
# do 
# 	for m in 0 6 24
# 	do
# 		for h in 0
# 		do 
# 			group1=spm-"$f"-"$m"-0
# 			group2=spm-"$f"-"$m"-1
# 			r=/nfs/nas-empenn/data/share/users/egermani/hcp_pipelines_compatibility/figures/ER_"$group1"_VS_"$group2"
# 			c='["right-hand"]'
# 			i=1000
# 			python3 -u $main_script --result_dir $r --n_iter $i --contrast_list $c
# done 
# done
# done

# for f in 5
# do 
# 	for m in 24
# 	do
# 		for h in 0
# 		do 
# 			group1=spm-5-"$m"-0
# 			group2=spm-8-"$m"-1
# 			r=/nfs/nas-empenn/data/share/users/egermani/hcp_pipelines_compatibility/figures/ER_"$group1"_VS_"$group2"
# 			c='["right-hand"]'
# 			i=1000
# 			python3 -u $main_script --result_dir $r --n_iter $i --contrast_list $c
# done 
# done
# done

# for f in 5
# do 
# 	for m in 0
# 	do
# 		for h in 0 1
# 		do 
# 			group1=spm-5-24-"$h"
# 			group2=spm-8-0-"$h"
# 			r=/nfs/nas-empenn/data/share/users/egermani/hcp_pipelines_compatibility/figures/ER_"$group1"_VS_"$group2"
# 			c='["right-hand"]'
# 			i=1000
# 			python3 -u $main_script --result_dir $r --n_iter $i --contrast_list $c
# done 
# done
# done
