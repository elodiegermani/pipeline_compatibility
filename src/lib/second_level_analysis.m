function [] = second_level_analysis(dataset1, dataset2)

    for n = 0:999
        n = num2str(n);

        matlabbatch{1}.spm.stats.results.spmmat = {fullfile('/nfs/nas-empenn/data/share/users/egermani', 'hcp_pipelines_compatibility', 'figures', ['ER_', dataset1, '_VS_', dataset2], 
        'final_results_group_comparison', 'l2_analysis', '_contrast_right-hand', ['_n_', n], 'SPM.mat')};
        matlabbatch{1}.spm.stats.results.conspec.titlestr = '';
        matlabbatch{1}.spm.stats.results.conspec.contrasts = Inf;
        matlabbatch{1}.spm.stats.results.conspec.threshdesc = 'FWE';
        matlabbatch{1}.spm.stats.results.conspec.thresh = 0.05;
        matlabbatch{1}.spm.stats.results.conspec.extent = 0;
        matlabbatch{1}.spm.stats.results.conspec.conjunction = 1;
        matlabbatch{1}.spm.stats.results.conspec.mask.none = 1;
        matlabbatch{1}.spm.stats.results.units = 1;
        matlabbatch{1}.spm.stats.results.export{1}.tspm.basename = 'thresholded_FWE';

        spm_jobman('run',matlabbatch);
        clear matlabbatch;
    end 