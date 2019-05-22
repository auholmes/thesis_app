from bs4 import BeautifulSoup


def create_header(title='', author='', editor=''):
    soup = BeautifulSoup(features='xml')
    soup.append(soup.new_tag('teiHeader'))
    soup.find('teiHeader').append(soup.new_tag('fileDesc'))
    soup.find('fileDesc').append(soup.new_tag('titleStmt'))
    if title != '':
        soup.find('titleStmt').append(soup.new_tag('title'))
        soup.title.string = title
    if author != '':
        soup.find('titleStmt').append(soup.new_tag('author'))
        soup.author.string = author
    if editor != '':
        soup.find('titleStmt').append(soup.new_tag('editor'))
        soup.editor.string = editor
    return soup


def create_xml(header, body=''):
    soup = BeautifulSoup(features='xml')
    soup.append(soup.new_tag('TEI', xmlns="http://www.tei-c.org/ns/1.0"))
    soup.TEI.append(header)
    return soup.prettify()


if __name__ == '__main__':
    print(create_header(author='author', editor='editor'))
