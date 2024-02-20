import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.stats
from matplotlib import rc
import nibabel as nib
import random
import pylab as py

def voxel_concat(
    pipeline_1:str, 
    pipeline_2:str, 
    result_dir:str
):
    '''
    Concatenate voxels from all group comparison statistic maps.
    '''
    vox_vect_1=[]
    vox_vect_2=[]

    for i in range(1000):
        
        stat_img_1 = nib.load(
            os.path.join(
                result_dir, 
                f'ER_{pipeline_1}_VS_{pipeline_2}',
                'final_results_group_comparison',
                'l2_analysis',
                '_contrast_right-hand',
                f'_n_{i}',
                'spmT_0001.nii'
            )
        ).get_fdata().flatten()

        stat_img_2 = nib.load(
            os.path.join(
                result_dir, 
                f'ER_{pipeline_1}_VS_{pipeline_2}',
                'final_results_group_comparison',
                'l2_analysis',
                '_contrast_right-hand',
                f'_n_{i}',
                'spmT_0002.nii'
            )
        ).get_fdata().flatten()
        
        mask_img = nib.load(
            os.path.join(
                result_dir, 
                f'ER_{pipeline_1}_VS_{pipeline_2}',
                'final_results_group_comparison',
                'l2_analysis',
                '_contrast_right-hand',
                f'_n_{i}',
                'mask.nii'
            )
        ).get_fdata().flatten()
        
        masked_stat_img_1 = stat_img_1[mask_img!=0].tolist()
        masked_stat_img_2 = stat_img_2[mask_img!=0].tolist()
        
        vox_vect_1 = vox_vect_1 + masked_stat_img_1
        vox_vect_2 = vox_vect_2 + masked_stat_img_2
        
    return vox_vect_1, vox_vect_2

def save_sample(
    data,
    name
): 
    ''' 
    Sample 1,000,000 values from voxel sample and save in file.
    '''
    
    random.seed(0)
    
    data_sample=random.sample(
        data, 
        1000000
    )
    
    sample_file = open(name+".txt","w")
    
    for i in range(1000000):
        
        sample_file.write(str(data_sample[i]))
        
        if i!=999999:
            sample_file.write(" \n")
            
    sample_file.close()

def voxel_concat_sample(
    pipeline_1, 
    pipeline_2, 
    sample_dir,
    result_dir
):
    '''
    Concatenate samples and save in files if not already done.
    If already done, just load saved sample. 
    '''
    
    if not (
        os.path.isfile(
            os.path.join(sample_dir, 'sample_'+pipeline_1+'_'+pipeline_2+'.txt'))
        ) or not (
        os.path.isfile(
            os.path.join(sample_dir, 'sample_'+pipeline_2+'_'+pipeline_1+'.txt')
        )):
        
        vox_vect_1, vox_vect_2 = voxel_concat(
            pipeline_1, 
            pipeline_2, 
            result_dir
        )
        
        save_sample(
            vox_vect_1,
            os.path.join(sample_dir, 'sample_'+pipeline_1+'_'+pipeline_2)
        )

        save_sample(
            vox_vect_2,
            os.path.join(sample_dir, 'sample_'+pipeline_2+'_'+pipeline_1)
        )

    
    with open(
        os.path.join(sample_dir, 'sample_'+pipeline_1+'_'+pipeline_2+'.txt'),
        "r"
    ) as sample:
        
        filecontents_1 = sample.readlines()
        
    vox_vect_sample_1 = [float(i) for i in filecontents_1]

    with open(
        os.path.join(sample_dir, 'sample_'+pipeline_2+'_'+pipeline_1+'.txt'),
        "r"
    ) as sample:
        
        filecontents_2 = sample.readlines()
        
    vox_vect_sample_2= [float(i) for i in filecontents_2]
    
    return vox_vect_sample_1, vox_vect_sample_2