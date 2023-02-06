import csv
import json

from nltk.corpus import wordnet
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def FindSynonyms(word):
    synonymList = []
    for synset in wordnet.synsets(word):
        for synonym in synset.lemmas():
            if synonym.name().lower() == word:
                continue
            else:
                synonymList.append(synonym.name())
    return synonymList


def ProcessCorpus(corpus, lexicon):
    synonymList = []
    weightedCorpus = {}
    for corpusWord in corpus:
        if corpusWord in lexicon:
            continue
        else:
            synonymList = FindSynonyms(corpusWord)
            for synonym in synonymList:
                if synonym in lexicon:
                    corpusWordRating = lexicon[synonym]
                    print(f'{synonym}: {corpusWordRating}')
                    weightedCorpus[synonym] = corpusWordRating
                    break
    return weightedCorpus


def GenerateCorpusFile(corpus):
    with open('corpus.txt', 'a+') as corpusFile:
        fileHasLines = False
        corpusFile.seek(0)
        for entry in corpus:
            if fileHasLines == True:
                corpusFile.write('\n')
            else:
                fileHasLines = True
            corpusFile.write(f'{entry}\t{corpus[entry]}')


with open('adjs.json') as adjs:
    adjsList = json.load(adjs)
    adjsList = adjsList['adjs']

with open('descriptions.json') as desc:
    descList = json.load(desc)
    descList = descList['descriptions']

with open('encouraging_words.json') as enc:
    encList = json.load(enc)
    encList = encList['encouraging_words']

csvList = []
with open('Adjectives.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        csvList.append(row['Word'])

corpusList = []
for jsonObj in (adjsList, descList, encList, csvList):
    for i in jsonObj:
        corpusList.append(i.strip())

# purge duplicates using set datatype, order change is irrelevant
corpusList = list(set(corpusList))

print(corpusList)
#vader = SentimentIntensityAnalyzer()
