import flask
import spacy
from flask import Flask
from Queue import Queue
from threading import Thread
# Setup flask app
flask_app = Flask(__name__)
from app import nlp
import operator

l = {}


@flask_app.route('/')
def index():
    return 'Index Page'


# Status URL for ops purpose


@flask_app.route('/keywords/', methods=['POST'])
def keywords():
    payload = flask.request.get_json(force=True)
    keywords = payload["keywords"]
    title = payload["title"]
    Asin = payload["Asin"]
    sort = payload["sort"]
    l.clear()

    if sort:
        keywords_queue = Queue()
        max_threads = 10
        print "Populating queue"
        for keyword in keywords:
            keyword = keyword.strip()
            keywords_queue.put(keyword)

        print "Starting %d workers" % max_threads
        for i in range(max_threads):
            worker = Thread(target=task, args=(keywords_queue, title))
            worker.setDaemon(True)
            # threads.append(worker)
            worker.start()
            worker.join()
        keywords_queue.join()

        result = {}  # dictionary to keep output
        key = []  # list to store keywords and relevance_score
        result["ASIN"] = Asin
        # response, dic = get_keyword()
        response = get_keyword()
        for r in response :
            key.append({'keyword': r[0], 'relevance_score': r[1]})

        result["result"] = key
        return flask.jsonify(result)
    else:
        result = {"keywords": keywords}
        return flask.jsonify(result)


def get_keyword():
    sorted_l = sorted(l.items(), key = operator.itemgetter(1), reverse=True)
    return sorted_l


def task(queue, title):
    doc = nlp(title)
    while not queue.empty():

        word = queue.get()
        if word not in l.keys():
            doc1 = nlp(word)
            l[word] = doc1.similarity(doc)
            # sen.append(word)
        else:
            print ("exists")
        queue.task_done()

