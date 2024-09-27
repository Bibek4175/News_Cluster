import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity

def clustering(df,filtered_df,adjusted_matrix):

	vectorizer = TfidfVectorizer(ngram_range=(1,3))
	vectorizer_filtered = TfidfVectorizer(vocabulary=filtered_df['Feature'])
	X1 = vectorizer_filtered.fit_transform(df['np']).toarray()
	X2 = vectorizer_filtered.fit_transform(df['title']).toarray()

	X2 = 2 * X2

	combined_vectors = np.hstack((X1,X2,adjusted_matrix))


	dbscan =DBSCAN(eps=0.25,min_samples=1,metric='cosine')
	clusters = dbscan.fit_predict(combined_vectors)

	df['Cluster'] = clusters

	return df 
