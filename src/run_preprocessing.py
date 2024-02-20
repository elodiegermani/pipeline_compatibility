from lib import preprocessing

if __name__ == '__main__':
	data_dir = '/nfs/nas-empenn/data/share/users/egermani/hcp_many_pipelines/sub*right-hand*con.nii*'
	output_dir = '/srv/tempdd/egermani/hcp_many_pipelines_preprocess'
	
	preprocessing.preprocessing(data_dir, output_dir)