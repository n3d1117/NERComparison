import nltk
from nltk.tag import StanfordNERTagger


# https://nlp.stanford.edu/software/CRF-NER.shtml#Download
class Stanford:

    def __init__(self):

        nltk.download('punkt', download_dir='nltk_data/', quiet=True)
        nltk.data.path.append('./nltk_data/')

        model = './stanford/classifiers/english.muc.7class.distsim.crf.ser.gz'
        jar = './stanford/stanford-ner.jar'
        self.tagger = StanfordNERTagger(model, jar)

    def extract_entities(self, text):
        tokens = nltk.word_tokenize(text)
        chunk = []
        entities = []
        for token, tag in self.tagger.tag(tokens):
            if tag == 'O':
                if chunk:
                    entities.append(' '.join([c[0] for c in chunk]))
                    chunk = []
            elif tag in ['PERSON', 'LOCATION', 'ORGANIZATION', 'GPE']:
                chunk.append((token, tag))
        return list(set(entities))
