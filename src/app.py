import re
from flask import Flask, request, render_template
from gevent.pywsgi import WSGIServer
from src.ner.flair_ner import tag_entities
from src.tei.assemble_tei import create_header, create_xml

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
    title = request.form['teiHeaderTitle']
    author = request.form['teiHeaderAuthor']
    editor = request.form['teiHeaderEditor']

    tei_header = create_header(title, author, editor)

    text = request.form['rawText']
    text = re.sub('\t', ' ', text)
    text = re.sub(' +', ' ', text)

    tei_document = create_xml(tei_header, '')
    return render_template('output.html',
                           tei=tei_document,
                           results=tag_entities(text))


if __name__ == '__main__':
    WSGIServer(('0.0.0.0', 3000), app).serve_forever()
