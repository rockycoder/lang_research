import concurrent.futures
import flask
from flask import Flask
flask_app = Flask(__name__)
from app import nlp
import operator

@flask_app.route('/')
def index():
    return 'Index Page'


# Status URL for ops purpose


@flask_app.route('/keywords/', methods=['POST'])
def keywords():
    payload = flask.request.get_json(force=True)
    keywords = payload["keywords"]
    title = payload["title"]
    title = nlp(title)
    Asin = payload["Asin"]
    sort = payload["sort"]
    response = {}
    if sort:

        with concurrent.futures.ProcessPoolExecutor(max_workers= 4) as executor:

            for (word, score) in executor.map(get_score, keywords, title):
                response[word] = score

        result = {}  # dictionary to keep output
        key = []  # list to store keywords and relevance_score
        result["ASIN"] = Asin
        sorted_l = sorted(response.items(), key=operator.itemgetter(1), reverse=True)
        for r in sorted_l:
            key.append({'keyword': r[0], 'relevance_score': r[1]})
        result["result"] = key
        return flask.jsonify(result)

    else :
        result = {"keywords": keywords}
        return flask.jsonify(result)




def get_score(keyword, comp_str):
    doc1 = nlp(keyword)
    return keyword, doc1.similarity(comp_str)