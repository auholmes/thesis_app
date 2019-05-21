from flair.models import SequenceTagger
from flair.data import Sentence
import logging
from nltk.tokenize import sent_tokenize
from spacy import displacy

tagger = SequenceTagger.load('ner')
logging.info('Loaded tagger')


def tag_entities(text):
    sentences = sent_tokenize(text)
    output = []
    for s in sentences:
        s = Sentence(s)
        tagger.predict(s)
        output.append(s.to_dict(tag_type='ner'))
    return output

