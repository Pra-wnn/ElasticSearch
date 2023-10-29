# from elasticsearch import Elasticsearch

# import csv

# es = Elasticsearch(hosts=["http://127.0.0.1:9200"])

# print(f"Connected to ElasticSearch cluster `{es.info().body['cluster_name']}`")

# with open("./Car details v3.csv", "r") as f:
#     reader = csv.reader(f)

#     for i, line in enumerate(reader):
#         document = {
#             "name": line[0],
#             "engine": line[9],
#             "year": line[1],
#             "price": line[2],
#         }
#         es.index(index="cars", document=document)

from elasticsearch import Elasticsearch
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=["http://127.0.0.1:9200"])

# Define index settings and mappings
index_settings = {
    "settings": {
        "analysis": {
            "analyzer": {
                "standard": {
                    "type": "standard",
                    "filter": ["lowercase", "asciifolding"]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "name": {
                "type": "text",
                "analyzer": "standard",
                "search_analyzer": "standard",
                "fielddata": True,
                "fielddata_frequency_filter": {
                    "min": 0.001,
                    "max": 0.1,
                    "min_segment_size": 100
                },
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                },
                "index_options": "positions"
            }
        }
    }
}

# Create the index with settings and mappings
es.indices.create(index="text_data", body=index_settings)


es = Elasticsearch(hosts=["http://127.0.0.1:9200"])

print(f"Connected to ElasticSearch cluster `{es.info().body['cluster_name']}`")

with open("./data.txt", "r",encoding="utf-8") as f:
    lines = f.readlines()

    for i, line in enumerate(lines):
        document = {
            "name": line.strip(),  # Use the entire line as the 'name' field
            "line_number": i  # Optional: store the line number as an identifier
        }
        es.index(index="text_data", document=document)
