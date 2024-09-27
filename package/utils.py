def save_file(df):
    df3['Cluster'] = clusters

    grouped = df3.groupby('Cluster')
    data = {}

    for cluster,group in grouped:
        data[f'Cluster {cluster}'] = group[['url','title','published_time']].to_dict()
    with open('cluster_analysis.json', 'w') as file:
        json.dump(data,file,ensure_ascii=False,indent=4)


