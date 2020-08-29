# NERComparison
This project aims at comparing the performance of various named entity extractors in Python:
* [Dandelion](https://dandelion.eu) (en, it)
* [Apple's Natural Language framework](https://developer.apple.com/documentation/naturallanguage) (en, it)
* [Polyglot](https://polyglot.readthedocs.io/en/latest/) (en, it)
* [Spacy](https://spacy.io/) (en, it)
* [NLTK (Natural Language Toolkit)](http://www.nltk.org/book/ch07.html) (en)
* [Stanford CoreNLP](https://nlp.stanford.edu/software/CRF-NER.shtml#Download) (en)
* [Stanza](https://stanfordnlp.github.io/stanza/ner.html#accessing-named-entities-for-sentence-and-document) (en)
* [Google Cloud](https://cloud.google.com/natural-language/docs/analyzing-entities#language-entities-string-python) (en, it)
* [Tint](http://tint.fbk.eu/download.html) (it)

Over two different datasets:
* [Annotated Corpus for Named Entity Recognition](https://www.kaggle.com/abhinavwalia95/entity-annotated-corpus?select=ner_dataset.csv) (en)
* [Italian Content Annotation Bank (I-CAB)](https://ontotext.fbk.eu/i-cab/download-icab.html) (it)

## Results averaged over 50 different articles
Results (en)             |  Results (it)
:-------------------------:|:-------------------------:
![](https://user-images.githubusercontent.com/11541888/91637891-e540f200-ea0b-11ea-83aa-791b5fd9fbc5.png)  |  ![](https://user-images.githubusercontent.com/11541888/91637894-e83be280-ea0b-11ea-997a-b2fea4ade46a.png)

## Steps to reproduce
Download this project and install all the requirements:
```bash
$ git clone https://github.com/n3d1117/NERComparison.git
$ cd NERComparison/
$ source venv/bin/activate
$ pip install requirements.txt
```

### Datasets
* Download the english dataset [here](https://www.kaggle.com/abhinavwalia95/entity-annotated-corpus?select=ner_dataset.csv), name it `dataset_orig.csv` and place it in `datasets/en/` folder
* Download the italian dataset [here](https://ontotext.fbk.eu/i-cab/download-icab.html), and place the `I-CAB_All` folder in `datasets/it/`

### Requirements
* For Dandelion, you need to add your token to the `ner_dandelion.py` file (line 8, replace `xxx`). You can generate your token in the [Dandelion dashboard](https://dandelion.eu/profile/dashboard/) after signing up
* For Apple's Natural Language framework, make sure your have [Swift](https://swift.org) installed on your machine (Windows not supported at the moment)
* For the Stanford NER, download the zip file from [here](https://nlp.stanford.edu/software/CRF-NER.html#Download), unzip it and place the contents in a root folder called `stanford`
* For Google Cloud, generate your json authentication file (see [here](https://cloud.google.com/docs/authentication/getting-started) for more info), name it `auth.json` and place it in a root folder called `google-cloud-auth`
* For Tint, you need to manually start the local server on port 8012. Just download the latest version form [here](https://tint.fbk.eu/download.html) and run the `tint-server.sh` bash file

### Run
Once your have all the requirements, run the main file `main.py` to start the process.

Cleaned datasets will be added to the `dataset` folder. Results will appear in the `results` folder.

## Report
Full report is available [here](/report/relazione.pdf), in italian.