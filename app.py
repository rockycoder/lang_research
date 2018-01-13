from fast_api import flask_app
import en_core_web_lg
nlp = en_core_web_lg.load()

if __name__ == "__main__":
    flask_app.run(port=8080, host="0.0.0.0", threaded=True)
