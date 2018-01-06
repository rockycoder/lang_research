import flask
import spacy
from flask import Flask
from Queue import Queue
from threading import Thread
# Setup flask app
flask_app = Flask(__name__)
from app import nlp
l = {}
li = []
sen = []


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

    if sort == True:
        keywords_queue = Queue()
        max_threads = 10
        print "Populating queue"
        for keyword in keywords:
            keyword = keyword.strip()
            keywords_queue.put(keyword)



        print "Starting %d workers" % max_threads
        for i in range(max_threads):
            worker = Thread(target=task, args=(keywords_queue, title,))
            worker.setDaemon(True)
            worker.start()
        keywords_queue.join()

        result = {}  # dictionary to keep output
        key = []  # list to store keywords and relevance_score
        result["ASIN"] = Asin
        response, dic = get_keyword()
        # response, dic = li, l
        # result['keywords'] = get_keyword(words, title)
        for r in response:
            key.append({'keyword': r, 'relevance_score': dic[r]})

        result["result"] = key
        return flask.jsonify(result)
    else:
        result = {"keywords": keywords}
        return flask.jsonify(result)


def get_keyword():

    def comp(val):
        v = val.strip()
        if v in l.keys():
            # print (-float(l[v]))
            return -float(l[v])
        else:
            return 0

    for w in sorted(sen, key=comp):
        if w.strip() in l.keys():
            li.append(w)
    return li, l
    # return


def task(queue, title):
    doc = nlp(title)
    while not queue.empty():

        word = queue.get()
        queue.task_done()

        if word not in l.keys():
            doc1 = nlp(word)
            l[word] = doc1.similarity(doc)
            sen.append(word)
        else:
            print ("exists")

