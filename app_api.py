import flask
import spacy
from flask import Flask
# nlp = spacy.load("en_core_web_lg")
# Setup flask app
flask_app = Flask(__name__)
from app import nlp


@flask_app.route('/')
def index():
    return 'Index Page'

# Status URL for ops purpose


@flask_app.route('/keywords/', methods=['POST'])
def keywords():
    payload  = flask.request.get_json(force=True)
    keywords    = payload["keywords"]
    title    = payload["title"]
    Asin = payload["Asin"]
    result = {}  # dictionary to keep output
    key = []  # list to store keywords and relevance_score
    result["ASIN"] = Asin
    response, dic = get_keyword(keywords, title)
    # result['keywords'] = get_keyword(words, title)
    for r in response:
        key.append({'keyword': r, 'relevance_score': dic[r]})

    result["result"] = key
    return flask.jsonify(result)


def get_keyword(words, title):
    l = {}
    li = []
    # print (type(words))
    doc = nlp(title)
    for t in words:
        doc1 = nlp(t)
        l[t.strip()] = doc1.similarity(doc)
        # print (l[t])
    print (l)

    # Function to sort the dictionary 'l' according to relevance_score
    def comp(val):
        v = val.strip()
        if v in l.keys():
            # print (-float(l[v]))
            return -float(l[v])
        else:
            return 0

    for word in sorted(words, key=comp):
        if word.strip() in l.keys():
            li.append(word)
    print (li)
    return li, l
