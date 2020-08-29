import stanza


# https://stanfordnlp.github.io/stanza/ner.html#accessing-named-entities-for-sentence-and-document
class Stanza:

    def __init__(self):
        stanza.download('en', dir='stanza_data/', logging_level='ERROR')  # This downloads the English models for the neural pipeline
        self.nlp = stanza.Pipeline('en', dir='stanza_data', logging_level='ERROR')  # This sets up a default neural pipeline in English

    def extract_entities(self, text):
        doc = self.nlp(text)
        return list(set([e.text for e in doc.entities
                         if e.type in ['PERSON', 'ORG', 'LOC', 'GPE']]))

