import json
import pandas as pd
import numpy as np
import re
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_data(json_file):
    suffixes = ['कुछ', 'के साथ', 'में', 'हुए', 'हुआ', 'हमले', 'खिलाफ', 'भी', 'और', 'से करते']

    with open(json_file, "r") as file:
        data = json.load(file)

    text1, text2, url, published_time, title = [], [], [], [], []
    
    for item in data:
        text1.append(item['stem']["en_stemmed"])
        text2.append(item['stem']['np'])
        url.append(item['url'])
        published_time.append(item['published_time'])
        title.append(item['title'])

    df3 = pd.DataFrame({
        "np": text2,
        "url": url,
        "title": title,
        "published_time": published_time
    })

    pattern = '|'.join(suffixes)
    df3 = df3[~df3['np'].str.contains(pattern)]
    df3.reset_index(drop=True, inplace=True)

    return df3

def convert_date(date):
    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return int(date.timestamp())

def normalize_date_features(date_feature, min_timestamp, max_timestamp):
    return (date_feature - min_timestamp) / (max_timestamp - min_timestamp)

def compute_term_frequencies(df):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df["np"])

    feature_names = vectorizer.get_feature_names_out()
    term_frequencies = X.sum(axis=0).A1

    df_term_freq = pd.DataFrame({
        'Feature': feature_names,
        'Frequency': term_frequencies
    })

    df_term_freq_sorted = df_term_freq.sort_values(by='Frequency', ascending=False)
    filtered_df = df_term_freq_sorted[(df_term_freq_sorted['Frequency'] < 5) & (df_term_freq_sorted['Frequency'] > 0)]

    return filtered_df

def cosine_sim_matrix(df3):
    vectorizer = TfidfVectorizer(ngram_range=(1,3))
    X = vectorizer.fit_transform(df3['np'])
    cosine_matrix = cosine_similarity(X)
    return cosine_matrix



def adjust_weight(date_features,cosine_sim_matrix):
  adjusted_matrix = np.zeros_like(cosine_sim_matrix)
  for i in range(cosine_sim_matrix.shape[0]):
    for  j in range(cosine_sim_matrix.shape[1]):
      adjusted_matrix[i,j] = date_features[i] * cosine_sim_matrix[i][j]
  return adjusted_matrix

def process_data(json_file):
    df3 = load_data(json_file)

    # Convert published time to UNIX timestamp
    df3['published_time_seconds'] = df3['published_time'].apply(convert_date)

    min_timestamp = df3['published_time_seconds'].min()
    max_timestamp = df3['published_time_seconds'].max()

    # Normalize date features
    date_features= df3['published_time_seconds'].apply(lambda x: normalize_date_features(x, min_timestamp, max_timestamp))

    cosine_matrix = cosine_sim_matrix(df3)
    adjusted_matrix = adjust_weight(date_features,cosine_matrix)

    # Compute term frequencies

    filtered_term_frequencies = compute_term_frequencies(df3)

    return df3, filtered_term_frequencies,adjusted_matrix
