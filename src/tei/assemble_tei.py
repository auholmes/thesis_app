import re
from bs4 import BeautifulSoup
from lxml import etree
from src.utils.license_utils import license_dict


tag_dict = {'PER': 'persName',
            'LOC': 'placeName',
            'MISC': 'orgName',
            'ORG': 'name'}

titles = ['Mr.', 'Mr', 'Mrs.', 'Mrs', 'Miss', 'Dr.', 'Dr', 'Sir', 'Ms.', 'Ms']


def create_name_ref(x):
    ref = x.split()
    ref = [t for t in ref if t not in titles]
    ref.insert(0, ref.pop(-1))
    ref = '#{}'.format('_'.join(ref))
    return re.sub(r'\.|,', '', ref)


def create_ref(x):
    ref = x.split()
    ref = '#{}'.format('_'.join(ref))
    return re.sub(r'\.|,', '', ref)


def create_header(title='', author='', editor='', publisher='', publisher_address='',
                  publication_date='', license_desc=''):
    soup = BeautifulSoup()
    soup.append(soup.new_tag('teiHeader'))
    soup.find('teiHeader').append(soup.new_tag('fileDesc'))
    soup.find('fileDesc').append(soup.new_tag('titleStmt'))
    if title != '':
        soup.find('titleStmt').append(soup.new_tag('title'))
        soup.title.string = title
    if author != '':
        soup.find('titleStmt').append(soup.new_tag('author'))
        soup.author.append(soup.new_tag('persName'))
        soup.author.persName.string = author
        soup.author.persName['ref'] = create_name_ref(author)
    if editor != '':
        soup.find('titleStmt').append(soup.new_tag('editor'))
        soup.editor.append(soup.new_tag('persName'))
        soup.editor.persName.string = editor
        soup.editor.persName['ref'] = create_name_ref(editor)
    if publisher != '':
        soup.fileDesc.append(soup.new_tag('publicationStmt'))
        soup.publicationStmt.append(soup.new_tag('publisher'))
        soup.publisher.append(soup.new_tag('orgName'))
        soup.publisher.orgName.string = publisher
        soup.publisher.orgName['ref'] = create_ref(publisher)
        if publisher_address != '':
            soup.publicationStmt.append(soup.new_tag('address'))
            soup.publicationStmt.address.append(soup.new_tag('addrLine'))
            soup.publicationStmt.address.addrLine.string = publisher_address
        if license_desc != '':
            soup.publicationStmt.append(soup.new_tag('availability'))
            soup.availability.append(soup.new_tag('license'))
            soup.license['target'] = license_dict[license_desc]['target']
            soup.license.string = license_dict[license_desc]['text']
        if publication_date != '':
            soup.publicationStmt.append(soup.new_tag('date'))
            soup.publicationStmt.date.string = publication_date
    return soup


def create_body(flair_output):
    soup = BeautifulSoup()
    soup.append(soup.new_tag('text'))
    soup.find('text').append(soup.new_tag('body'))
    soup.body.append(soup.new_tag('div'))
    soup.div.append(soup.new_tag('p'))
    markup = ''
    for x in flair_output:
        text = x['text']
        entities = x['entities']
        index = 0
        for e in entities:
            if e['text'] not in ["I’ve", "I’ll", "I", "I’m", "I've", "I'll", "I'm"]:
                markup += text[index:e['start_pos']]
                markup += '<{}>{}</{}>'.format(tag_dict[e['type']], e['text'], tag_dict[e['type']])
                index = e['end_pos']
        markup += text[index:]
        markup += ' '
    markup = markup[0:-1]
    soup.p.string = markup
    return soup


def create_xml(header, body):
    soup = BeautifulSoup()
    soup.append(soup.new_tag('TEI', xmlns="http://www.tei-c.org/ns/1.0"))
    soup.TEI.append(header)
    soup.TEI.append(body)
    root = etree.fromstring(str(soup))
    xml_str = etree.tostring(root, pretty_print=True).decode()
    xml_str = re.sub('&lt;', '<', xml_str)
    xml_str = re.sub('&gt;', '>', xml_str)
    xml_str = re.sub('&amp;', '&', xml_str)
    xml_str = re.sub('&#163;', '£', xml_str)
    xml_str = re.sub('&#8220;', '"', xml_str)
    xml_str = re.sub('&#8221;', '"', xml_str)
    xml_str = re.sub('&#8217;', "'", xml_str)
    xml_str = re.sub(' Nile.', ' <placeName ref="Nile">Nile</placeName>.', xml_str)

    return xml_str.encode('utf-8')


if __name__ == '__main__':
    flair_output = [{'text': 'Hello, my name is Audrey.', 'labels': [], 'entities': [{'text': 'Audrey.', 'start_pos': 18, 'end_pos': 25, 'type': 'PER', 'confidence': 0.9849573373794556}]},
                    {'text': 'I love New York.', 'labels': [], 'entities': [
                        {'text': 'New York.', 'start_pos': 7, 'end_pos': 16, 'type': 'LOC',
                         'confidence': 0.9960977137088776}]}
                    ]
    header = create_header('Title', 'Author', 'Editor')
    body = create_body(flair_output)
    print(create_xml(header, body))
