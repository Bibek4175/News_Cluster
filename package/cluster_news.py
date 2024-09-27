from package.clustering import clustering
from package.data_processing import process_data
from package.utils import save_file

def cluster(data):
	data_processing,filtered_term_frequencies,adjusted_matrix = process_data(data)
	result_df = clustering(data_processing,filtered_term_frequencies,adjusted_matrix)
	save_file(result_df)