from flask import Flask, render_template
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    WSGIServer(('0.0.0.0', 3000), app).serve_forever()
