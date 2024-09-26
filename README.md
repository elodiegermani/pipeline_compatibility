# HCP PIPELINES COMPATIBILITY

This repository contains scripts used to explore the validity of group-level studies with subject-level contrast maps obtained with different pipelines using FSL and SPM and different parameters. 

## Table of contents
   * [Contents overview](#contents-overview)
   * [Install environment](#install-environment)
   * [Reproduce analyses](#reproduce-analyses)
   * [Reproduce figures and tables](#reproduce-figures-and-tables)

## Contents overview

### `src`

This directory contains scripts and notebooks used to launch the between-pipelines two-sample-t-test.  

### `data`

This directory will contain the results of the scripts in `src`. 

### `results`

This directory contains notebooks and scripts used to analyze the results of the between-group analyses: error rates, Bland-altman P-P plots, statistical distributions. 

### `figures`

This directory contain a `groups.csv` file containing the ids of participants included in the different groups of the between-group analyses, and will contain the figures obtained when running the notebooks in the `results` directory.

## Install environment 

To launch the between-pipelines analyses, you need to install the [NiPype](https://nipype.readthedocs.io/en/latest/users/install.html) Python package but also the original software package used in the pipeline (SPM, FSL, AFNI...). To facilitate this step, we created a Docker container based on [Neurodocker](https://github.com/ReproNim/neurodocker) that contains the necessary Python packages and software packages. To install the Docker image, two options are available. You can also launch the scripts to analyze the results inside this Docker container. 

This container can be downloaded here:
```bash
docker pull elodiegermani/open_pipeline:latest
```

To launch thresholding, you will also need to install [SPM12](https://www.fil.ion.ucl.ac.uk/spm/software/spm12/) and run it natively (under Octave or Matlab, not Nipype). 

## Reproduce analyses

### Subject-level analyses

Details of the subject-analyses performed as part of the HCP multi-pipeline dataset can be found in the corresponding repository: [hcp_pipelines](https://gitlab.inria.fr/egermani/hcp_pipelines).

### Data preprocessing
In some cases, you might want to preprocess your data before performing between-pipelines analyses. 
This can be done using `src/lib/preprocessing.py`. You must use the function `preprocessing(data_dir, output_dir, resolution, scale_factor)`. 
This will perform resampling to MNI152 template, at the chosen resolution, masking with the MNI152 brain mask and rescaling to a chosen factor (can be useful if comparing FSL and SPM data).

In the study, we used : `resolution=4, scale_factor=0.4` for SPM and `resolution=4, scale_factor=0.01`.

### Between-pipelines analyses 

#### Two-sample t-test 
Between-group analysis can be used to obtain group statistic maps comparing groups of the same pipeline or of different pipelines. These can then be used to compute error rates between pipelines. 
These can be done using the `src/run_between_groups_analysis.py`
How to use:
```bash
python3 between_groups_analysis.py -g1 /srv/tempdd/egermani/hcp_pipelines/data/derived/"$dataset1"/original -g2 /srv/tempdd/egermani/hcp_pipelines/data/derived/"$dataset2"/original -S '["100206", ...]' -c '["rh"]' -r /srv/tempdd/egermani/hcp_pipelines/figures/ER_"$dataset1"_VS_"$dataset2" -i 1000
```
This will compute the between-group maps between dataset1 and dataset2, for 1000 groups. If you want to use precomputed groups, the csv file must be stored in the base directory of the one used in the -r option (here, `/srv/tempdd/egermani/hcp_pipelines/figures/groups.csv` for the example here). If not, groups will be randomly chosen. 

This script only computes unthresholded statistic maps. 

#### Thresholding 
Thresholding is performed outside of the Docker container because it uses Octave and SPM. The script to use is `src/lib/second_level_analysis.m`. 
The path to find the files must be modified depending on where you stored the results of the two-sample t-test. 

### Error rates computation 
After performing two-sample t-tests and thresholding, you might want to compute the error rate. This can be done using `results/error_rate_computation.py`. 
How to use:
```bash
python3 error_rate_computation.py -g1 /srv/tempdd/egermani/hcp_pipelines/data/derived/"$dataset1"/original -g2 /srv/tempdd/egermani/hcp_pipelines/data/derived/"$dataset2"/original -S '["100206", ...]' -c '["rh"]' -r /srv/tempdd/egermani/hcp_pipelines/figures/ER_"$dataset1"_VS_"$dataset2" -i 1000

```

### Samples for P-P plots
After performing two-sample t-tests and thresholding, you might want to compute the samples to build the P-P plots. This can be done using `results/samples_computation.py`. 
How to use:

```bash
python3 samples_computation.py
```

## Reproduce figures and tables

Figures and Tables can be reproduced using the notebook available in the `results` directory. This requires to have run all the steps above beforehand.
