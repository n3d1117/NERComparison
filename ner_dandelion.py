import requests


# https://dandelion.eu
class Dandelion:

    def __init__(self, language):
        self.token = 'xxx'
        self.language = language

    def extract_entities(self, text):

        base_url = 'https://api.dandelion.eu/datatxt/nex/v1/?lang={}&min_confidence=0.75&token={}&text={}'\
                    .format(self.language, self.token, text)
        json = requests.get(base_url).json()

        if 'annotations' in json:
            return list(set([entity['spot'] for entity in json['annotations']]))
        else:
            print('[*] hit dandelion daily limit!')
            return []