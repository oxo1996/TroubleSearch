from .imodel import imodel
import json
import math
import numpy as np

class avgtfw2v(imodel):
    def __init__(self, word2vecPath : str, modelPath : str):
        self.w2vPath = word2vecPath # 현재 특정 증상에 관한 벡터만 받아옴. 보완해야 함.
        self.mPath = modelPath
        self.w2v = self._loadW2v()
        self.ingrW2v = self._loadModel()
        self.ingrKo2Eng = self._loadIngrKo2Eng()
        self.items = self._loadItems()

    def _loadW2v(self):
        with open(self.w2vPath) as data_file:    
            w2v = json.load(data_file)
        return w2v

    def _loadModel(self):
        with open(self.mPath) as data_file:    
            ingrW2v = json.load(data_file)
        return ingrW2v

    def _loadIngrKo2Eng(self):
        with open("webcrawler/ingrKo2Eng.json") as data_file:    
            ingrKo2Eng = json.load(data_file)
        return ingrKo2Eng
        
    def _loadItems(self):
        with open("webcrawler/items.json") as data_file:    
            items = json.load(data_file)
        return items

    def _l2Norm(self, a : float):
        return math.sqrt(np.dot(a, a))

    def _cosine_similarity(self, a : float, b : float):
        #print(np.dot(a,b) / (self._l2Norm(a) * self._l2Norm(b)))
        return np.dot(a,b) / (self._l2Norm(a) * self._l2Norm(b))

    #def _weights(self, numIngr, similarities):


    def mostSimilar(self, symptom, product, topn : int, order = True):
        calc_cs = {}
        koIngrList = self.items[product]["ingredients"]
        symptomVec = self.w2v[symptom]

        for koName in koIngrList:
            try: 
                engName = self.ingrKo2Eng[koName]
                iwv = self.ingrW2v[engName]
                calc_cs[koName] = self._cosine_similarity(iwv, symptomVec)
                #calc_cs[engName] = self._cosine_similarity(iwv, symptomVec)
            except KeyError as e:
                #print(e)
                continue
        
        res = sorted(calc_cs.items(), key=(lambda x: x[1]), reverse = order)
        return res[:topn]

    def getResult(self, symptom, products):
        topn = 3
        temp = {}
        vecDict = {}
        result = {}
        
        for pname in products:
            vecDict[pname] = {}
            vecDict[pname]["ingr"] = []
            sum = 0
            similarity = self.mostSimilar(symptom, pname, topn)
            for idx in range(topn):
                vecDict[pname]["ingr"].append(similarity[idx])
                sum += similarity[idx][1]
            temp[pname] = sum / len(similarity)
            vecDict[pname]["sim"] = sum / len(similarity)

        sorting = sorted(temp.items(), key=(lambda x: x[1]), reverse = True)

        for pname in sorting:
            result[pname[0]] = vecDict[pname[0]]

        return result