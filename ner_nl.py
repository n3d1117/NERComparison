import json
import subprocess


# https://developer.apple.com/documentation/naturallanguage
class NaturalLanguageFramework:
    def __init__(self):
        # Compile .swift file into binary (only once)
        subprocess.check_output('cd nl && swiftc -o ner ner.swift', shell=True, stderr=subprocess.STDOUT)

    def extract_entities(self, text):

        # Fill .txt file with given text
        file = open("nl/text.txt", "w")
        file.write(text)
        file.close()

        output = subprocess.check_output('cd nl && ./ner', shell=True, stderr=subprocess.STDOUT)
        if output:
            entities = json.loads(output)
            return list(set(entities))
        else:
            print('[NaturalLanguageFramework] failed to extract entities')
            return []