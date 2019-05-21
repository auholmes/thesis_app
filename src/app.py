import re
from flask import Flask, request, render_template
from gevent.pywsgi import WSGIServer
from src.ner.flair_ner import tag_entities

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('markup.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/output')
def output():
    return render_template('output.html')


@app.route('/', methods=['POST'])
def submit_text():
    text = request.form['rawtext']
    text = re.sub('\t', ' ', text)
    text = re.sub(' +', ' ', text)
    return render_template('output.html', results=tag_entities(text))


if __name__ == '__main__':
    WSGIServer(('0.0.0.0', 3000), app).serve_forever()
