import flask
import spacy
from flask import Flask
from Queue import Queue
import threading
# Setup flask app
flask_app = Flask(__name__)
from app import nlp
import process_keywords

import operator



l = {}
exitFlag = 0
queueLock = threading.Lock()
workQueue = Queue()



@flask_app.route('/')
def index():
    return 'Index Page'



@flask_app.route('/keywords/', methods=['POST'])
def keyword():
    # exitFlag = 0

    payload = flask.request.get_json(force=True)
    keywords = payload["keywords"]
    title = payload["title"]
    title = nlp(title)
    Asin = payload["Asin"]
    sort = payload["sort"]
    l.clear()

    if sort:
        global exitFlag
        exitFlag = 0

        threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5", "Thread-6", "Thread-7", "Thread-8",
                      "Thread-9", "Thread-10"]

        workQueue.queue.clear()
        threads = []
        threadID = 1

        # Create new threads
        for tName in threadList:
            thread = process_keywords.myThread(threadID, tName, workQueue, title)
            thread.start()
            threads.append(thread)
            threadID += 1

        # Fill the queue
        queueLock.acquire()
        for word in keywords:
            workQueue.put(word.strip())
        queueLock.release()

        # Wait for queue to empty
        while not workQueue.empty():
            pass

        # Notify threads it's time to exit
        exitFlag = 1

        # Wait for all threads to complete
        for t in threads:
            t.join()
        print "Exiting Main Thread"
        key = []
        result = {}
        sorted_l = sorted(l.items(), key=operator.itemgetter(1), reverse=True)
        for r in sorted_l:
            key.append({'keyword': r[0], 'relevance_score': r[1]})
        result["result"] = key
        return flask.jsonify(result)
    else:
        result = {"keywords": keywords}
        return flask.jsonify(result)

