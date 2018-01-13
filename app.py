from fast_api import flask_app
import spacy_lib

if __name__ == "__main__":
    spacy_lib.SPSpacy.getnlp()
    flask_app.run(port=8080, host="0.0.0.0", threaded=True)
