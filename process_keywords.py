import new_app
# from new_app import exitFlag, workQueue, queueLock, l, nlp
from app import nlp
import time
import threading
import datetime


class myThread (threading.Thread):
    def __init__(self, threadID, name, q, title):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
        self.title = title
        self.result_dic = {}

    def run(self):
        print "Starting " + self.name
        get_keyword(self.name, self.q, self.title)
        print "Exiting " + self.name


def get_keyword(threadName, q, title):
    # sorted_l = sorted(l.items(), key = operator.itemgetter(1), reverse=True)
    # return sorted_l
    while not new_app.exitFlag:
        new_app.queueLock.acquire()
        if not new_app.workQueue.empty():
            data = q.get()
            new_app.queueLock.release()
            doc1 = nlp(data)
            score = doc1.similarity(title)
            new_app.l[data] = score
            print "%s processing %s  %-100s" % (threadName, data,datetime.datetime.utcnow())
        else:
            new_app.queueLock.release()
