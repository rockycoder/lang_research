from fast_api import flask_app
import spacy
nlp = spacy.load("en_core_web_lg")

if __name__ == "__main__":
    flask_app.run(port=8080, host="0.0.0.0", threaded=True)
