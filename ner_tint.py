import requests
import time
import os


# http://tint.fbk.eu/download.html
class Tint:
    def __init__(self):

        def check_server():
            try:
                requests.get('http://0.0.0.0:8012/tint?text=test')
            except:
                print('To continue, please start Tint server! (./tint/tint-server.sh)')
                time.sleep(2)
                check_server()

        check_server()

        # This doesn't work for some reason (hangs after a few requests), you need to start the server manually instead
        # Start server
        # subprocess.Popen('./tint/tint-server.sh', stdout=subprocess.PIPE)
        # time.sleep(15)

    # def __del__(self):
        # os.system('./tint/stop-server.sh')

    def extract_entities(self, text):
        base_url = 'http://0.0.0.0:8012/tint?text={}'.format(text)

        json = requests.get(base_url).json()

        entities = []
        chunk = []
        for sentence in json['sentences']:
            for token in sentence['tokens']:
                if token['ner'] not in ['LOC', 'ORG', 'PER', 'GPE']:
                    if chunk:
                        entities.append(' '.join([c['word'] for c in chunk]))
                        chunk = []
                else:
                    chunk.append(token)
        return list(set(entities))