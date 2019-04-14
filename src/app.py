from flask import Flask, request, render_template
from gevent.pywsgi import WSGIServer

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def submit_text():
    text = request.form['text']
    return 'Sorry, this doesn\'t do anything (yet).'

if __name__ == '__main__':
    WSGIServer(('0.0.0.0', 3000), app).serve_forever()
