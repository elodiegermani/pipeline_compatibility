#python3
# This script performs group maps computation between two datasets.
# Usage: python3 -g1 /srv/tempdd/egermani/hcp_pipelines/data/derived/dataset1 -g2 /srv/tempdd/egermani/hcp_pipelines/data/derived/dataset2 -S '["100206", ...]' -c '["rh"]' -r /srv/tempdd/egermani/hcp_pipelines/figures -i 1000

import numpy as np
import nibabel as nib 
from lib import between_groups_analysis#, non_parametric_thresholding
from glob import glob
from os.path import join as opj
import os
import sys
import getopt
import json
import warnings
import csv

# import warnings filter
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=UserWarning)
simplefilter(action='ignore', category=RuntimeWarning)

def compute_group_comparison(exp_dir, group1, group2, result_dir, subject_list, contrast_list, gzip=[True, True], param=True):
    """
    Function to run Nipype workflow corresponding to group comparisons. 
    Parameters:
        - exp_dir_group1: str, path to directory where to find files from group1
        - exp_dir_group2: str, path to directory where to find files from group2
        - result_dir: str, path to directory where to store results and intermediate results
        - subject_list: list of list of str, lists of subjects to use for each iteration
        - contrast_list: list of str, list of contrast to which perform analysis 
        - gzip: list of Bool, perform gunzip or not on file for group1 and 2 (depend on wether files are already unzipped or not)
    """  

    # Important directories
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)

    ## working_dir : where the intermediate outputs will be store
    working_dir = f"intermediate_results"
    

    # Create workflow and run it
    if param==True:
        print('Perform parametric analysis')
        ## output_dir : where the final results will be store
        output_dir = f"final_results_group_comparison"
        l2_analysis_generated = between_groups_analysis.get_l2_analysis_group_comparison(exp_dir, group1, group2, output_dir, working_dir, result_dir, 
            subject_list, contrast_list, gzip=gzip)
    else:
        print('Perform non parametric analysis')
        ## output_dir : where the final results will be store
        output_dir = f"final_results_group_comparison_non_param"
        l2_analysis_generated = non_parametric_thresholding.get_l2_analysis(exp_dir, group1, group2, output_dir, 
                                            working_dir, result_dir, random_subject_list, contrast_list)
        
    l2_analysis_generated.run()#('MultiProc', plugin_args={'n_procs': 8})
        
            
if __name__ == "__main__":
    exp_dir = None
    group1 = None
    group2 = None
    subject_list = None
    contrast_list = None
    result_dir = None
    n_iter = None 
    param = None

    try:
        OPTIONS, REMAINDER = getopt.getopt(sys.argv[1:], 'e:g1:g2:S:c:r:i:p:', ['exp_dir=','group1=', 'group2=',
            'subject_list=', 'contrast_list=', 'result_dir=', 'n_iter=', 'param='])

    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    # Replace variables depending on options
    for opt, arg in OPTIONS:
        if opt in ('-e', '--exp_dir'):
            exp_dir = str(arg)
        elif opt in ('-g1', '--group1'):
            group1= str(arg)
        elif opt in ('-g2', '--group2'):
            group2 = str(arg)
        elif opt in ('-S', '--subject_list'): 
            subject_list = json.loads(arg)
        elif opt in ('-c', '--contrast_list'): 
            contrast_list = json.loads(arg)
        elif opt in ('-r', '--result_dir'):
            result_dir = str(arg)
        elif opt in ('-i', '--n_iter'):
            n_iter = int(arg)
        elif opt in ('-p', '--param'):
            param = bool(arg)


    print('OPTIONS   :', OPTIONS)

    gzip = [False, False]
    # If SPM files, already unziped so no need to re-unzip them during pipeline
    if 'spm' in group1:
        gzip[0] = False
    if 'spm' in group2:
        gzip[1] = False
    
    # If file containing list of groups doesn't exist, create it with random groups
    if not os.path.exists(opj(('/').join(result_dir.split('/')[:-1]), 'groups.csv')):
        random_subject_list = []
        for i in range(n_iter):
            random_subject_list.append(np.random.choice(subject_list, 100, False))

        with open(opj(('/').join(result_dir.split('/')[:-1]), 'groups.csv'), 'w') as file:
            for i, sub_list in enumerate(random_subject_list):
                for j, sub in enumerate(sub_list):
                    file.write(str(sub))
                    if j != 99:
                        file.write(',')
                file.write('\n')
        file.close()

    else: # Read it if it exists
        with open(opj(('/').join(result_dir.split('/')[:-1]), 'groups.csv'), 'r') as file:
            reader = csv.reader(file)
            random_subject_list = list(reader)
        file.close()

    compute_group_comparison(exp_dir, group1, group2, result_dir, random_subject_list, contrast_list, gzip=gzip, param=param)
