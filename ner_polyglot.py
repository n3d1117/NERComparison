import os

os.environ['POLYGLOT_DATA_PATH'] = '.'

from polyglot.text import Text
from polyglot.downloader import downloader


# https://polyglot.readthedocs.io/en/latest/
class Polyglot:

    def __init__(self, language):
        self.language = language
        for resource in ['embeddings2.en', 'ner2.en', 'embeddings2.it', 'ner2.it']:
            downloader.download(resource, quiet=True)

    def extract_entities(self, text):
        text = Text(text, hint_language_code=self.language)
        return list(set([' '.join(entity) for entity in text.entities
                         if entity.tag in ['I-LOC', 'I-PER', 'I-ORG']]))
