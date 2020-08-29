import nltk


# http://www.nltk.org/book/ch07.html
class NLTK:

    def __init__(self):
        for resource in ['punkt', 'averaged_perceptron_tagger', 'maxent_ne_chunker', 'words']:
            nltk.download(resource, download_dir='nltk_data/', quiet=True)
        nltk.data.path.append('./nltk_data/')

    def extract_entities(self, text):
        tokens = nltk.word_tokenize(text)
        tagging = nltk.pos_tag(tokens)
        named_entities = nltk.ne_chunk(tagging)
        return list(set([' '.join(w for w, t in elt) for elt in named_entities
                         if type(elt) == nltk.tree.Tree and elt.label() in ['LOCATION', 'GPE', 'PERSON', 'ORGANIZATION']]))
