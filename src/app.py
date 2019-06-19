import re
from flask import Flask, request, render_template
from gevent.pywsgi import WSGIServer
from src.ner.flair_ner import tag_entities
from src.tei.assemble_tei import create_header, create_xml, create_body

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
    publisher = request.form['teiHeaderPublisher']
    publisher_address = request.form['teiHeaderPublisherAddress']
    publication_date = request.form['teiHeaderPublicationDate']
    license_desc = request.form['teiHeaderLicense']
    project_description = request.form['teiHeaderProjectDescription']
    source_description = request.form['teiHeaderSourceDescription']

    project_description = re.sub('\n|\t\r|\r\n', ' ', project_description)
    project_description = re.sub(' +', ' ', project_description)
    if project_description != '':
        project_description = tag_entities(project_description)

    source_description = re.sub('\n|\t\r|\r\n', ' ', source_description)
    source_description = re.sub(' +', ' ', source_description)
    if source_description != '':
        source_description = tag_entities(source_description
                                          )
    # Create header
    tei_header = create_header(title, author, editor, publisher, publisher_address,
                               publication_date, license_desc, project_description, source_description)

    # Create body
    text = request.form['rawText']
    text = re.sub('\n|\t\r|\r\n', ' ', text)
    text = re.sub(' +', ' ', text)

    flair_output = tag_entities(text)
    tei_body = create_body(flair_output)

    # Assemble document
    tei_document = create_xml(tei_header, tei_body).decode('unicode-escape')
    return render_template('output.html',
                           tei=tei_document)


if __name__ == '__main__':
    WSGIServer(('0.0.0.0', 3000), app).serve_forever()
