import json
def save_file(df):

    grouped = df.groupby('Cluster')
    data = {}

    for cluster,group in grouped:
        data[f'Cluster {cluster}'] = group[['url','title','published_time']].to_dict()
    with open('cluster_analysis.json', 'w') as file:
        json.dump(data,file,ensure_ascii=False,indent=4)

    print("File saved in cluster_analysis.json")    


