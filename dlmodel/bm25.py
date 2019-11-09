from math import log

class bm25:
    def __init__(self, docs, tokenizer):        
        self.docList = docs
        self.tokenizer = tokenizer
        self.materials = self._getMaterials()

    def _calcDoc(self, tokenList):
        # 하나의 문서 안에서 단어의 등장 횟수와 문서의 길이 계산
        docDict = {}
        docDict["fl"] = len(tokenList)  # field length
        docDict["nwid"] = {}            # number of word in doc

        for token in tokenList:
            if token in docDict["nwid"]:
                docDict["nwid"][token] += 1
            else:
                docDict["nwid"][token] = 1
        
        return docDict

    def _getMaterials(self):
        # idf와 tf를 구하기 위한 변수 계산
        materials = {}
        materials["docCount"] = len(self.docList)
        materials["avgFieldLength"] = 0
        materials["docsFreq"]= {}
        materials["docs"] = []
        
        for doc in self.docList:
            tokenizedDoc = self.tokenizer(doc)
            docDict = self._calcDoc(tokenizedDoc)
            materials["avgFieldLength"] += docDict["fl"]
            materials["docs"].append(docDict)
            for token in docDict["nwid"].keys():
                if token in materials["docsFreq"].keys():
                    materials["docsFreq"][token] += 1
                else:
                    materials["docsFreq"][token] = 1
        materials["avgFieldLength"] /= materials["docCount"]
        return materials

    def _idf(self, docFreq, docCount):
        return log(1 + (docCount - docFreq + 0.5) / (docFreq + 0.5))
    
    def _tfNorm(self, termFreq, avgFieldLength, fieldLength, k1, b):
        return (termFreq * (k1 + 1)) / (termFreq + k1 * (1 - b + b * fieldLength / avgFieldLength))

    def _calcBm25(self, docFreq, docCount, termFreq, avgFieldLength, fieldLength, k1, b):
        return self._idf(docFreq, docCount) * self._tfNorm(termFreq, avgFieldLength, fieldLength, k1 = k1, b = b)

    def getResult(self, k1 = 1.2, b = 0.75):
        calcBm25List = []
        docIdx = 0
        for elem in self.materials["docs"]:
            bm25Dict = {}
            preprocessedDoc = elem["nwid"]
            for token in preprocessedDoc:
                docFreq = self.materials["docsFreq"][token]
                docCount = self.materials["docCount"]
                termFreq = self.materials["docs"][docIdx]["nwid"][token]
                avgFieldLength = self.materials["avgFieldLength"]
                fieldLength = self.materials["docs"][docIdx]["fl"]
                result = self._calcBm25(docFreq, docCount, termFreq, avgFieldLength, fieldLength, k1, b)
                bm25Dict[token] = result
            calcBm25List.append(bm25Dict)
            docIdx += 1
        return calcBm25List