from google.cloud import language_v1
from google.cloud.language_v1 import enums


# https://cloud.google.com/natural-language/docs/analyzing-entities#language-entities-string-python
class GoogleCloudNER:

    def __init__(self, language):
        self.language = language
        self.client = language_v1.LanguageServiceClient.from_service_account_file('./google-cloud-auth/auth.json')

    def extract_entities(self, text):
        document = {"content": text, "type": enums.Document.Type.PLAIN_TEXT, "language": self.language}
        response = self.client.analyze_entities(document, encoding_type=enums.EncodingType.UTF8)
        return list(set([entity.mentions[0].text.content for entity in response.entities
                         if enums.Entity.Type(entity.type).name in ['PERSON', 'LOCATION', 'ORGANIZATION']
                         and enums.EntityMention.Type(entity.mentions[0].type).name == 'PROPER']))
