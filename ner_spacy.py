import spacy


# https://spacy.io
class Spacy:

    def __init__(self, language):
        if language == 'it':
            self.nlp = spacy.load('it_core_news_sm')
            self.personTag = 'PER'
        else:
            self.nlp = spacy.load('en_core_web_sm')
            self.personTag = 'PERSON'

    def extract_entities(self, text):
        doc = self.nlp(text)
        return list(set([e.text for e in doc.ents
                         if e.label_ in ['LOC', 'GPE', self.personTag, 'ORG']]))