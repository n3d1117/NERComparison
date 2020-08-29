from ner_nltk import NLTK
from ner_spacy import Spacy
from ner_polyglot import Polyglot
from ner_dandelion import Dandelion
from ner_tint import Tint
from ner_nl import NaturalLanguageFramework
from ner_stanford import Stanford
from ner_googlecloud import GoogleCloudNER
from ner_stanza import Stanza


class EntityExtractor:

    def __init__(self, language):

        self.spacy = Spacy(language)
        self.polyglot = Polyglot(language)
        self.dandelion = Dandelion(language)
        self.nl = NaturalLanguageFramework()
        self.nltk = NLTK()
        self.stanford = Stanford()
        self.google_cloud = GoogleCloudNER(language)
        self.stanza = Stanza()

        if language == 'it':  # don't load tint if language is 'en', as it takes some time
            self.tint = Tint()

    def extract_entities(self, text, tool, quiet=False):
        if tool == 'spacy':
            if not quiet:
                print('[*] Extracting entities using Spacy...')
            return self.spacy.extract_entities(text)
        elif tool == 'polyglot':
            if not quiet:
                print('[*] Extracting entities using Polyglot...')
            return self.polyglot.extract_entities(text)
        elif tool == 'dandelion':
            if not quiet:
                print('[*] Extracting entities using Dandelion...')
            return self.dandelion.extract_entities(text)
        elif tool == 'nl':
            if not quiet:
                print('[*] Extracting entities using NaturalLanguage framework...')
            return self.nl.extract_entities(text)
        elif tool == 'nltk':
            if not quiet:
                print('[*] Extracting entities using Natural Language Toolkit (NLTK)...')
            return self.nltk.extract_entities(text)
        elif tool == 'stanford':
            if not quiet:
                print('[*] Extracting entities using Stanford NER Tagger...')
            return self.stanford.extract_entities(text)
        elif tool == 'tint':
            if not quiet:
                print('[*] Extracting entities using Tint...')
            return self.tint.extract_entities(text)
        elif tool == 'gcloud':
            if not quiet:
                print('[*] Extracting entities using Google Cloud...')
            return self.google_cloud.extract_entities(text)
        elif tool == 'stanza':
            if not quiet:
                print('[*] Extracting entities using Stanza...')
            return self.stanza.extract_entities(text)
        raise NameError
