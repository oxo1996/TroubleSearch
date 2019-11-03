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
        with open("../webcrawler/ingrKo2Eng.json") as data_file:    
            ingrKo2Eng = json.load(data_file)
        return ingrKo2Eng
        
    def _loadItems(self):
        with open("../webcrawler/items.json") as data_file:    
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

    def _productTotSim(self, similarities):
        # 현재 sim이 높은 topn개의 성분의 평균으로 상품과 증상 간의 유사도 계산
        topn = 3
        sum = 0
        
        for idx in range(topn):
            sum += similarities[idx][1]

        return sum / topn

    def recommendProduct(self, symptom):
        vecList = []
        for pname in self.items.keys():
            if len(self.items[pname]["ingredients"]) < 2:
                print("not exist ingredients data")
                continue
            similarities = self.mostSimilar(symptom, pname, len(self.items[pname]["ingredients"]))
            totSim = self._productTotSim(similarities)
            #print(pname, totSim)
            vecList.append((pname, totSim))
        
        vecList = sorted(vecList, key=(lambda x: x[1]), reverse = False)
        return vecList

    def getResult(self, symptom, products):
        # products는 str의 list
        topn = 3
        vecDict = {}
        result = {}
        
        for pname in products:
            if len(self.items[pname]["ingredients"]) < 2:
                print("not exist ingredients data")
                continue
            vecDict[pname] = {}
            similarity = self.mostSimilar(symptom, pname, topn)
            vecDict[pname]["ingr"] = similarity
            vecDict[pname]["sim"] = self._productTotSim(similarity)

        vecDict = sorted(vecDict.items(), key=(lambda x: x[1]["sim"]), reverse = True)
        print(vecDict)

        return vecDict