
from elasticsearch import Elasticsearch
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=["http://127.0.0.1:9200"])

# Define index settings and mappings
# Works with unicode chartacters such as Japnese,Chinese Characters
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
    #Change to your specific filename and path
    lines = f.readlines()

    for i, line in enumerate(lines):
        document = {
            "name": line.strip(),  # Use the entire line as the 'name' field
            "line_number": i  # Optional: store the line number as an identifier
        }
        es.index(index="text_data", document=document)
