from lib import samples, plots
import matplotlib.pyplot as plt
import os

def compute_samples(
	samples_dir, 
	figures_dir
	):

	for f in [5, 8]:
		for m in [0, 6, 24]:
			for h in [0, 1]:
				data = samples.voxel_concat_sample(
					f'spm-{f}-{m}-{h}', 
					f'fsl-{f}-{m}-{h}', 
					samples_dir,
					figures_dir
				)

	for f in [5]:
		for m in [0, 6, 24]:
			for h in [0, 1]:
				data_1, data_2 = samples.voxel_concat_sample(
					f'fsl-5-{m}-{h}', 
					f'fsl-8-{m}-{h}', 
					samples_dir,
					figures_dir
				)

	for f in [5, 8]:
		for m in [24]:
			for h in [0, 1]:
				data_1, data_2 = samples.voxel_concat_sample(
					f'fsl-{f}-24-{h}', 
					f'fsl-{f}-0-{h}', 
					samples_dir,
					figures_dir
				)

	for f in [5, 8]:
		for m in [24]:
			for h in [0, 1]:
				data_1, data_2 = samples.voxel_concat_sample(
					f'fsl-{f}-24-{h}', 
					f'fsl-{f}-6-{h}', 
					samples_dir,
					figures_dir
				)

	for f in [5, 8]:
		for m in [0, 6, 24]:
			for h in [0]:
				data_1, data_2 = samples.voxel_concat_sample(
					f'fsl-{f}-{m}-0', 
					f'fsl-{f}-{m}-1', 
					samples_dir,
					figures_dir
				)

	for f in [5, 8]:
		for m in [24]:
			for h in [0, 1]:
				data_1, data_2 = samples.voxel_concat_sample(
					f'fsl-{f}-6-{h}', 
					f'fsl-{f}-0-{h}', 
					samples_dir,
					figures_dir
				)

	for f in [5]:
		for m in [24]:
			for h in [0, 1]:
				data_1, data_2 = samples.voxel_concat_sample(
					f'fsl-5-24-{h}', 
					f'fsl-8-0-{h}', 
					samples_dir,
					figures_dir
				)

	for f in [5]:
		for m in [0,6,24]:
			for h in [0]:
				data_1, data_2 = samples.voxel_concat_sample(
					f'fsl-5-{m}-0', 
					f'fsl-8-{m}-1', 
					samples_dir,
					figures_dir
				)

if __name__ == '__main__':
	
	samples_dir = '/nfs/nas-empenn/data/share/users/egermani/hcp_pipelines_compatibility/figures/samples'
	figures_dir = '/nfs/nas-empenn/data/share/users/egermani/hcp_pipelines_compatibility/figures'

	compute_samples(
		samples_dir, 
		figures_dir
		)