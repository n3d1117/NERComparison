import pandas as pd
from utils import cleaned


# https://www.kaggle.com/abhinavwalia95/entity-annotated-corpus#ner_dataset.csv
def preprocess_english_dataset(file, output, n=25000):
    df = pd.read_csv(file, encoding='ISO-8859-1')
    df = df.head(n)  # filter only first n elements
    df = df.fillna(method='ffill')  # use ffill to propagate non-null values forward for easier grouping
    df['Sentence #'] = df['Sentence #'].str.replace('Sentence: ', '')  # rename "Sentence: x" -> "x" for easier indexing

    # Populate Sentences column
    indices = []
    sentences = []
    df1 = df.groupby('Sentence #')['Word'].apply(lambda x: ' '.join(x)).reset_index().rename(columns={'Word': 'Sentence'})
    for index, row in df1.iterrows():
        indices.append(row['Sentence #'])
        sentences.append(cleaned(row['Sentence']))

    d = pd.DataFrame({'id': indices, 'Sentence': sentences})  # create dataframe from data
    d['Entities'] = ''  # initialize empty 'Entities' column

    # Populate entities column

    # Group by sentence and filter only Geographical, Organization and Person entities
    relevant_tags = ['B-geo', 'I-geo', 'B-per', 'I-per', 'B-org', 'I-org']
    df2 = df.groupby('Sentence #', as_index=False).apply(lambda g: g[g['Tag'].isin(relevant_tags)])
    # Compute entities for each sentence
    for i, group in df2.groupby('Sentence #'):
        entities = []
        # If tag starts with "I-" (e.g. "I-geo"), then it needs to be appended to previous value (multi word entity)
        for index, row in group.iterrows():
            if row['Tag'].startswith('I-'):
                last = entities.pop()
                entities.append(last + ' ' + row['Word'])
            else:
                entities.append(row['Word'])
        d['Entities'][d.id == i] = ', '.join(entities)

    # Output an 'id,Sentence,Entities' csv file
    d.id = d.id.astype(int)  # convert 'id' column from string to int
    d = d.sort_values('id')  # sort by index
    d = d[d['Entities'] != '']  # filter out sentences without entities
    d.to_csv(output, index=False)  # export cleaned data to csv


# http://ontotext.fbk.eu/icab.html
def preprocess_italian_dataset(file, output):
    blocks = []
    block = []
    sentences = []
    entities = []
    relevant_tags = ['B-PER', 'I-PER', 'B-ORG', 'I-ORG', 'B-LOC', 'I-LOC']

    f = open(file)

    for line in f:
        if line == '\n':
            blocks.append(block)
            block = []
        else:
            block.append(line)
    f.close()

    for block in blocks:

        # Extract sentences
        full_sentence = ' '.join([line.split(' ', 1)[0] for line in block])
        if len(full_sentence) > 10:  # filter only lines with at least 10 characters
            sentences.append(cleaned(full_sentence))

            # Extract entities in sentence
            l_entities = []
            for line in block:
                word = line.split(' ', 1)[0]
                entity_type = line.split(' ')[-1].replace('\n', '')  # entity tag
                if entity_type in relevant_tags:
                    # If tag starts with "I-" (e.g. "I-LOC"), then it needs to be appended to previous value (multi word entity)
                    if entity_type.startswith('I-'):
                        last = l_entities.pop()
                        l_entities.append(last + ' ' + word)
                    else:
                        l_entities.append(word)
            entities.append(l_entities)

    # create dataframe from data
    d = pd.DataFrame({'id': list(range(len(sentences))), 'Sentence': sentences, 'Entities': [', '.join(entity_list) for entity_list in entities]})

    # Output an 'id,Sentence,Entities' csv file
    d.id = d.id.astype(int)  # convert 'id' column from string to int
    d = d.sort_values('id')  # sort by index
    d = d[d['Entities'] != '']  # filter out sentences without entities
    d.to_csv(output, index=False)  # export cleaned data to csv
