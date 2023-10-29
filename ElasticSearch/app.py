# from flask import Flask, request, render_template
# from elasticsearch import Elasticsearch
# from flask_cors import CORS,cross_origin

# es = Elasticsearch(hosts=["http://127.0.0.1:9200"])
# print(f"Connected to ElasticSearch cluster `{es.info().body['cluster_name']}`")

# app = Flask(__name__)
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

# MAX_SIZE = 15

# @app.route("/")
# @cross_origin()
# def home():
#     return render_template("index.html")


# @app.route("/search")
# def search_autocomplete():
#     query = request.args["q"].lower()
#     tokens = query.split(" ")

#     clauses = [
#         {
#             "span_multi": {
#                 "match": {"fuzzy": {"name": {"value": i, "fuzziness": "AUTO"}}}
#             }
#         }
#         for i in tokens
#     ]

#     payload = {
#         "bool": {
#             "must": [{"span_near": {"clauses": clauses, "slop": 0, "in_order": False}}]
#         }
#     }

#     resp = es.search(index="cars", query=payload, size=MAX_SIZE)
#     return [result['_source']['name'] for result in resp['hits']['hits']]


# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request, render_template
from elasticsearch import Elasticsearch
from flask_cors import CORS, cross_origin

es = Elasticsearch(hosts=["http://127.0.0.1:9200"])
print(f"Connected to ElasticSearch cluster `{es.info().body['cluster_name']}`")

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

MAX_SIZE = 15

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/search")
def search_autocomplete():
    query = request.args["q"].lower()

    payload = {
        "query": {
            "match": {
                "name": {
                    "query": query,
                    "fuzziness": "AUTO"
                }
            }
        }
    }

    resp = es.search(index="text_data", body=payload, size=MAX_SIZE)
    return [result['_source']['name'] for result in resp['hits']['hits']]

if __name__ == "__main__":
    app.run(debug=True)
