from detector import detector
import pickle as pkl
import string
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

class SVM_model(detector):
    def __init__(self, mpath : str):
        self.mpath = mpath
        self.featureDict = {}
        self.table = str.maketrans({key: None for key in string.punctuation})
        self.model = self._loadModel()        

    def _loadModel(self):
        with open(self.mpath, 'rb') as myfile:
            model = pkl.load(myfile)
        return model

    def preProcess(self, text):
        lemmatizer = WordNetLemmatizer()
        filtered_tokens=[]
        lemmatized_tokens = []
        stop_words = set(stopwords.words('english'))
        text = text.translate(self.table)
        for w in text.split(" "):
            if w not in stop_words:
                lemmatized_tokens.append(lemmatizer.lemmatize(w.lower()))
            filtered_tokens = [' '.join(l) for l in nltk.bigrams(lemmatized_tokens)] + lemmatized_tokens
        return filtered_tokens

    def toFeatureVector(self, Rating, verified_Purchase, product_Category, tokens):
        localDict = {}
        self.featureDict["R"] = 1   
        localDict["R"] = Rating
        self.featureDict["VP"] = 1
                
        if verified_Purchase == "N":
            localDict["VP"] = 0
        else:
            localDict["VP"] = 1
        
        if product_Category not in self.featureDict:
            self.featureDict[product_Category] = 1
        else:
            self.featureDict[product_Category] = +1
                
        if product_Category not in localDict:
            localDict[product_Category] = 1
        else:
            localDict[product_Category] = +1                
                
        #Text        
        for token in tokens:
            if token not in self.featureDict:
                self.featureDict[token] = 1
            else:
                self.featureDict[token] = +1
                
            if token not in localDict:
                localDict[token] = 1
            else:
                localDict[token] = +1
        
        return localDict

    def predict(self, reviewSamples):
        # reviewSamples = ([rating, verified purchases, category, preprocessed token], label)
        return self.model.classify_many(map(lambda t: t[0], reviewSamples))