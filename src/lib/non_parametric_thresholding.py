from nipype.interfaces import spm
matlab_cmd = '/opt/spm12-r7771/run_spm12.sh /opt/matlabmcr-2010a/v713/ script'
spm.SPMCommand.set_mlab_paths(matlab_cmd=matlab_cmd, use_mcr=True)

from nipype.interfaces.spm import (Coregister, Smooth, OneSampleTTestDesign, EstimateModel, EstimateContrast, 
                                   Level1Design, TwoSampleTTestDesign, Realign, 
                                   Normalize12, NewSegment)
from nipype.interfaces.fsl import (BET, ICA_AROMA, FAST, MCFLIRT, FLIRT, FNIRT, ApplyWarp, SUSAN, 
                                   Info, ImageMaths, IsotropicSmooth, Threshold, Level1Design, FEATModel, 
                                   L2Model, Merge, FLAMEO, ContrastMgr,Cluster,  FILMGLS, Randomise, MultipleRegressDesign)
from nipype.interfaces.fsl import ExtractROI, Info
from nipype.interfaces.spm import Threshold 
from nipype.algorithms.modelgen import SpecifySPMModel
from nipype.interfaces.utility import IdentityInterface, Function
from nipype.interfaces.io import SelectFiles, DataSink
from nipype.algorithms.misc import Gunzip
from nipype import Workflow, Node, MapNode, JoinNode
from nipype.interfaces.base import Bunch

from os.path import join as opj
import os
import json


def get_groups_maps(group1_files, group2_files, subject_list, n):
    ''' 
    Functions to get corresponding files depending on subject list to use. 
    Parameters:
        - group1_files: list of str representing existing files, all files for group 1
        - group2_files: list of str representing existing files, all files for group 2
        - subject_list: list of list of str, lists of subjects to use for each iteration
        - n: int, iteration to make

    Outputs:
        - group1_sublist: list of str representing existing files, files corresponding to selected subjects for group1
        - group2_sublist: list of str representing existing files, files corresponding to selected subjects for group2
    '''
    group1_sublist = []
    group2_sublist = []

    group1_subjects = subject_list[n][:int(len(subject_list[n])/2)] # Select the n-th list of subject and split it to obtain the two groups
    group2_subjects = subject_list[n][int(len(subject_list[n])/2):]

    for file in group1_files:
        sub_id = file.split('/')[-1].split('_')[-3]
        if sub_id in group1_subjects:
            group1_sublist.append(file)  # Get the files corresponding to subjects from the first part of the n-th list of subjects 

    for file in group2_files:
        sub_id = file.split('/')[-1].split('_')[-3]
        if sub_id in group2_subjects:
            group2_sublist.append(file) 

    group1_sublist.extend(group2_sublist)
    
    print(group1_sublist)
        
    return group1_sublist
        

def get_l2_analysis(exp_dir_group1, exp_dir_group2, output_dir, working_dir, result_dir, subject_list, contrast_list): 
    """
    """         
        # Infosource - a function free node to iterate over the list of subject names
    infosource_groupanalysis = Node(IdentityInterface(fields=['contrast', 'task']),
                      name="infosource_groupanalysis")

    infosource_groupanalysis.iterables = [('contrast', contrast_list)]

    # SelectFiles templates and Node
    group1_files = opj(exp_dir_group1, 'sub_*_contrast_{contrast}.nii*')
    group2_files = opj(exp_dir_group2, 'sub_*_contrast_{contrast}.nii*')

    templates = {'group1' : group1_files, 'group2':group2_files}
    
    selectfiles_groupanalysis = Node(SelectFiles(templates, base_directory=result_dir, force_list= True),
                       name="selectfiles_groupanalysis")
    
    # Datasink node : to save important files 
    datasink_groupanalysis = Node(DataSink(base_directory = result_dir, container = output_dir), 
                                  name = 'datasink_groupanalysis')

    
    # Node to select subset of files corresponding to selected subjects
    sub_contrasts = Node(Function(input_names = ['group1_files', 'group2_files', 'subject_list', 'n'],
                                 output_names = ['group1_sublist'],
                                 function = get_groups_maps),
                        name = 'sub_contrasts')

    sub_contrasts.iterables = ('n', range(0, len(subject_list))) # Iterate on all lists of subjects 
    sub_contrasts.inputs.subject_list = subject_list
        
    merge_files_groupanalysis = Node(Merge(dimension = 't'), name = 'merge_files_groupanalysis')
    
    specifymodel_groupanalysis = Node(MultipleRegressDesign(), name = 'specifymodel_groupanalysis')
    
    regressors = dict(group1 = [i for i in [1,0] for n in range(50)], 
                  group2 = [i for i in [0,1] for n in range(50)])
    
    specifymodel_groupanalysis.inputs.regressors = regressors
    
    randomise = Node(Randomise(num_perm = 1000, vox_p_values=True, tfce=False),
                     name = "randomise")
    
    l2_analysis = Workflow(base_dir = opj(result_dir, working_dir), name = f"l2_analysis")
            
    specifymodel_groupanalysis.inputs.contrasts = [["group1_sup", "T", ["group1", "group2"],
                                               [1, -1]], ["group2_sup", "T", ["group1", "group2"],
                                               [-1, 1]]]
    
    l2_analysis.connect([(infosource_groupanalysis, selectfiles_groupanalysis, [('contrast', 'contrast')]),
                        (selectfiles_groupanalysis, sub_contrasts, [('group1', 'group1_files'), ('group2', 'group2_files')]),
                        (sub_contrasts, merge_files_groupanalysis, [('group1_sublist', 'in_files')]),
                        (merge_files_groupanalysis, randomise, [('merged_file', 'in_file')]),
                        (specifymodel_groupanalysis, randomise, [('design_mat', 'design_mat'),
                                                           ('design_con', 'tcon')]),
                        (randomise, datasink_groupanalysis, [('t_corrected_p_files', 
                                                         f"l2_analysis.@tcorpfile"),
                                                       ('tstat_files', f"l2_analysis.@tstat")]),
            ])
    
    return l2_analysis
