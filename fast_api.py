import flask
import goless
import operator
from flask import Flask
flask_app = Flask(__name__)


@flask_app.route('/')
def index():
    return 'Index Page'


# Status URL for ops purpose

#
# @flask_app.route('/keywords/', methods=['POST'])
# def keywords():
#     l = {}
#     comp_str = ""
#     response = {}
#
#     payload = flask.request.get_json(force=True)
#     keywords = payload["keywords"]
#     title = payload["title"]
#     title = nlp(title)
#     Asin = payload["Asin"]
#     sort = payload["sort"]
#
#     if sort:
#         comp_str = title
#         with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
#
#             for (word, score) in executor.map(get_score, keywords):
#                 response[word] = score
#
#         result = {}  # dictionary to keep output
#         key = []  # list to store keywords and relevance_score
#         result["ASIN"] = Asin
#         sorted_l = sorted(response.items(), key=operator.itemgetter(1), reverse=True)
#         for r in sorted_l:
#             key.append({'keyword': r[0], 'relevance_score': r[1]})
#         result["result"] = key
#         return flask.jsonify(result)
#
#     else :
#         result = {"keywords": keywords}
#         return flask.jsonify(result)


@flask_app.route('/keywordsV2/', methods=['POST'])
def keywords():
    from app import nlp
    l = {}
    payload = flask.request.get_json(force=True)
    keywords = payload["keywords"]
    title = payload["title"]
    title = nlp(title)
    Asin = payload["Asin"]
    sort = payload["sort"]

    chn = goless.chan()

    for k in keywords:
        goless.go(get_score, k, title,chn)

    for k1 in keywords:
        l[k1] = chn.recv()

    if sort:
         result = {}  # dictionary to keep output
         key = []  # list to store keywords and relevance_score
         result["ASIN"] = Asin
         sorted_l = sorted(l.items(), key=operator.itemgetter(1), reverse=True)

         for r in sorted_l:
             key.append({'keyword': r[0], 'relevance_score': r[1]})
             result["result"] = key
         return flask.jsonify(result)
    else :
        result = {}  # dictionary to keep output
        key = []  # list to store keywords and relevance_score
        result["ASIN"] = Asin
        for r in l:
            key.append({'keyword': r[0], 'relevance_score': r[1]})
            result["result"] = key
        return flask.jsonify(result)

def get_score(keyword,comp_str,chn):
    from app import nlp
    doc1 = nlp(keyword)
    chn.send(doc1.similarity(comp_str))




