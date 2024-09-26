#python3
# This script performs error rate computation between two datasets.
import numpy as np
import nibabel as nib 
from glob import glob
from os.path import join as opj
import os
import sys
import getopt
import json
import warnings
import csv
from nilearn import plotting
import matplotlib.pyplot as plt

# import warnings filter
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=UserWarning)
simplefilter(action='ignore', category=RuntimeWarning)

def compute_error_rate(result_dir, n_iter, contrast_list):
    '''
    Compute error rate between the two groups by taking the percentage of images having at least one active voxel among the n_iter images.

    Parameters:
        - result_dir: str, path to the directory where to find the results of the two sample t-tests between groups
        - n_iter: int, number of iterations performed (default=1000)
        - contrast_list: list of str, contrast for which to perform the calcul

    Output: 
        - ER_1: float, error rate for group1 > group2 analysis
        - ER_2: float, error rate for group2 > group1 analysis
    '''
    print('Computing error rate...')

    frac_1=[]
    frac_2=[]

    for contrast in contrast_list: 
        for i in range(n_iter):
            # Files for contrast and iteration
            stat_map_1 = opj(result_dir, f'final_results_group_comparison', 'l2_analysis', f'_contrast_{contrast}', 
                          f'_n_{i}', 'spmT_0001_thresholded_FWE.nii')
            stat_map_2 = opj(result_dir, f'final_results_group_comparison', 'l2_analysis', f'_contrast_{contrast}',
                          f'_n_{i}', 'spmT_0002_thresholded_FWE.nii')
            mask = opj(opj(result_dir, f'final_results_group_comparison', 'l2_analysis', f'_contrast_{contrast}',
                          f'_n_{i}', 'mask.nii'))
            # Remove NaNs
            stat_map_1_data = np.nan_to_num(nib.load(stat_map_1).get_fdata()) 
            stat_map_2_data = np.nan_to_num(nib.load(stat_map_2).get_fdata()) 

            mask_data = np.nan_to_num(nib.load(mask).get_fdata()) 

            # Apply mask
            stat_map_1_data = stat_map_1_data * mask_data
            stat_map_2_data = stat_map_2_data * mask_data

            # Vectorize
            stat_map_1_data = np.reshape(stat_map_1_data, -1)
            stat_map_2_data = np.reshape(stat_map_2_data, -1)

            # Search for activated voxels
            if np.any(stat_map_1_data != 0):
                print(f'Image {i} contains errors.')
                frac_1.append(1)
            if  np.any(stat_map_2_data != 0):
                print(f'Image {i} contains errors.')
                frac_2.append(1)
            
        #print(len(frac_1), len(frac_2))

    ER_1 = len(frac_1)/n_iter
    ER_2 = len(frac_2)/n_iter
    print(result_dir)
    print(ER_1, ER_2)

    return ER_1, ER_2

def compute_error_rate_non_param(result_dir, n_iter, contrast_list):
    '''
    Compute error rate between the two groups by taking the percentage of images having at least one active voxel among the n_iter images.

    Parameters:
        - result_dir: str, path to the directory where to find the results of the two sample t-tests between groups
        - n_iter: int, number of iterations performed (default=1000)
        - contrast_list: list of str, contrast for which to perform the calcul

    Output: 
        - ER_1: float, error rate for group1 > group2 analysis
        - ER_2: float, error rate for group2 > group1 analysis
    '''
    print('Computing error rate...')

    frac_1=[]
    frac_2=[]

    for contrast in contrast_list: 
        for i in range(1, n_iter+1):
            # Files for contrast and iteration
            stat_map_1 = opj(result_dir,  
                          f'_n_{i}', 'lP_FWE+.img')
            stat_map_2 = opj(result_dir, 
                          f'_n_{i}', 'lP_FWE+.img')
            mask = opj(opj(result_dir, 
                          f'_n_{i}', 'mask.nii'))

            # Remove NaNs
            stat_map_1_data = np.nan_to_num(nib.load(stat_map_1).get_fdata()) 
            stat_map_2_data = np.nan_to_num(nib.load(stat_map_2).get_fdata()) 

            #mask_data = np.nan_to_num(nib.load(mask).get_fdata()) 

            # Apply mask
            #stat_map_1_data = stat_map_1_data * mask_data
            #stat_map_2_data = stat_map_2_data * mask_data

            # Vectorize
            stat_map_1_data = np.reshape(stat_map_1_data, -1)
            stat_map_2_data = np.reshape(stat_map_2_data, -1)

            # Search for activated voxels
            if np.any(stat_map_1_data != 0):
                #print(f'Image {i} contains errors.')
                frac_1.append(1)
            if  np.any(stat_map_2_data != 0):
                #print(f'Image {i} contains errors.')
                frac_2.append(1)
            
        #print(len(frac_1), len(frac_2))

    ER_1 = len(frac_1)/n_iter
    ER_2 = len(frac_2)/n_iter

    print(ER_1)

    return ER_1, ER_2
            
if __name__ == "__main__":
    contrast_list = None
    result_dir = None
    n_iter = None 

    # Usage: python3 -g1 /srv/tempdd/egermani/hcp_pipelines/data/derived/dataset1 -g2 /srv/tempdd/egermani/hcp_pipelines/data/derived/dataset2 -S '["100206", ...]' -c '["rh"]' -r /srv/tempdd/egermani/hcp_pipelines/figures -i 1000
    try:
        OPTIONS, REMAINDER = getopt.getopt(sys.argv[1:], 'c:r:i', ['contrast_list=', 'result_dir=', 'n_iter='])

    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    # Replace variables depending on options
    for opt, arg in OPTIONS:
        if opt in ('-c', '--contrast_list'): 
            contrast_list = json.loads(arg)
        elif opt in ('-r', '--result_dir'):
            result_dir = str(arg)
        elif opt in ('-i', '--n_iter'):
            n_iter = int(arg)


    print('OPTIONS   :', OPTIONS)
    
    
    compute_error_rate(result_dir, n_iter, contrast_list)
