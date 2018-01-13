import en_core_web_lg


class SPSpacy(object):

    nlp = {}

    @staticmethod
    def getnlp():
        if SPSpacy.nlp is not None:
            SPSpacy.nlp = en_core_web_lg.load()
            return SPSpacy.nlp
        else:
            return SPSpacy.nlp
