from glob import glob
from nilearn.image import resample_img, resample_to_img
from nilearn import datasets, plotting, masking, image
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
import os.path as op
import os
import nipype.interfaces.fsl as fsl 

def get_imlist(images):
    '''
    Search for the list of images in the repository "images" that are in NiFti file format.
    
    Parameters:
        - images: str, path to the directory containing images or list, list of the paths to images
        
    Return:
        - files: list, list containing all paths to the images
        - inpdir: boolean, True if images is the directory containing the images, False otherwise
    '''
    files = sorted(glob(images))
    inpdir = True

    return files, inpdir

def compute_intersection_mask(data, pipeline):
    '''
    Compute intersection mask of images located in a directory and resample this mask to MNI.

    Parameters
    ----------
    data : list
        List of images images

    Returns
    -------
    mask : Nifti1Image
        Mask image
    '''
    img_list = []
    mask_list = []

    target = nib.load(fsl.Info.standard_image('MNI152_T1_2mm_brain_mask.nii.gz')) #datasets.load_mni152_gm_template(4)

    print('Computing mask for pipeline', pipeline)
    data_pipeline = [f for f in data if pipeline in f]

    print('Number of masks:', len(data_pipeline))
    for fpath in data_pipeline:
        try:
            img = nib.load(fpath)
        except:
            os.rename(fpath, f'{fpath}.gz')
            img = nib.load(f'{fpath}.gz')

        mask_img = image.binarize_img(img)

        resampled_mask = image.resample_to_img(
                    mask_img,
                    target,
                    interpolation='nearest')

        mask_list.append(resampled_mask)
    print('All subjects masks resampled.')

    mask = masking.intersect_masks(mask_list, threshold=1)

    return mask

def postprocessing(data_dir, output_dir):
    '''
    Preprocess all maps that are stored in the 'original' repository of the data_dir. 
    Store these maps in subdirectories of the data_dir corresponding to the preprocessing step applied.


    Parameters:
        - data_dir, str: path to directory where 'original' directory containing all original images is stored
        - output_dir, str: path to directory where 'preprocessed' directory is stored and where all preprocessed images will be stored.

    '''
    # Get image list to preprocess
    img_list, input_dir = get_imlist(op.join(data_dir))
        
    # Create dirs to save images
    if not op.isdir(op.join(output_dir, f'postprocessed')):
        os.mkdir(op.join(output_dir, f'postprocessed'))

    # Load standard image 
    standard = nib.load(fsl.Info.standard_image('MNI152_T1_2mm.nii.gz'))
    pipeline_list = ['fsl-5-0-0', 'fsl-5-0-1', 'fsl-8-0-0', 'fsl-8-0-1', 'fsl-5-6-0', 'fsl-5-6-1', 'fsl-8-6-0', 
        'fsl-8-6-1','fsl-5-24-0', 'fsl-5-24-1', 'fsl-8-24-0', 'fsl-8-24-1',
        'spm-5-0-0', 'spm-5-0-1', 'spm-8-0-0', 'spm-8-0-1', 'spm-5-6-0', 'spm-5-6-1', 'spm-8-6-0', 'spm-8-6-1',
        'spm-5-24-0', 'spm-5-24-1', 'spm-8-24-0', 'spm-8-24-1']

    ## Search for mask or compute intersection mask between images of ALL pipelines if first time
    if not os.path.exists(op.join(output_dir, f'postprocessed', 'mask.nii.gz')):
        mask_list = []
        # 1 - Compute mask per pipeline
        
        for pipeline in pipeline_list: # To adapt if you use less pipelines
            if not os.path.exists(op.join(output_dir, f'postprocessed', f'{pipeline}-mask.nii.gz')):
                pipeline_mask = compute_intersection_mask(img_list, pipeline)
                nib.save(pipeline_mask, op.join(output_dir, f'postprocessed', f'{pipeline}-mask.nii.gz'))
            else:
                pipeline_mask = nib.load(op.join(output_dir, f'postprocessed', f'{pipeline}-mask.nii.gz'))
                
            mask_list.append(pipeline_mask)

        # 2 - Compute mask for ALL pipeline
        mask = masking.intersect_masks(mask_list, threshold=1)
        nib.save(mask, op.join(output_dir, f'postprocessed', 'mask.nii.gz'))

    else:
        mask = nib.load(op.join(output_dir, f'postprocessed', 'mask.nii.gz'))
    
    for idx, img in enumerate(img_list):
        print('Image', img)
        img_pipeline = [p for p in pipeline_list if p in img][0]
        print('Pipeline', img_pipeline)
        img_sub = op.basename(img).split('_')[0]
        print('Subject', img_sub)

        if os.path.exists(op.join(output_dir, f'postprocessed', img_pipeline, 'node-L1', img_sub, op.basename(img))):
            pass

        if not os.path.isdir(op.join(output_dir, 'postprocessed', img_pipeline)):
            os.mkdir(op.join(output_dir, 'postprocessed', img_pipeline))
            os.mkdir(op.join(output_dir, 'postprocessed', img_pipeline, 'node-L1'))

        if not os.path.isdir(op.join(output_dir, 'postprocessed', img_pipeline, 'node-L1', img_sub)):
            os.mkdir(op.join(output_dir, 'postprocessed', img_pipeline, 'node-L1', img_sub))

        # Transform NaN to 0s
        nib_img = nib.load(img)

        img_data = nib_img.get_fdata()
        img_data = np.nan_to_num(img_data)

        img_affine = nib_img.affine
        nib_img = nib.Nifti1Image(img_data, img_affine)
        
        print('Original shape of image ', idx+1, ':',  nib_img.shape)

        try:
            # Resample to standard image
            print("Resampling image {0} of {1}...".format(idx + 1, len(img_list)))
            
            res_img = resample_to_img(
                nib_img, 
                standard, 
                interpolation='continuous'
            )

            print('New shape for image', idx, res_img.shape)            
            print("Masking image {0} of {1}...".format(idx + 1, len(img_list)))
            
            # Apply mask 
            mask_data = mask.get_fdata()
            res_img_data = res_img.get_fdata()
            res_masked_img_data = res_img_data * mask_data

            # Rescale images
            scale_factor = 1
            # if 'fsl' in img_pipeline:
            #     scale_factor = 0.01
            # elif 'spm' in img_pipeline:
            #     scale_factor = 0.4
            print('Rescaling image...')
            res_masked_scaled_img_data = res_masked_img_data * scale_factor

            res_masked_scaled_img = nib.Nifti1Image(res_masked_scaled_img_data, res_img.affine)            
            
            nib.save(res_masked_scaled_img, op.join(output_dir, f'postprocessed', img_pipeline, 'node-L1', img_sub, op.basename(img))) # Save original image resampled and normalized

            print(f"Image {idx} : DONE.")

        except Exception as e:
            print("Failed!")
            print(e)
            continue