from imodel import imodel
import json
from gensim.models import Word2Vec,KeyedVectors


class avgtfw2v(imodel):
    def __init__(self, data, label, pw2vPath):
        self.data = data
        self.label = label
        self.pw2vPath = pw2vPath

    def readW2v():
        word_vectors = KeyedVectors.load_word2vec_format('enwiki_20180420_300d.txt', binary=False)
    

    def loadModel(self, path):
        with open(path) as json_file:
            model = json.load(json_file)
        return model

    def saveModel(self):
        with open('avgtfw2v.json', 'w', encoding='utf-8') as make_file:
            json.dump(items, make_file, indent="\t")

    def getData(self):
